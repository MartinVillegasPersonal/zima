import pexpect
import os
from dotenv import load_dotenv

load_dotenv()
ZIMA_HOST = os.getenv("ZIMA_HOST")
ZIMA_USER = os.getenv("ZIMA_USER")
ZIMA_PASS = os.getenv("ZIMA_PASS")
import sys

def check_script_perms():
    child = pexpect.spawn(f'ssh {ZIMA_USER}@{ZIMA_HOST}', encoding='utf-8', timeout=60)
    child.expect('password: ')
    child.sendline(ZIMA_PASS)
    child.expect(r'\$')
    
    child.sendline('ls -la /mnt/external_hdd/supabase/volumes/api/kong-entrypoint.sh')
    child.expect(r'\$')
    print(child.before)
    
    # Also try to set it to executable
    print("Setting +x...")
    child.sendline('chmod +x /mnt/external_hdd/supabase/volumes/api/kong-entrypoint.sh')
    child.expect(r'\$')
    
    child.sendline('ls -la /mnt/external_hdd/supabase/volumes/api/kong-entrypoint.sh')
    child.expect(r'\$')
    print(child.before)

if __name__ == "__main__":
    check_script_perms()
