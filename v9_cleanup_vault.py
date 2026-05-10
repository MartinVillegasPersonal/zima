import pexpect
import os
from dotenv import load_dotenv

load_dotenv()
ZIMA_HOST = os.getenv("ZIMA_HOST")
ZIMA_USER = os.getenv("ZIMA_USER")
ZIMA_PASS = os.getenv("ZIMA_PASS")
import sys

def cleanup_vaultwarden():
    child = pexpect.spawn(f'ssh {ZIMA_USER}@{ZIMA_HOST}', encoding='utf-8', timeout=60)
    child.expect('password: ')
    child.sendline(ZIMA_PASS)
    child.expect(r'\$')
    
    print("Cleaning up Vaultwarden...")
    child.sendline('sudo docker rm -f vaultwarden')
    child.expect(r'\$')
    
    # Optional: remove data directory? 
    # Better keep it for now in case user changes mind, or delete if they want.
    # I will just stop and remove the container for now.
    
    print("Vaultwarden removed. System clean.")

if __name__ == "__main__":
    cleanup_vaultwarden()
