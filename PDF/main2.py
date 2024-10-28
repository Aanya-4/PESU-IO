from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.jinaai import JinaEmbedding
from llama_index.llms.groq import Groq
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
import os
from dotenv import load_dotenv

load_dotenv()

# Configure the embedding model and LLM
Settings.embed_model = JinaEmbedding(
    api_key=os.getenv("JINA_API_KEY"),
    model="jina-embeddings-v3",
    task="retrieval.passage",
)

Settings.llm = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="mixtral-8x7b-32768",
    temperature=0.7
)

def create_rag_system(data_dir="./data"):
    # Initialize Qdrant client (runs locally by default)
    client = QdrantClient(path="./qdrant_data")
    
    # Create Qdrant vector store
    vector_store = QdrantVectorStore(
        client=client,
        collection_name="my_documents",
        dimension=1024  # Must match embedding dimension
    )
    
    # Load documents from the specified directory
    documents = SimpleDirectoryReader(data_dir).load_data()
    
    # Create vector store index with Qdrant
    index = VectorStoreIndex.from_documents(
        documents,
        vector_store=vector_store
    )
    
    # Create query engine
    query_engine = index.as_query_engine()
    
    return query_engine

def query_rag(query_engine, question: str):
    # Query the system
    response = query_engine.query(question)
    return response

def main():
    # Initialize the RAG system
    query_engine = create_rag_system()
    
    questions = [
        "1.Discuss the concept of operator precedence in Java.",
        "2.Describe the difference between using the `&` and `&&` operators for logical AND operations in Java.",
        "3.Explain the concept of character escape codes in Java.",
        "4.How is nested `if` statements in Java used.",
        "5.Explain the use of the `%` (modulo) operator in Java.",
        "6.What is a loop in Java? Explain the different types of loops available.",
        "7.Describe the structure and operation of the `do-while` loop in Java. Explain how it differs from the `while` loop and when it is more appropriate to use.",
        "8.Explain the use of the `break` statement within a loop in Java.",
        "9.How are labels used to identify specific loops and to control the execution of `break` statements?",
        "10.Explain the concept of nested loops in Java. How are they used?",
        "11.How is an object created from a class using the `new` keyword?",
        "12.What are reference variables in Java?",
        "13.Explain the purpose of methods in Java.",
        "14.What is the use of the `return` statement?",
        "15.What is constructor overloading?",
        "16.What is an array?",
        "17.Explain the concept of two-dimensional arrays in Java. How are they declared, initialized, and accessed?",
        "18.Discuss the use of the `length` variable in Java arrays.",
        "19.Describe the use of string methods in Java. Explain how they are used to manipulate and extract information from strings, providing examples.",
        "20.Explain the concept of file operations in Java."
    ]
    
    with open("output.md", "w") as file:
        # Loop through the questions and query the system
        for question in questions:
            response = query_rag(query_engine, question)
            file.write(f"## Question: {question}\n\n**Answer:** {response}\n\n")
    
    print("Output saved to output.md")

if __name__ == "__main__":
    main()

