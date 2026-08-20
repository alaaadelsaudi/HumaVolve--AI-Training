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

    def _extract_text(self, raw_content):
        """يحول محتوى الرد لصيغة نص عادي، بغض النظر عن شكل رد الموديل."""
        if isinstance(raw_content, str):
            return raw_content
        elif isinstance(raw_content, list):
            text_parts = []
            for block in raw_content:
                if isinstance(block, dict) and block.get("type") == "text":
                    text_parts.append(block.get("text", ""))
                elif isinstance(block, str):
                    text_parts.append(block)
            return "".join(text_parts)
        else:
            return str(raw_content)

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
        raw_content = getattr(ai_message, "content", ai_message)
        response_text = self._extract_text(raw_content)

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