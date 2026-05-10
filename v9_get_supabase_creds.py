import pexpect
import os
from dotenv import load_dotenv

load_dotenv()
ZIMA_HOST = os.getenv("ZIMA_HOST")
ZIMA_USER = os.getenv("ZIMA_USER")
ZIMA_PASS = os.getenv("ZIMA_PASS")
import sys

def get_supabase_creds():
    child = pexpect.spawn(f'ssh {ZIMA_USER}@{ZIMA_HOST}', encoding='utf-8', timeout=60)
    child.expect('password: ')
    child.sendline(ZIMA_PASS)
    child.expect(r'\$')
    
    # Read the .env file and grep for credentials
    child.sendline('grep -E "DASHBOARD_USERNAME|DASHBOARD_PASSWORD" /mnt/external_hdd/supabase/docker-compose.yml')
    child.expect(r'\$')
    print("Checking docker-compose for dashboard vars:")
    print(child.before)
    
    child.sendline('grep -E "DASHBOARD_USERNAME|DASHBOARD_PASSWORD" /mnt/external_hdd/supabase/.env')
    child.expect(r'\$')
    print("Checking .env for dashboard vars:")
    print(child.before)

if __name__ == "__main__":
    get_supabase_creds()
