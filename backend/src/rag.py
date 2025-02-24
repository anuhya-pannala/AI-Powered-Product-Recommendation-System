import os
from langchain_openai import OpenAIEmbeddings
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
USE_OPENAI = os.getenv("USE_OPENAI", "False").lower() == "true"
FAISS_INDEX_FILE = "faiss_index"
# USE_OPENAI = True

# Load FAISS Vector Store
# vector_store = FAISS.load_local(FAISS_INDEX_FILE, 
#                                 OpenAIEmbeddings() if USE_OPENAI else OllamaEmbeddings())
vector_store = FAISS.load_local(
    FAISS_INDEX_FILE,
    OpenAIEmbeddings() if USE_OPENAI else OllamaEmbeddings(),
    allow_dangerous_deserialization=True
)

# Initialize LLM dynamically
llm = ChatOpenAI(api_key=OPENAI_API_KEY, model_name="gpt-4-turbo") if USE_OPENAI\
    else ChatGroq(groq_api_key=GROQ_API_KEY, model_name="Llama3-8b-8192")

# Define the retrieval prompt
prompt = ChatPromptTemplate.from_template(
    """
    INSTRUCTIONS:
    Answer the users question using the context text below.
    Keep your answer ground in the facts of the context.
    If the context doesn't contain the facts to answer the question return 
        - "I don't have such information"

    <context>
    {context}
    <context>

    <question>
    {input}
    <question>
    """
)

def retrieve_and_generate(query):
    """Retrieve relevant data from FAISS and generate a response"""
    document_chain = create_stuff_documents_chain(llm, prompt)
    retriever = vector_store.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    response = retrieval_chain.invoke({'input':query})

    print("=============== Response ==============")
    print(response)
    return response['answer']


# Define the prompt for augmenting product description.
product_prompt = ChatPromptTemplate.from_template(
    """
    INSTRUCTIONS:
    Generate a 2-3 line augmented product description based on the product name\
        provided below.
    Use the context text to enhance the description with any relevant details.
    If no useful context is available, return "Insufficient product\
        information to augment description."

    <context>
    {context}
    <context>

    <question>
    Describe the product: {input}
    <question>
    """
)

def retrieve_product_context(product_name):
    """Retrieve relevant product details from FAISS based on product name"""
    retriever = vector_store.as_retriever()

    # Search using the product name as the query
    retrieved_docs = retriever.get_relevant_documents(product_name)

    # print("======== Retrieved docs =========")
    # print(retrieved_docs)

    if not retrieved_docs:
        return None  # No relevant documents found

    # Convert retrieved text into LangChain `Document` objects
    context_documents = [Document(page_content=doc.page_content,
                                  metadata=doc.metadata) for doc in retrieved_docs]

    return context_documents

def generate_augmented_description(product_name):
    """Generate a product description"""
    context_documents = retrieve_product_context(product_name)

    if not context_documents:
        return "I couldn't find relevant details for this product."

    # Create the chain with refined prompt
    document_chain = create_stuff_documents_chain(llm, product_prompt)
    retrieval_chain = create_retrieval_chain(vector_store.as_retriever(), document_chain)

    response = retrieval_chain.invoke({'input': product_name, 'context': context_documents})

    print("=============== Augmented Product Description ==============")
    print(response)
    return response['answer']
