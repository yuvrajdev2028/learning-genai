from dotenv import load_dotenv
load_dotenv()


# Step 1: Fetch pdf from path
from pathlib import Path

pdf_path = Path(__file__).parent / "constitution_of_india.pdf"

# Step 2: Load the pdf in python program (page by page)
from langchain_community.document_loaders import PyMuPDFLoader

loader = PyMuPDFLoader(file_path=pdf_path)
docs = loader.load()

print("Number of pages in given pdf: ",len(docs))
# print(docs[27])

# Step 3: Chunking using document splitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 800,
    chunk_overlap = 200
)

chunks = text_splitter.split_documents(documents=docs)

print("Type of chunks: ", type (chunks)) # <class 'list'>
print("Type of chunk: ", type (chunks[0])) # <class 'langchain_core.documents.base.Document'>
print("Number of chunks: ",len(chunks)) # 1376
print("One chunk: ", chunks[100]) # page_content='......' metadata={'producer': '', 'creator', ......}

# Step 4: Vector Embeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore

embedding_model = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2-preview"
)

vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name='rag_learning'
)

print("Indexing of Documents complete.")