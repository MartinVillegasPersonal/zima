import pexpect
import os
from dotenv import load_dotenv

load_dotenv()
ZIMA_HOST = os.getenv("ZIMA_HOST")
ZIMA_USER = os.getenv("ZIMA_USER")
ZIMA_PASS = os.getenv("ZIMA_PASS")
import sys

def setup_keys_properly():
    child = pexpect.spawn(f'ssh {ZIMA_USER}@{ZIMA_HOST}', encoding='utf-8', timeout=120)
    child.logfile = sys.stdout
    child.expect('password: ')
    child.sendline(ZIMA_PASS)
    child.expect(r'\$')
    
    child.sendline('cd /mnt/external_hdd/supabase')
    child.expect(r'\$')
    
    # Permissions
    child.sendline('chmod +x utils/*.sh')
    child.expect(r'\$')
    
    # Password
    print("Setting DB password...")
    child.sendline('./utils/db-passwd.sh casaos')
    child.expect(r'\$')
    
    # Keys
    print("Generating keys...")
    child.sendline('./utils/generate-keys.sh')
    child.expect(r'\$')
    
    # Wait for .env to be updated
    child.sendline('sleep 2')
    child.expect(r'\$')
    
    # Read keys
    child.sendline('grep "ANON_KEY=" .env | cut -d "=" -f2')
    child.expect(r'\$')
    print("--- ANON_KEY OUTPUT START ---")
    print(child.before)
    print("--- ANON_KEY OUTPUT END ---")
    
    child.sendline('grep "SERVICE_ROLE_KEY=" .env | cut -d "=" -f2')
    child.expect(r'\$')
    print("--- SERVICE_KEY OUTPUT START ---")
    print(child.before)
    print("--- SERVICE_KEY OUTPUT END ---")

if __name__ == "__main__":
    setup_keys_properly()
