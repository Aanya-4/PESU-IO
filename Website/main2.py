import re
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.jinaai import JinaEmbedding
from llama_index.embeddings.cohere import CohereEmbedding
from llama_index.llms.groq import Groq
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
import os
from dotenv import load_dotenv
import requests
from pathlib import Path

load_dotenv()

# Configure the embedding model and LLM 
# Uncomment and use this if JinaEmbedding gives you an error
# Settings.embed_model = CohereEmbedding(
#     api_key=os.getenv("COHERE_API_KEY"),
#     model_name="embed-english-v3.0",
#     input_type="search_query"
# )

# Configure the embedding model and LLM
Settings.embed_model = JinaEmbedding(
    api_key=os.getenv("JINA_API_KEY"),
    model="jina-embeddings-v3",
    task="retrieval.passage",  # choose `retrieval.passage` to get passage embeddings
)

Settings.llm = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="gemma-7b-it",
    temperature=0.7
)

def sanitize_filename(filename):
    # Replace any invalid characters with underscores
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def create_rag_system(data_dir="./web_data"):
    # Initialize Qdrant client (runs locally by default)
    client = QdrantClient(path="./qdrant_web_data")
    
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

def fetch_and_save_webpage(url: str, output_dir: str = "./web_data") -> str:
    """Fetch webpage content and save as markdown"""
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Get markdown content from r.jina.ai
    response = requests.get(f"https://r.jina.ai/{url}")
    if response.status_code != 200:
        raise Exception(f"Failed to fetch content: {response.status_code}")
    
    # Create a safe filename from URL
    filename = sanitize_filename(url) + ".md"
    filepath = os.path.join(output_dir, filename)
    
    # Save content to file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(response.text)
    
    return filepath

def main():
    # Get URL from user
    url = input("Enter the URL to analyze: ")
    
    # Fetch and save webpage content
    filepath = fetch_and_save_webpage(url)
    
    # Initialize the RAG system with web_data directory
    query_engine = create_rag_system("./web_data")
    
    # Define the new set of questions
    questions = [
        "Explain the concept of generative AI and discuss its key differences from traditional AI approaches.",
        "What is the impact of transformers on the development of generative AI.",
        "Analyze the ethical concerns surrounding generative AI.",
        "Provide examples of how generative AI can be applied in fields like finance, healthcare, and manufacturing, while also considering its limitations.",
        "Whar are hallucinations and why do they occur.",
        "Compare and contrast the functionalities of popular generative AI tools such as ChatGPT, Dall-E, and Google Gemini.",
        "Examine the role of large language models (LLMs).",
        "Explore the potential of generative AI in enhancing creativity and innovation.",
        "What is transformer architecture?.",
        "Explain the concept of 'attention' in the context of transformer architecture. ",
        "How can generative ai be misued?",
        "Describe how attention helps improve the performance of generative AI models.",
        "What are the latest advancements, emerging trends, and potential future directions.",
        "Will it replace jobs?",
        "Discuss the importance of responsible AI development and deployment in the context of generative AI.",
        "Analyze the impact of generative AI on traditional media and entertainment industries. ",
        "Explore the potential of generative AI in personalized education and learning. Discuss how it can be used to create tailored learning experiences and provide individualized support.",
        "Will it affect the privacy?",
        "Examine the role of generative AI in fostering greater accessibility to creative tools and resources.",
        "Explore the potential of generative AI to bridge the gap between human and machine intelligence."
    ]
    
    # Create a Markdown file to save all responses
    output_filepath = "./responses/answers.md"
    Path("./responses").mkdir(parents=True, exist_ok=True)

    with open(output_filepath, "w", encoding="utf-8") as output_file:
        for question in questions:
            response = query_rag(query_engine, question)

            # Write the question and response to the Markdown file
            output_file.write(f"# Question:\n{question}\n\n# Answer:\n{response}\n\n---\n")

            print(f"Response for question saved: {question[:50]}...")  # Print the first 50 characters of the question

    print(f"All responses saved to: {output_filepath}")

if __name__ == "__main__":
    main()



