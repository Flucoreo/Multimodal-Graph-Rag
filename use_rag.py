"""
Using the Rag
"""

import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_redis import RedisVectorStore
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough


load_dotenv()
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}"


# instantiate a connection to a local llm
llm = ChatOpenAI (
    model="local-model",
    openai_api_key="dummy-key",
    openai_api_base="http://localhost:1234/v1",
    temperature=0.7,
)

embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5")

rds = RedisVectorStore.from_existing_index(
    embedding=embeddings,
    index_name="langchain_ex",
    redis_url=REDIS_URL,
)


def chat_with_llm():
    """
    Chat with the local llm
    """

    response = llm.invoke("Explain what LangChain is in one sentence.")
    print(response.content)


def view_vector_results():

    res = rds.similarity_search_with_score(query="veggie meat", k=4)

    for doc in res:
        text, similarity = doc
        print(text.page_content)


# def format_docs(docs):
#     context = ""

#     for doc in docs:
#         text, similarity = doc
#         context += doc.page_content
#         context += "\n\n"

#     return context    


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def llm_with_rag():

    prompt_template = """
        You are a helpful assistant who is good at analyzing source information and answering questions.
        Use the following pieces of context to answer the user question at the end. 
        If you don't know the answer, say that you don't know, don't try to make up an answer.
        Use three sentences maximum and keep the answer concise.

        Context:
        ---------
        {context}
        ---------
        Question:
        {question}
        Answer:
    """

    prompt = ChatPromptTemplate.from_template(prompt_template)

    rag_chain = (
        {
            "context": rds.as_retriever() | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    query = "What was Nike's revenue last year compared to this year??"
    rag_chain.invoke(query)


if __name__ == "__main__":
    chat_with_llm()
