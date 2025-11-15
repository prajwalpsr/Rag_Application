import uuid
import os
import datetime
import logging
import inngest
import inngest.fast_api
from fastapi import FastAPI
from inngest.experimental import ai
from dotenv import load_dotenv, find_dotenv
from data_loader import load_and_chunk_pdf, embed_texts
from vector_db import QdrantStorage
from custom_types import RAGChunkandSrc, RAGQueryResult, RAGSearchResult, RAGUpsertResult

load_dotenv(find_dotenv(), override=True)

inngest_client = inngest.Inngest(
    app_id='rag_application',
    logger=logging.getLogger("uvicorn"),
    is_production=False,
    serializer=inngest.PydanticSerializer()
)

@inngest_client.create_function(
    fn_id='RAG: Ingest PDF',
    trigger=inngest.TriggerEvent(event='rag/ingest_pdf')
)
async def rag_ingest_pdf(ctx: inngest.Context):
    def _load(ctx: inngest.Context) -> RAGChunkandSrc:
        pdf_path = ctx.event.data["pdf_path"]
        source_id = ctx.event.data.get("source_id", pdf_path)
        chunks = load_and_chunk_pdf(pdf_path)
        return RAGChunkandSrc(chunks=chunks, source_id=source_id)

    def _upsert(chunks_and_src: RAGChunkandSrc) -> RAGUpsertResult:
        chunks = chunks_and_src.chunks
        source_id = chunks_and_src.source_id    
        vecs = embed_texts(chunks)
        ids = [str(uuid.uuid5(uuid.NAMESPACE_URL, f"{source_id}: {i}")) for i in range(len(chunks))]
        payloads = [{"source": source_id, "text":chunks[i]} for i in range(len(chunks))]
        QdrantStorage().upsert(ids, vecs, payloads)
        return RAGUpsertResult(ingested=len(chunks))

    chunks_and_src = await ctx.step.run("load-and-chunk", lambda: _load(ctx), output_type=RAGChunkandSrc)
    ingested = await ctx.step.run('embed-and-upsert', lambda: _upsert(chunks_and_src), output_type=RAGUpsertResult)

    return ingested.model_dump()

@inngest_client.create_function(
    fn_id='RAG: Query PDF',
    trigger = inngest.TriggerEvent(event="rag/query_pdf_ai")
)
async def rag_query_search(ctx: inngest.Context) -> RAGQueryResult:
    def _search(question: str, top_k: int = 5):
        query_vec = embed_texts([question])[0]
        store = QdrantStorage()
        found = store.search(query_vec, top_k)
        return RAGSearchResult(contexts=found['contexts'], sources=found['sources'])
    
    question = ctx.event.data["question"]
    top_k = int(ctx.event.data.get("top_k", 5))

    search_result = await ctx.step.run('embed-and-search', lambda: _search(question, top_k), output_type=RAGSearchResult)

    context_block = "\n\n".join(f"- {c}" for c in search_result.contexts)
    user_content = {
        "Use the following context to answer the quetion.\n\n"
        f"Context:\n{context_block}\n\n"
        f"Question: {question}\n"
        "Answer concisely using the context above."
    }

    adapter = ai.openai.Adapter(
        base_url=os.environ["LLM_URL"],   
        model=os.environ["LLM_MODEL"],                      
        auth_key=""                            
    )

    res = await ctx.step.ai.infer(
        "llm-answer",
        adapter=adapter,
        body={
            "max_tokens": 1024,
            "temperature": 0.2,
            "messages": [
                {
                    "role": "system",
                    "content": "You answer questions using only the provided context."
                },
                {
                    "role": "user",
                    "content": str(user_content)   
                }
            ]
        }
    )

    answer =  res["choices"][0]["message"]["content"]
    return {"answer": answer, "sources": search_result.sources, "num_context": len(search_result.contexts)}

@inngest_client.create_function(
    fn_id='RAG: Delete PDF',
    trigger=inngest.TriggerEvent(event='rag/delete_pdf')
)
async def rag_delete_pdf(ctx: inngest.Context):
    source_id = ctx.event.data['source_id']

    def _delete():
        store = QdrantStorage()

        results = store.client.scroll(
            collection_name=store.collection,
            scroll_filter={"must": [{"key": "source", "match": {"value" : source_id}}]},
            limit=100
        )
        points_id = [p.id for p in results[0]]
        if points_id:
            store.client.delete(store.collection, points_id)
        return {'delete_count': len(points_id)}
    
    result = await ctx.step.run("delete-chunks", _delete)
    return result


app = FastAPI()

inngest.fast_api.serve(app, inngest_client, [rag_ingest_pdf, rag_query_search, rag_delete_pdf])