import pexpect
import os
from dotenv import load_dotenv

load_dotenv()
ZIMA_HOST = os.getenv("ZIMA_HOST")
ZIMA_USER = os.getenv("ZIMA_USER")
ZIMA_PASS = os.getenv("ZIMA_PASS")
import sys

def download_supabase():
    child = pexpect.spawn(f'ssh {ZIMA_USER}@{ZIMA_HOST}', encoding='utf-8', timeout=120)
    child.logfile = sys.stdout
    
    child.expect('password: ')
    child.sendline(ZIMA_PASS)
    child.expect(r'\$')
    
    # Download ZIP
    child.sendline('cd /mnt/external_hdd && sudo rm -rf supabase_tmp.zip supabase_docker-main docker-main supabase')
    i = child.expect([r'password for {ZIMA_USER}:', r'\$'])
    if i == 0:
        child.sendline(ZIMA_PASS)
        child.expect(r'\$')
    
    # Try different URLs if main.zip fails
    child.sendline('wget https://github.com/supabase/docker/archive/refs/heads/main.zip -O supabase_tmp.zip')
    child.expect(r'\$', timeout=60)
    
    # Unzip
    child.sendline('unzip supabase_tmp.zip')
    child.expect(r'\$', timeout=60)
    
    # Move and rename
    child.sendline('mv docker-main supabase')
    child.expect(r'\$')
    
    # Cleanup
    child.sendline('rm supabase_tmp.zip')
    child.expect(r'\$')
    
    print("Supabase downloaded.")

if __name__ == "__main__":
    download_supabase()
