import os
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://wvattyjoisrgyrxpchkp.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind2YXR0eWpvaXNyZ3lyeHBjaGtwIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0MjE4NDY4MiwiZXhwIjoyMDU3NzYwNjgyfQ.CdxDo43AQBmygF2r7Fq497JtdBAAzxwINuUqxVk8ezQ")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
