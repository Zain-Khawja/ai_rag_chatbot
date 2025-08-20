"""
Chat Logger Module for storing chat conversations in PostgreSQL database
"""
import datetime
import psycopg2
from lib.config import PGVECTOR_DB_URL

class ChatLogger:
    """
    Class for logging chat interactions to PostgreSQL database
    """
    def __init__(self, db_url=PGVECTOR_DB_URL):
        # Convert connection string format if needed
        if db_url.startswith("postgresql+psycopg://"):
            self.db_url = db_url.replace("postgresql+psycopg://", "postgresql://")
        else:
            self.db_url = db_url
        self.ensure_table_exists()
    
    def ensure_table_exists(self):
        """Create the chat_logs table if it doesn't exist"""
        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor() as cur:
                    # First check if table exists
                    cur.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_schema = 'public' 
                        AND table_name = 'chat_logs'
                    );
                    """)
                    table_exists = cur.fetchone()[0]
                    
                    if not table_exists:
                        cur.execute("""
                        CREATE TABLE IF NOT EXISTS chat_logs (
                            id SERIAL PRIMARY KEY,
                            user_id VARCHAR(255) NOT NULL,
                            session_id VARCHAR(255),
                            question TEXT NOT NULL,
                            answer TEXT NOT NULL,
                            validation_status VARCHAR(50),
                            attempts INT DEFAULT 1,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        );
                        """)
                        conn.commit()
                        print("Chat logs table created successfully")
                    else:
                        print("Chat logs table already exists")
        except Exception as e:
            print(f"Error creating chat logs table: {e}")
    
    def log_chat(self, user_id, question, answer, session_id=None, validation_status="approved", attempts=1):
        """
        Log a chat interaction to the database
        
        Args:
            user_id (str): User identifier
            question (str): User's question
            answer (str): AI's response
            session_id (str, optional): Session identifier
            validation_status (str, optional): Validation status of the response
            attempts (int, optional): Number of attempts to generate a valid response
        
        Returns:
            bool: True if logging successful, False otherwise
        """
        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor() as cur:
                    # Match the existing column names in the table
                    cur.execute("""
                    INSERT INTO chat_logs 
                    (user_id, session_id, user_question, bot_response, validation_status, attempts, created_at) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (
                        user_id, 
                        session_id, 
                        question, 
                        answer, 
                        validation_status, 
                        attempts,
                        datetime.datetime.now()
                    ))
                    conn.commit()
                    print(f"Chat log saved for user {user_id} with session {session_id}")
                    return True
        except Exception as e:
            print(f"Error logging chat: {e}")
            return False
    
    def get_user_chat_history(self, user_id, limit=10):
        """
        Retrieve chat history for a specific user
        
        Args:
            user_id (str): User identifier
            limit (int, optional): Maximum number of records to retrieve
        
        Returns:
            list: List of chat log records
        """
        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                    SELECT id, user_id, session_id, user_question, bot_response, validation_status, 
                           attempts, created_at
                    FROM chat_logs
                    WHERE user_id = %s
                    ORDER BY created_at DESC
                    LIMIT %s
                    """, (user_id, limit))
                    
                    columns = [desc[0] for desc in cur.description]
                    result = [dict(zip(columns, row)) for row in cur.fetchall()]
                    return result
        except Exception as e:
            print(f"Error retrieving chat history: {e}")
            return []
    
    def get_session_chat_history(self, session_id, limit=10):
        """
        Retrieve chat history for a specific session
        
        Args:
            session_id (str): Session identifier
            limit (int, optional): Maximum number of records to retrieve
        
        Returns:
            list: List of chat log records
        """
        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                    SELECT id, user_id, session_id, user_question, bot_response, validation_status, 
                           attempts, created_at
                    FROM chat_logs
                    WHERE session_id = %s
                    ORDER BY created_at DESC
                    LIMIT %s
                    """, (session_id, limit))
                    
                    columns = [desc[0] for desc in cur.description]
                    result = [dict(zip(columns, row)) for row in cur.fetchall()]
                    return result
        except Exception as e:
            print(f"Error retrieving session chat history: {e}")
            return []
