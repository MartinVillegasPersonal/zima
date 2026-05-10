import pexpect
import os
from dotenv import load_dotenv

load_dotenv()
ZIMA_HOST = os.getenv("ZIMA_HOST")
ZIMA_USER = os.getenv("ZIMA_USER")
ZIMA_PASS = os.getenv("ZIMA_PASS")
import sys

def clone_supabase():
    child = pexpect.spawn(f'ssh {ZIMA_USER}@{ZIMA_HOST}', encoding='utf-8', timeout=120)
    child.logfile = sys.stdout
    
    child.expect('password: ')
    child.sendline(ZIMA_PASS)
    child.expect(r'\$')
    
    # Try cloning without prompt
    child.sendline('cd /mnt/external_hdd && sudo rm -rf supabase')
    child.expect(r'\$')
    
    child.sendline('GIT_TERMINAL_PROMPT=0 git clone --depth 1 https://github.com/supabase/docker.git supabase')
    child.expect(r'\$', timeout=120)
    
    child.sendline('ls -la /mnt/external_hdd/supabase')
    child.expect(r'\$')

if __name__ == "__main__":
    clone_supabase()
