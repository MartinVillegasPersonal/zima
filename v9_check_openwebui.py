import pexpect
import os
from dotenv import load_dotenv

load_dotenv()
ZIMA_HOST = os.getenv("ZIMA_HOST")
ZIMA_USER = os.getenv("ZIMA_USER")
ZIMA_PASS = os.getenv("ZIMA_PASS")
import sys

def check_all():
    child = pexpect.spawn(f'ssh {ZIMA_USER}@{ZIMA_HOST}', encoding='utf-8', timeout=60)
    child.expect('password: ')
    child.sendline(ZIMA_PASS)
    child.expect(r'\$')
    
    child.sendline('sudo docker ps -a | grep open-webui')
    child.expect(r'\$')
    print("Open WebUI Status:")
    print(child.before)
    
    child.sendline('sudo docker logs open-webui')
    child.expect(r'\$')
    print("Open WebUI Logs:")
    print(child.before)

if __name__ == "__main__":
    check_all()
