import pexpect
import os
from dotenv import load_dotenv

load_dotenv()
ZIMA_HOST = os.getenv("ZIMA_HOST")
ZIMA_USER = os.getenv("ZIMA_USER")
ZIMA_PASS = os.getenv("ZIMA_PASS")
import sys

def validate_db():
    child = pexpect.spawn(f'ssh {ZIMA_USER}@{ZIMA_HOST}', encoding='utf-8', timeout=60)
    child.logfile = sys.stdout
    child.expect('password: ')
    child.sendline(ZIMA_PASS)
    child.expect(r'\$')
    
    # Connect to postgres container and list tables
    print("Checking tables in 'postgres' database...")
    child.sendline('sudo docker exec -it supabase-db psql -U postgres -c "\\dt"')
    child.expect(r'\$')
    
    # Check pgvector
    print("Checking pgvector extension...")
    child.sendline('sudo docker exec -it supabase-db psql -U postgres -c "SELECT * FROM pg_extension WHERE extname = \'vector\';"')
    child.expect(r'\$')
    
    print("Validation finished.")

if __name__ == "__main__":
    validate_db()
