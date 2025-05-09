from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
import os


load_dotenv()

FAISS_INDEX_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../faiss_index"))
LLM_MODEL_NAME = "gpt-4o-mini"
EMBEDDING_MODEL_NAME = "text-embedding-3-small"

embedding = OpenAIEmbeddings( model=EMBEDDING_MODEL_NAME)
vector_store = FAISS.load_local(FAISS_INDEX_PATH, embeddings=embedding, allow_dangerous_deserialization=True)
retriever = vector_store.as_retriever(search_kwargs={"k": 3})

prompt_template = """You are an Email Wizard's Assistant. Use the following pieces of context, which are past emails, to answer the question at the end.
If you don't know the answer from the context, just say that you don't know, don't try to make up an answer.
Provide a concise answer, and if possible, quote relevant parts from the retrieved emails.
If the question is a general greeting or not answerable from the emails, respond politely.
Context:
{context}
Question: {question}
Helpful Answer:"""

QA_PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
llm = ChatOpenAI(model_name=LLM_MODEL_NAME, temperature=0.7)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=False,
    chain_type_kwargs={"prompt": QA_PROMPT},
)

def query_email_assistant(query: str) -> str:
    """Main entry point for processing a query using the RAG pipeline."""
    result = qa_chain.invoke({"query": query})
    return result["result"]
