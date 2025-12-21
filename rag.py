"""
Rag
"""

import os
from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_redis import RedisVectorStore


load_dotenv()
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")


# If SSL is enabled on the endpoint, use rediss:// as the URL prefix
REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}"

def chuncking():
    """
    Load the text and chunk it
    """

    # load the text files
    data_path = ""
    file = f"{data_path}test.txt"

    # set up the file loader
    loader = UnstructuredFileLoader(
        file, mode="single", strategy="fast"
    )

    # set up the file the text splitter to create chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=20
    )

    # create the chunks
    chunks = loader.load_and_split(text_splitter)

    print("Done preprocessing. Created", len(chunks), "chunks of the original pdf", file)
    return chunks


def embedding():
    """ 
    Intitalize the embedding model
    """

    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5")
    # model stored in .cache/hugginface/hub

    print(REDIS_URL)
    return embeddings


def store(embed, text_chunks):
    """ 
    Ccreate a redis vector store
    """

    index_name = "langchain_ex"

    # construct the vector store class from texts and metadata
    rds = RedisVectorStore.from_documents(
        text_chunks,
        embed,
        index_name=index_name,
        redis_url=REDIS_URL,
        metadata_schema=[
            {
                "name": "source",
                "type": "text"
            },
        ]
    )

    # view the number of documents stored in redis
    print("documents stored -> ", rds._index.client.dbsize())


# def search(embed):
#     """
#     Performing similarity search
#     """

#     r = RedisVectorStore.from_existing_index(
#         embedding=embed,
#         index_name="langchain_ex",
#         redis_url=REDIS_URL,
#     )

#     res = r.similarity_search_with_score(query="veggie meat", k=4)
#     for doc in res:
#         text, similarity = doc
#         print(text.page_content)


if __name__ == "__main__":
    chunks = chuncking()
    em = embedding()
    store(em, chunks)
    # search(em)

# langchain==1.2.0
# langchain-community==0.4.1
# langchain-text-splitters==1.1.0
# langchain-huggingface==1.2.0
# langchain-redis==0.2.5
# unstructured==0.18.21
# sentence-transformers==5.2.0
# youtube-transcript-api==1.2.3
# openai==2.14.0
# langchain-openai==1.1.6