import pexpect
import os
from dotenv import load_dotenv

load_dotenv()
ZIMA_HOST = os.getenv("ZIMA_HOST")
ZIMA_USER = os.getenv("ZIMA_USER")
ZIMA_PASS = os.getenv("ZIMA_PASS")
import sys

def stabilize():
    child = pexpect.spawn(f'ssh {ZIMA_USER}@{ZIMA_HOST}', encoding='utf-8', timeout=60)
    child.expect('password: ')
    child.sendline(ZIMA_PASS)
    child.expect(r'\$')
    
    # 1. Restart all existing containers
    print("Restarting Supabase and others...")
    child.sendline('sudo docker start $(sudo docker ps -a -q)')
    child.expect(r'\$')
    
    # 2. Launch Open WebUI pull in background (nohup)
    print("Launching Open WebUI pull in background...")
    child.sendline('nohup sudo docker pull ghcr.io/open-webui/open-webui:main > /dev/null 2>&1 &')
    child.expect(r'\$')
    
    print("Stabilization command sent.")

if __name__ == "__main__":
    stabilize()
