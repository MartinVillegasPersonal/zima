import pexpect
import os
from dotenv import load_dotenv

load_dotenv()
ZIMA_HOST = os.getenv("ZIMA_HOST")
ZIMA_USER = os.getenv("ZIMA_USER")
ZIMA_PASS = os.getenv("ZIMA_PASS")
import sys

def enable_vector():
    child = pexpect.spawn(f'ssh {ZIMA_USER}@{ZIMA_HOST}', encoding='utf-8', timeout=60)
    child.logfile = sys.stdout
    child.expect('password: ')
    child.sendline(ZIMA_PASS)
    child.expect(r'\$')
    
    print("Enabling pgvector...")
    child.sendline('sudo docker exec -i supabase-db psql -U postgres -c "CREATE EXTENSION IF NOT EXISTS vector;"')
    child.expect(r'\$')
    
    print("Verifying extensions again...")
    child.sendline('sudo docker exec -i supabase-db psql -U postgres -c "SELECT extname FROM pg_extension WHERE extname = \'vector\';"')
    child.expect(r'\$')

if __name__ == "__main__":
    enable_vector()
