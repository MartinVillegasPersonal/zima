import pexpect
import os
from dotenv import load_dotenv

load_dotenv()
ZIMA_HOST = os.getenv("ZIMA_HOST")
ZIMA_USER = os.getenv("ZIMA_USER")
ZIMA_PASS = os.getenv("ZIMA_PASS")
import sys

def check_disk_space():
    child = pexpect.spawn(f'ssh {ZIMA_USER}@{ZIMA_HOST}', encoding='utf-8', timeout=60)
    child.expect('password: ')
    child.sendline(ZIMA_PASS)
    child.expect(r'\$')
    
    print("Disk usage (Summary):")
    child.sendline('df -h')
    child.expect(r'\$')
    print(child.before)
    
    print("-" * 20)
    print("Docker space usage:")
    child.sendline('sudo docker system df')
    i = child.expect([r'password for {ZIMA_USER}:', r'\$'])
    if i == 0:
        child.sendline(ZIMA_PASS)
        child.expect(r'\$')
    print(child.before)
    
    print("-" * 20)
    print("Top 10 largest folders in root (excluding /mnt):")
    child.sendline('sudo du -hx --max-depth=2 / | sort -rh | head -n 10')
    child.expect(r'\$', timeout=120)
    print(child.before)

if __name__ == "__main__":
    check_disk_space()
