# config.py
# Store all sensitive API keys and credentials here

# WooCommerce API credentials
WOOCOMMERCE_CK = "ck_638a06f75cc259b80e76c6524a97036dce0c981d"
WOOCOMMERCE_CS = "cs_fcbfd7dc032263a3c76d52d7a906f3cf8ad83d86"

# Gemini API key
# GEMINI_API_KEY = "AIzaSyCFcNu1C1aMKB6iNhEuVEoFGRWcsBAiy44" #zk
GEMINI_API_KEY = "AIzaSyBel_RBd1MwSoH5PoWPFOZVWqZKXq43OTM" #dev

# Database configurations
DB_NAME="postgres"
DB_PASS="ZPRaAkQmWbEX6EZq"

# Supabase connection (current - may need fixing)
# PGVECTOR_DB_URL = "postgresql://postgres:ZPRaAkQmWbEX6EZq@db.qcfdlzwhqntotebycnwl.supabase.co:5432/postgres"
# PGVECTOR_DB_URL = "postgresql+psycopg://postgres:ZPRaAkQmWbEX6EZq@db.qcfdlzwhqntotebycnwl.supabase.co:5432/postgres"

#Transaction pooler
PGVECTOR_DB_URL = "postgresql+psycopg://postgres.qcfdlzwhqntotebycnwl:ZPRaAkQmWbEX6EZq@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"

# Alternative Supabase URL format (if the above doesn't work)
# PGVECTOR_DB_URL = "postgresql+psycopg://postgres.qcfdlzwhqntotebycnwl:ZPRaAkQmWbEX6EZq@aws-0-ap-south-1.pooler.supabase.com:5432/postgres"

# Local PostgreSQL (if you want to use local database)
# PGVECTOR_DB_URL = "postgresql://postgres:password@localhost:5432/postgres" 
