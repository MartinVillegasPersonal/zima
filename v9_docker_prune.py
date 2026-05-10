import pexpect
import os
from dotenv import load_dotenv

load_dotenv()
ZIMA_HOST = os.getenv("ZIMA_HOST")
ZIMA_USER = os.getenv("ZIMA_USER")
ZIMA_PASS = os.getenv("ZIMA_PASS")
import sys

def prune_docker():
    child = pexpect.spawn(f'ssh {ZIMA_USER}@{ZIMA_HOST}', encoding='utf-8', timeout=120)
    child.logfile = sys.stdout
    child.expect('password: ')
    child.sendline(ZIMA_PASS)
    child.expect(r'\$')
    
    print("Pruning unused Docker images...")
    child.sendline('sudo docker image prune -a -f')
    i = child.expect([r'password for {ZIMA_USER}:', r'\$'])
    if i == 0:
        child.sendline(ZIMA_PASS)
        child.expect(r'\$')
    
    print("Checking space again...")
    child.sendline('df -h /')
    child.expect(r'\$')
    
    child.sendline('sudo docker system df')
    child.expect(r'\$')

if __name__ == "__main__":
    prune_docker()
