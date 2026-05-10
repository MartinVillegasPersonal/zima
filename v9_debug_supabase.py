import pexpect
import os
from dotenv import load_dotenv

load_dotenv()
ZIMA_HOST = os.getenv("ZIMA_HOST")
ZIMA_USER = os.getenv("ZIMA_USER")
ZIMA_PASS = os.getenv("ZIMA_PASS")
import sys

def debug_ssh():
    child = pexpect.spawn(f'ssh {ZIMA_USER}@{ZIMA_HOST}', encoding='utf-8', timeout=60)
    child.logfile = sys.stdout
    
    i = child.expect(['password: ', 'Are you sure you want to continue connecting', pexpect.EOF, pexpect.TIMEOUT])
    if i == 1:
        child.sendline('yes')
        child.expect('password: ')
        child.sendline(ZIMA_PASS)
    elif i == 0:
        child.sendline(ZIMA_PASS)
    
    child.expect(r'\$')
    
    # Check if we can run sudo
    child.sendline('sudo -v')
    i = child.expect([r'password for {ZIMA_USER}:', r'\$'])
    if i == 0:
        child.sendline(ZIMA_PASS)
        child.expect(r'\$')
    
    # Try the clone again with more verbosity
    child.sendline('sudo rm -rf /mnt/external_hdd/supabase')
    child.expect(r'\$')
    
    child.sendline('cd /mnt/external_hdd && git clone --depth 1 https://github.com/supabase/docker.git supabase')
    child.expect(r'\$', timeout=120)
    
    child.sendline('ls -la /mnt/external_hdd/supabase')
    child.expect(r'\$')

if __name__ == "__main__":
    debug_ssh()
