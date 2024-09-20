import argparse
import os
import shutil

from langchain_core.tools import tool
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from tools.getembedding import get_embedding_function
#from testRag import test_question
from tools.interface import CHROMA_PATH, query_rag
from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader

from pathlib import Path
from pydantic import BaseModel, Field
#__import__('pysqlite3')
import sys
#sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from langchain_community.vectorstores.chroma import Chroma
CHROMA_PATH = "chroma"
DATA_PATH = "data"
class RetrievalAugmentedGeneration(BaseModel):
    filename: str = Field(
        description="the file name in 'data' folder that is most appropriate for the task requested"
    )
    context: str = Field(
        description="the user input that was given"
    )
@tool("RAG", args_schema=RetrievalAugmentedGeneration)
def RAG_TOOL(filename, context: str) -> str:
    """When you get a request for info that may be stored in a pdf in file 'data' you use this tool to retrieve info from the appropriate pdf file"""
    print("This is the file utilized: " + filename)
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    args = parser.parse_args()
    if args.reset:
        print("✨ Clearing Database")
        clear_database()
    # Create (or update) the data store.
    documents = load_documents()
    chunks = split_documents(documents)
    add_to_chroma(chunks)
    query_rag(context)

    

        
            
        
   ##    documents = load_documents()

def load_documents():
  document_loader = PyPDFDirectoryLoader('data')
  return document_loader.load()


   
def add_to_chroma(chunks: list[Document]):
  # Load the existing database.

    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=get_embedding_function()
    )
    

    # Calculate Page IDs.
    chunks_with_ids = calculate_chunk_ids(chunks)

    # Add or Update the documents.
    existing_items = db.get(include=[])  # IDs are always included by default
    print(os.getenv("OPENAI_API_KEY"))
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")
    
    # Only add documents that don't exist in the DB.
    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
          new_chunks.append(chunk)
    
    if len(new_chunks):
        print(f"Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids) #error
        db.persist()
    else:
        print("No new documents to add")
        

def calculate_chunk_ids(chunks):

# Page Source : Page Number : Chunk Index
    
    last_page_id = None
    current_chunk_index = 0
    
    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"
    
        # If the page ID is the same as the last one, increment the index.
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0
    
        # Calculate the chunk ID.
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id
    
        # Add it to the page meta-data.
        chunk.metadata["id"] = chunk_id
    
    return chunks


def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=128,
        chunk_overlap=64,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)


def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)





