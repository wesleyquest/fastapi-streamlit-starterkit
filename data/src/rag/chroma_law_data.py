# INDUSTRIAL ACCIDENT COMPENSATION INSURANCE ACT

import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_community.embeddings import OpenAIEmbeddings
from langchain.embeddings import CacheBackedEmbeddings
from langchain.storage import LocalFileStore

import chromadb
from langchain_community.vectorstores import Chroma

from langchain.chat_models import ChatOpenAI

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

oa_embedding = OpenAIEmbeddings(openai_api_key= openai_api_key)
store = LocalFileStore("/app/volumes/file_volumes/cache/")
cached_embedder= CacheBackedEmbeddings.from_bytes_store(
    oa_embedding, store, namespace=oa_embedding.model)

chroma_client = chromadb.HttpClient(host="chroma_server",port=8000)
existing_collections = [col.name for col in chroma_client.list_collections()]

if "law20240209" not in existing_collections:
    collection = chroma_client.create_collection(name="law20240209")

    loader = PyPDFLoader("/app/volumes/file_volumes/rag/law20240209.pdf")
    docs = loader.load_and_split()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    # docs = [doc.page_content for doc in splits]
    # vectors = [cached_embedder.embed_documents(doc.page_content) for doc in splits]
    # ids = [f"id{i}" for i in range(len(vectors))]
    # metadatas = [{"source":doc.metadata["source"],"page":doc.metadata["page"]} for doc in splits]

    # collection.add(
    #     ids=ids,
    #     documents= docs,
    #     embeddings = vectors,
    #     metadatas=metadatas
    # )

    for i, doc in enumerate(splits):
        # 각 문서의 임베딩 계산
        vectors = cached_embedder.embed_documents([doc.page_content])
        
        # 벡터의 개수에 맞게 ids 리스트를 생성
        ids = [f"doc_{i}_vector_{j}" for j in range(len(vectors))]
        metadatas = [{"source":doc.metadata["source"],"page":doc.metadata["page"]} for doc in splits]
        # 문서와 임베딩을 chromadb에 추가
        collection.add(
            documents=[doc.page_content],  # 텍스트 데이터를 리스트로 전달
            embeddings=vectors,  # 미리 계산한 임베딩을 전달
            ids=ids,  # 각 벡터에 대해 고유한 ID 전달
            #metadatas = [{"source":doc.metadata["source"],"page":doc.metadata["page"]} for doc in splits]
        )

    print("law20240209 chromadb was created!")
else:
    print("law20240209 chromadb was already created!")