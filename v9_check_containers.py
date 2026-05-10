import pexpect
import os
from dotenv import load_dotenv

load_dotenv()
ZIMA_HOST = os.getenv("ZIMA_HOST")
ZIMA_USER = os.getenv("ZIMA_USER")
ZIMA_PASS = os.getenv("ZIMA_PASS")
import sys

def check_containers():
    child = pexpect.spawn(f'ssh {ZIMA_USER}@{ZIMA_HOST}', encoding='utf-8', timeout=60)
    
    child.expect('password: ')
    child.sendline(ZIMA_PASS)
    child.expect(r'\$')
    
    child.sendline('sudo docker ps -a | grep supabase')
    child.expect(r'\$')
    print("Active/Exited Supabase containers:")
    print(child.before)
    
    child.sendline('cd /mnt/external_hdd/supabase && sudo docker compose logs db | tail -n 20')
    child.expect(r'\$')
    print("DB logs:")
    print(child.before)

if __name__ == "__main__":
    check_containers()
