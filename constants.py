import os 
import chromadb
from chromadb.config import Settings 
persist_directory = "db"

CHROMA_SETTINGS = {
    "chroma_db_impl": "duckdb+parquet"
}
