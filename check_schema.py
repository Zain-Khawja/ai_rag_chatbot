"""
Check database schema for chat_logs table
"""
import psycopg2
from lib.config import PGVECTOR_DB_URL

def check_schema():
    """Check the schema of the chat_logs table"""
    db_url = PGVECTOR_DB_URL.replace('postgresql+psycopg://', 'postgresql://')
    
    try:
        with psycopg2.connect(db_url) as conn:
            with conn.cursor() as cur:
                # Check if table exists
                cur.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'chat_logs'
                );
                """)
                table_exists = cur.fetchone()[0]
                
                if not table_exists:
                    print("Table 'chat_logs' does not exist")
                    return
                
                # Get column information
                cur.execute("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'chat_logs';
                """)
                
                columns = cur.fetchall()
                print("Table 'chat_logs' has the following columns:")
                for col_name, data_type in columns:
                    print(f"  - {col_name} ({data_type})")
    
    except Exception as e:
        print(f"Error checking schema: {e}")

if __name__ == "__main__":
    check_schema()
