import pexpect
import os
from dotenv import load_dotenv

load_dotenv()
ZIMA_HOST = os.getenv("ZIMA_HOST")
ZIMA_USER = os.getenv("ZIMA_USER")
ZIMA_PASS = os.getenv("ZIMA_PASS")
import sys

def debug_openwebui():
    child = pexpect.spawn(f'ssh {ZIMA_USER}@{ZIMA_HOST}', encoding='utf-8', timeout=60)
    child.expect('password: ')
    child.sendline(ZIMA_PASS)
    child.expect(r'\$')
    
    print("Docker PS:")
    child.sendline('sudo docker ps -a | grep open-webui')
    child.expect(r'\$')
    print(child.before)
    
    print("Logs:")
    child.sendline('sudo docker logs open-webui | tail -n 20')
    child.expect(r'\$')
    print(child.before)
    
    print("Network check:")
    child.sendline('sudo ss -tulpn | grep 3001')
    child.expect(r'\$')
    print(child.before)

if __name__ == "__main__":
    debug_openwebui()
