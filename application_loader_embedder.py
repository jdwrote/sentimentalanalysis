from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
import requests


#-----------------------------------------------------------------------------------------------------------------------
#embedding content into vectorstore
#-----------------------------------------------------------------------------------------------------------------------


def load_embed(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes(404, 500, etc.)
        loader = WebBaseLoader(url)
        docs = loader.load()
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

        text_splitter = RecursiveCharacterTextSplitter()
        documents = text_splitter.split_documents(docs)
        vector = FAISS.from_documents(documents, embeddings)
        return vector

    except Exception as e:
        print(f"Error:{e}")
        return None