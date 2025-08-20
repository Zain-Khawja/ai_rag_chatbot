"""
Database setup script to initialize tables for chat logging
"""
import psycopg2
from lib.config import PGVECTOR_DB_URL
from lib.chat_logger import ChatLogger

def setup_database():
    """
    Set up the PostgreSQL database with required tables
    """
    print("Setting up database...")
    
    try:
        # Create chat_logs table
        chat_logger = ChatLogger(PGVECTOR_DB_URL)
        chat_logger.ensure_table_exists()
        print("Successfully created chat_logs table!")
        
    except Exception as e:
        print(f"Error setting up database: {e}")

if __name__ == "__main__":
    setup_database()
