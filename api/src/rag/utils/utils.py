# INDUSTRIAL ACCIDENT COMPENSATION INSURANCE ACT

import os

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_community.embeddings import OpenAIEmbeddings
from langchain.embeddings import CacheBackedEmbeddings
from langchain.storage import LocalFileStore
#from langchain_community.vectorstores import FAISS

import chromadb
from langchain_community.vectorstores import Chroma

from langchain.chat_models import ChatOpenAI
from langchain.schema.runnable import RunnablePassthrough
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_core.output_parsers import StrOutputParser

from langchain import hub
from langchain_core.prompts import load_prompt
from langchain_core.runnables import RunnableParallel

from operator import itemgetter
import json
import random


async def batch_generate_rag(
        openai_api_key,
        query
):
    oa_embedding = OpenAIEmbeddings(openai_api_key= openai_api_key)
    store = LocalFileStore("/app/cache/")
    cached_embedder= CacheBackedEmbeddings.from_bytes_store(
        oa_embedding, store, namespace=oa_embedding.model)

    chroma_client = chromadb.HttpClient(host="chroma_server",port=8000)

    
    db = Chroma(client=chroma_client,collection_name="law20240209",embedding_function=cached_embedder)
    
    # if os.path.isdir("/app/src/rag/utils/cache"):
    #     oa_embedding = OpenAIEmbeddings(openai_api_key= openai_api_key)
    #     store = LocalFileStore("/app/src/rag/utils/cache/")
    #     cached_embedder= CacheBackedEmbeddings.from_bytes_store(
    #         oa_embedding, store, namespace=oa_embedding.model)
        
    # else:
    #     os.mkdir("/app/src/rag/utils/cache")
    
    #     loader = PyPDFLoader("/app/src/rag/utils/raw20240209.pdf")

    #     docs = loader.load_and_split()
    #     # Data Splitter
    #     text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    #     splits = text_splitter.split_documents(docs)
    #     # Embedding
    #     oa_embedding = OpenAIEmbeddings(openai_api_key= openai_api_key)
    #     store = LocalFileStore("/app/src/rag/utils/cache/")
    #     cached_embedder= CacheBackedEmbeddings.from_bytes_store(
    #         oa_embedding, store, namespace=oa_embedding.model)
    #     # make VectorDB
    #     db = FAISS.from_documents(splits, cached_embedder)
    #     os.mkdir("/app/src/rag/utils/faiss")
    #     db.save_local("/app/src/rag/utils/faiss")

    #make Retriever        
    #db = FAISS.load_local("/app/src/rag/utils/faiss", cached_embedder, allow_dangerous_deserialization=True)
    #db = Chroma(persist_directory="https://chroma_server/chroma/chroma",embedding_function=cached_embedder)
    retriever = db.as_retriever(search_type="mmr",
                                search_kwargs={'k':3})
    # LLM
    llm = ChatOpenAI(model_name = "gpt-4o", temperature = 0, openai_api_key= openai_api_key)
    # Chain
    prompt = hub.pull("rlm/rag-prompt")

    chain = RunnableParallel({"context" : itemgetter("question")|retriever,"question": RunnablePassthrough()}) \
            | RunnableParallel({"reference": itemgetter("context"), "results": prompt| llm| StrOutputParser()})
    # chain = {"context" : itemgetter("question")|retriever,"question": RunnablePassthrough()}\
    #         | prompt \
    #         | llm \
    #         | StrOutputParser()

    result = chain.invoke({"question":query})
    output = (result["results"],result["reference"])
    return output
