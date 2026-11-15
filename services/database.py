
import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

# Get Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SECRET_KEY = os.getenv("SUPABASE_SECRET_KEY")

# Check credentials
if not SUPABASE_URL or not SUPABASE_SECRET_KEY:
    raise ValueError("Supabase credentials are missing from .env")

# Create Supabase client
supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_SECRET_KEY
)
