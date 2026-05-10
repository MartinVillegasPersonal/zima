import pexpect
import os
from dotenv import load_dotenv

load_dotenv()
ZIMA_HOST = os.getenv("ZIMA_HOST")
ZIMA_USER = os.getenv("ZIMA_USER")
ZIMA_PASS = os.getenv("ZIMA_PASS")
import sys

def list_disk():
    child = pexpect.spawn(f'ssh {ZIMA_USER}@{ZIMA_HOST}', encoding='utf-8', timeout=60)
    child.expect('password: ')
    child.sendline(ZIMA_PASS)
    child.expect(r'\$')
    
    print("Listing /mnt/external:")
    child.sendline('ls -d /mnt/external/*')
    child.expect(r'\$')
    print(child.before)
    
    print("Listing /mnt/external_hdd:")
    child.sendline('ls -d /mnt/external_hdd/*')
    child.expect(r'\$')
    print(child.before)

if __name__ == "__main__":
    list_disk()
