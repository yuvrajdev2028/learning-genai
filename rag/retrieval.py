from dotenv import load_dotenv
load_dotenv()

# Step 1: fetch embedding model and vector db
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore

embedding_model = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2-preview"
)

vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name='rag_learning',
    embedding=embedding_model
)

# Step 2: Take user query as input
user_query = input("Ask something about Constitution of India: ")

# Similarity search to fetch relevant chunks from vector db

search_results = vector_db.similarity_search(query=user_query)

# Creating context and inserting it in system prompt

context = "\n\n\n".join(
    [f"Page Contents: {result.page_content}\nPage Number: {result.metadata['page']}\nFile Location:{result.metadata['source']}"
    for result in search_results])

SYSTEM_PROMPT = f"""
    You are a helpful AI assistant who answers user query based on the available 
    context retrieved from a PDF file along with page_contents and page number.

    You should only answer the user based on the following context and navigate 
    user to open the right page number to know more.

    If you are unable to find the answer in the given context then simply apologize
    and tell the user that you do not have enough context.

    Context:
    {context}
"""

# Simply send completion request to ai client

from google import genai
import os

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

response = client.models.generate_content(
    model='gemini-3.1-flash-lite-preview',
    contents=[
        {
            "role": "user",
            "parts": [{"text":user_query}]
        }
    ],
    config=genai.types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT
    )
)

print("LAWBOT: ",response.text);