import pexpect
import os
from dotenv import load_dotenv

load_dotenv()
ZIMA_HOST = os.getenv("ZIMA_HOST")
ZIMA_USER = os.getenv("ZIMA_USER")
ZIMA_PASS = os.getenv("ZIMA_PASS")
import sys

def rebuild_kong():
    child = pexpect.spawn(f'ssh {ZIMA_USER}@{ZIMA_HOST}', encoding='utf-8', timeout=300)
    child.logfile = sys.stdout
    child.expect('password: ')
    child.sendline(ZIMA_PASS)
    child.expect(r'\$')
    
    # Remove the failed container
    print("Removing old kong container...")
    child.sendline('sudo docker rm -f supabase-kong')
    child.expect(r'\$')
    
    # Re-up it from compose (this will use /var/lib/docker images)
    print("Re-upping kong from compose...")
    child.sendline('cd /mnt/external_hdd/supabase && sudo docker compose up -d kong')
    child.expect(r'\$')
    
    # Check status
    child.sendline('sudo docker ps | grep kong')
    child.expect(r'\$')

if __name__ == "__main__":
    rebuild_kong()
