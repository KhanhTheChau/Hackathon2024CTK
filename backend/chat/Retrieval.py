# import hashlib
# import os
# import getpass
# from typing import List, Tuple
# from dotenv import load_dotenv
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_experimental.text_splitter import SemanticChunker
# from langchain.schema import Document
# from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
# from langchain.vectorstores import FAISS
# from langchain.prompts import ChatPromptTemplate
# from langchain.retrievers import EnsembleRetriever
# from langchain.retrievers.bm25 import BM25Retriever
# from rank_bm25 import BM25Okapi
# import time

# GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']