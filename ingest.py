# ingest.py

from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader, PDFMinerLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter 
from langchain_huggingface import HuggingFaceEmbeddings 
from langchain.vectorstores import Chroma 
from constants import persist_directory, CHROMA_SETTINGS
import os 

def main():
    documents = []
    for root, dirs, files in os.walk("docs"):
        for file in files:
            if file.endswith(".pdf"):
                print(f"Loading file: {file}")
                loader = PyPDFLoader(os.path.join(root, file))
                documents.extend(loader.load())
    
    print("Splitting into chunks")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    texts = text_splitter.split_documents(documents)

    # Create embeddings
    print("Loading sentence transformers model")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # Create vector store with new Chroma client configuration
    print(f"Creating embeddings. May take some minutes...")
    # load it into Chroma
   # save to disk
    db2 = Chroma.from_documents(texts, embeddings, persist_directory="./db")
    #docs = db2.similarity_search("text")
# load from disk
    db3 = Chroma(persist_directory="./db", embedding_function=embeddings)
    while True:
    # Prompt user for input
        user_input = input("Enter a query (or '1' to exit): ")

    # Exit loop if user inputs '1'
        if user_input == '1':
            break

    # Perform similarity search
        docs = db3.similarity_search(user_input)

    # Print the content of the first document (assuming docs[0] exists)
        if docs:
            print(docs[0].page_content)
        else:
            print("No documents found for the query.")


if __name__ == "__main__":
    main()
