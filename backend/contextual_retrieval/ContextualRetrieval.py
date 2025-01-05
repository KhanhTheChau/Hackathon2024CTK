from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from langchain.schema import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from rank_bm25 import BM25Okapi
from typing import List, Tuple
import hashlib
import os
import getpass

class ContextualRetrieval:
    """
    A class that implements the Contextual Retrieval system.
    """

    def __init__(self, embedding_model: str = "models/embedding-001",
              llm_model: str = "gemini-1.5-pro",
              max_history: int = 5):
        """
        Initialize the ContextualRetrieval system with configurable models and conversation history.

        Args:
            embedding_model (str): Model used for generating embeddings
            llm_model (str): Language model for contextual processing
            max_history (int): Maximum number of previous interactions to retain
        """
        # Initialize text splitter with semantic chunking
        self.text_splitter = SemanticChunker(
            GoogleGenerativeAIEmbeddings(model=embedding_model),
            breakpoint_threshold_type="percentile"
        )

        # Create embeddings and language model
        self.embeddings = GoogleGenerativeAIEmbeddings(model=embedding_model)
        self.llm = ChatGoogleGenerativeAI(model=llm_model, temperature=0)

        # Placeholders for retrievers
        self.vector_retriever = None
        self.bm25_retriever = None
        self.ensemble_retriever = None

        # Conversation history management
        self.conversation_history = []
        self.max_history = max_history

    def process_document(self, document: str) -> Tuple[List[Document], List[Document]]:
        """
        Process a document by splitting it into chunks and generating context.

        Args:
            document (str): The input document to process

        Returns:
            Tuple of original chunks and contextualized chunks
        """
        # Split document into semantic chunks
        chunks = self.text_splitter.create_documents([document])

        # Generate contextualized chunks
        # contextualized_chunks = self._generate_contextualized_chunks(document, chunks)

        # return chunks, contextualized_chunks
        return chunks#, contextualized_chunks


    def _generate_contextualized_chunks(self, document: str, chunks: List[Document]) -> List[Document]:
        """
        Generate contextualized versions of the given chunks.
        """
        contextualized_chunks = []
        for chunk in chunks:
            time.sleep(10)
            context = self._generate_context(document, chunk.page_content)
            contextualized_content = f"{context}\n\n{chunk.page_content}"
            contextualized_chunks.append(Document(page_content=contextualized_content, metadata=chunk.metadata))
        return contextualized_chunks

    def _generate_context(self, document: str, chunk: str) -> str:
        """
        Generate context for a specific chunk using the language model.
        """
        prompt = ChatPromptTemplate.from_template("""
        Bạn là một trợ lý AI chuyên cung cấp phân tích ngữ cảnh tài liệu, đặc biệt tập trung vào lĩnh vực bệnh tôm. Nhiệm vụ của bạn là cung cấp bối cảnh ngắn gọn, chính xác cho một đoạn văn bản từ báo cáo hoặc tài liệu chuyên môn về bệnh tôm.

        Đây là tài liệu:
        <document>
        {document}
        </document>

        Đây là đoạn văn cần đặt vào bối cảnh:
        <chunk>
        {chunk}
        </chunk>

        Hãy cung cấp bối cảnh ngắn gọn (2-3 câu) cho đoạn này, tuân theo các hướng dẫn sau:
        1. Xác định nội dung chính hoặc chỉ số được thảo luận (ví dụ: triệu chứng, nguyên nhân, phương pháp phòng ngừa, điều trị).
        2. Đề cập đến mốc thời gian hoặc so sánh liên quan (nếu có).
        3. Nếu áp dụng, nêu rõ cách thông tin này liên quan đến sức khỏe tổng thể của tôm, chiến lược phòng bệnh, hoặc tác động kinh tế.
        4. Bao gồm số liệu hoặc chi tiết quan trọng để bổ sung ngữ cảnh cho đoạn văn (nếu có).
        5. Không sử dụng các cụm từ như "Đoạn văn này bàn về", "Phần này cung cấp", "Đoạn văn này mô tả". Thay vào đó, trực tiếp cung cấp bối cảnh.

        Cung cấp bối cảnh ngắn gọn, súc tích để đặt đoạn văn này trong tổng thể tài liệu nhằm cải thiện khả năng tìm kiếm và truy xuất thông tin. Trả lời chỉ bằng bối cảnh ngắn gọn và không thêm gì khác.

        Bối cảnh:
        """)
        messages = prompt.format_messages(document=document, chunk=chunk)
        response = self.llm.invoke(messages)
        return response.content

    def create_vectorstores(self, chunks: List[Document]) -> FAISS:
        """
        Create a vector store for the given chunks.
        """
        return FAISS.from_documents(chunks, self.embeddings)

    def create_bm25_index(self, chunks: List[Document]) -> BM25Okapi:
        """
        Create a BM25 index for the given chunks.
        """
        tokenized_chunks = [chunk.page_content.split() for chunk in chunks]
        return BM25Okapi(tokenized_chunks)

    def create_retrievers(self, chunks: List[Document]):
        """
        Create vector and BM25 retrievers from document chunks.

        Args:
            chunks (List[Document]): Processed document chunks
        """
        # Create vector store retriever
        vector_store = FAISS.from_documents(chunks, self.embeddings)
        self.vector_retriever = vector_store.as_retriever(search_kwargs={"k": 5})

        # Create BM25 retriever
        self.bm25_retriever = BM25Retriever.from_documents(chunks)
        self.bm25_retriever.k = 5

        # Create ensemble retriever
        self.ensemble_retriever = EnsembleRetriever(
            retrievers=[self.vector_retriever, self.bm25_retriever],
            # Optional: Customize weights if needed
            weights=[0.5, 0.5]
        )

    def retrieve_documents(self, query: str) -> List[Document]:
        """
        Retrieve documents using the ensemble retriever.

        Args:
            query (str): Search query

        Returns:
            List of retrieved documents
        """
        # Ensure retrievers are created
        if self.ensemble_retriever is None:
            raise ValueError("Retrievers not initialized. Call create_retrievers() first.")

        # Retrieve documents
        return self.ensemble_retriever.invoke(query)


    @staticmethod
    def generate_cache_key(document: str) -> str:
        """
        Generate a cache key for a document.
        """
        return hashlib.md5(document.encode()).hexdigest()

    def add_to_conversation_history(self, query: str, response: str):
        """
        Add interaction to conversation history.

        Args:
            query (str): User's query
            response (str): System's response
        """
        # Add current interaction to history
        self.conversation_history.append({
            'query': query,
            'response': response
        })

        # Trim history if it exceeds max_history
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history:]
