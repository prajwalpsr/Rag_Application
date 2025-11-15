from langchain_ollama import OllamaEmbeddings, OllamaLLM
from llama_index.readers.file import PDFReader
from llama_index.core.node_parser import SentenceSplitter
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv(), override=True)

EMBED_MODEL = os.environ["EMBED_MODEL"]
EMBED_DIM = os.environ["EMBED_DIM"]

client = OllamaEmbeddings(model=EMBED_MODEL)

splitter = SentenceSplitter(chunk_size=1000, chunk_overlap=200)

def load_and_chunk_pdf(path: str) -> list[str]:
    docs = PDFReader().load_data(file=path)
    texts = [d.text for d in docs if getattr(d, "text", None)]

    chunks = []
    for t in texts:
        chunks.extend(splitter.split_text(t))
    return chunks 


def embed_texts(chunks: list[str]) -> list[list[float]]:
    vectors = []
    for chunk in chunks:
        vec = client.embed_query(chunk)  
        vectors.append(vec)
    return vectors
