import pexpect
import os
from dotenv import load_dotenv

load_dotenv()
ZIMA_HOST = os.getenv("ZIMA_HOST")
ZIMA_USER = os.getenv("ZIMA_USER")
ZIMA_PASS = os.getenv("ZIMA_PASS")
import sys

def get_final_logs():
    child = pexpect.spawn(f'ssh {ZIMA_USER}@{ZIMA_HOST}', encoding='utf-8', timeout=60)
    child.expect('password: ')
    child.sendline(ZIMA_PASS)
    child.expect(r'\$')
    
    print("Checking docker ps:")
    child.sendline('sudo docker ps | grep open-webui')
    child.expect(r'\$')
    print(child.before)
    
    print("Full Logs of Open WebUI:")
    child.sendline('sudo docker logs open-webui')
    child.expect(r'\$')
    print(child.before)

if __name__ == "__main__":
    get_final_logs()
