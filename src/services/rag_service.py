import time
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from src.core.factories import ModelFactory
from src.vectorstore.database import VectorDatabaseRepository
from src.config.config_parser import settings
from src.logging.logger import logger

class RAGService:
    """Business Logic: يجيب السياق من FAISS ويولد رد بالـ LLM."""

    def __init__(self):
        self.repo = VectorDatabaseRepository()
        self.llm = ModelFactory.get_llm()
        self.template = """أجب على سؤال العميل باستخدام السياق التالي فقط:
{context}

سؤال العميل:
{question}

الرد:"""
        self.prompt = PromptTemplate.from_template(self.template)

    def _format_docs(self, docs):
        return "\n\n".join(d.page_content for d in docs)

    def answer_ticket(self, customer_ticket: str) -> dict:
        start_time = time.time()
        logger.info(f"Processing ticket: {customer_ticket[:50]}...")

        vectorstore = self.repo.load_index()
        retriever = vectorstore.as_retriever(search_kwargs={"k": settings.k_retrieval})
        retrieved_chunks = retriever.invoke(customer_ticket)

        rag_chain = (
            {"context": retriever | self._format_docs, "question": RunnablePassthrough()}
            | self.prompt | self.llm
        )
        ai_message = rag_chain.invoke(customer_ticket)
        response_text = getattr(ai_message, "content", str(ai_message))

        usage = getattr(ai_message, "usage_metadata", None) or {}
        prompt_tokens = usage.get("input_tokens", 0)
        completion_tokens = usage.get("output_tokens", 0)
        total_tokens = usage.get("total_tokens", prompt_tokens + completion_tokens)

        elapsed = round(time.time() - start_time, 2)
        logger.info(f"RAG answer generated in {elapsed}s.")

        return {
            "ticket": customer_ticket,
            "response": response_text,
            "sources_count": len(retrieved_chunks),
            "execution_time_seconds": elapsed,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens
        }