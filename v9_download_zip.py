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
    
    # Install unzip if not present
    child.sendline('sudo apt-get update && sudo apt-get install -y unzip')
    child.expect('password for {ZIMA_USER}:', timeout=10)
    child.sendline(ZIMA_PASS)
    child.expect(r'\$', timeout=60)
    
    # Download ZIP
    child.sendline('cd /mnt/external_hdd && sudo rm -rf supabase_tmp.zip supabase_docker-master')
    child.expect(r'\$')
    
    child.sendline('wget https://github.com/supabase/docker/archive/refs/heads/main.zip -O supabase_tmp.zip')
    child.expect(r'\$', timeout=60)
    
    # Unzip
    child.sendline('unzip supabase_tmp.zip')
    child.expect(r'\$', timeout=60)
    
    # Rename folder to supabase
    child.sendline('sudo rm -rf supabase && mv docker-main supabase')
    child.expect(r'\$')
    
    # Cleanup
    child.sendline('rm supabase_tmp.zip')
    child.expect(r'\$')
    
    print("Supabase downloaded and unzipped.")

if __name__ == "__main__":
    download_supabase()
