import pexpect
import os
from dotenv import load_dotenv

load_dotenv()
ZIMA_HOST = os.getenv("ZIMA_HOST")
ZIMA_USER = os.getenv("ZIMA_USER")
ZIMA_PASS = os.getenv("ZIMA_PASS")
import sys

def fix_kong_conflict():
    child = pexpect.spawn(f'ssh {ZIMA_USER}@{ZIMA_HOST}', encoding='utf-8', timeout=120)
    child.logfile = sys.stdout
    child.expect('password: ')
    child.sendline(ZIMA_PASS)
    child.expect(r'\$')
    
    # 1. Stop Portainer
    print("Stopping Portainer to free port 8000...")
    child.sendline('sudo docker stop portainer')
    i = child.expect([r'password for {ZIMA_USER}:', r'\$'])
    if i == 0:
        child.sendline(ZIMA_PASS)
        child.expect(r'\$')
    
    # 2. Try starting Kong again
    print("Starting Kong...")
    child.sendline('cd /mnt/external_hdd/supabase && sudo docker compose up -d kong')
    child.expect(r'\$')
    
    # 3. Check logs
    child.sendline('sudo docker logs supabase-kong')
    child.expect(r'\$')
    
    # 4. Check status
    child.sendline('sudo docker ps | grep kong')
    child.expect(r'\$')

if __name__ == "__main__":
    fix_kong_conflict()
