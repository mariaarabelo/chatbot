# Imports
from langchain_community.document_loaders import UnstructuredPDFLoader, TextLoader, UnstructuredWordDocumentLoader
from langchain_openai import OpenAIEmbeddings
from langchain_openai.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
import pickle
from dotenv import load_dotenv
import os

vector_store = None

# Load environment variables from .env file
load_dotenv()

# Set the API Key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
embeddings_model = OpenAIEmbeddings()

# Initialize the OpenAI model with LangChain
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

# Paths to PDF files with recipes
files = [
    'Arroz de polvo _ Receitas _ Pingo Doce.pdf',
    'Arroz-doce _ Receitas _ Pingo Doce.pdf',
    'Bacalhau à Brás com legumes _ Receitas _ Pingo Doce.pdf',
    'Arroz de pato _ Receitas _ Pingo Doce.pdf',
    'Bacalhau à Gomes de Sá _ Receitas _ Pingo Doce.pdf',
    'Empadão de alheira com cogumelos e agrião _ Receitas _ Pingo Doce.pdf',
    'Francesinha _ Receitas _ Pingo Doce.pdf',
    'Pastel de nata _ Receitas _ Pingo Doce.pdf',
    'Polvo braseado com arroz do mesmo _ Receitas _ Pingo Doce.pdf',
    'Tigeladas de abóbora com nozes _ Receitas _ Pingo Doce.pdf',
    'Tripas à moda do Porto _ Receitas _ Pingo Doce.pdf',
    'BoloBolacha.txt',
    'CaldoVerde.docx'
]

def read_file(file_path: str) -> str:
    """Reads the content of a given file based on its format."""
    if file_path.endswith(".pdf"):
        loader = UnstructuredPDFLoader(file_path)
    elif file_path.endswith(".txt"):
        loader = TextLoader(file_path)
    elif file_path.endswith(".docx"):
        loader = UnstructuredWordDocumentLoader(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_path}")
    
    docs = loader.load()
    return docs[0].page_content  # Extract text content

def build_faiss_index():
    global vector_store 
    
    all_documents = []

    for file in files:
        content = read_file('recipes/' + file)
        all_documents.append(content)

    print(f"📄 Total documents read: {len(all_documents)}")

    # Split into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.create_documents(all_documents)
    print(f"📄 Total chunks created: {len(chunks)}") 

    # Convert text chunks into vector embeddings and store in FAISS
    vector_store = FAISS.from_documents(chunks, embeddings_model)

    # Save FAISS index to disk
    vector_store.save_local("faiss_index")
    print("✅ FAISS index saved successfully.")

# Function to handle conversation logic
def chat_with_llm(user_input, chat_history=None):
    """Handles a single interaction with the LLM using FAISS for retrieval."""

    # Retrieve relevant text chunks from FAISS
    search_results = vector_store.similarity_search(user_input, k=3)  # Get top 3 relevant chunks
    retrieved_context = "\n\n".join([doc.page_content for doc in search_results])

    # Construct system message with FAISS retrieved context
    system_message_with_context = {
        "role": "system",
        "content": f"""
        You are a culinary expert specializing in Portuguese cuisine. 
        Use the following relevant recipe details to answer the user's question:

        {retrieved_context}

        If the information is not relevant, rely on your general knowledge of Portuguese cuisine.
        Don't answer questions about any other topic.
        """
    }
    
    if chat_history is None or not chat_history:
        chat_history = [system_message_with_context]
        
    chat_history.append({"role": "user", "content": user_input})

    # Generate response with enriched context
    response = llm.invoke(chat_history)
    
    chat_history.append({"role": "assistant", "content": response.content})

    return chat_history  # Return updated chat history
