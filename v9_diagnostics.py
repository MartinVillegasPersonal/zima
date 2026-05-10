import pexpect
import os
from dotenv import load_dotenv

load_dotenv()
ZIMA_HOST = os.getenv("ZIMA_HOST")
ZIMA_USER = os.getenv("ZIMA_USER")
ZIMA_PASS = os.getenv("ZIMA_PASS")

def run_diagnostics():
    child = pexpect.spawn(f'ssh {ZIMA_USER}@{ZIMA_HOST}', encoding='utf-8', timeout=60)
    
    i = child.expect(['password: ', 'Are you sure you want to continue connecting', pexpect.EOF, pexpect.TIMEOUT])
    if i == 1:
        child.sendline('yes')
        child.expect('password: ')
        child.sendline(ZIMA_PASS)
    elif i == 0:
        child.sendline(ZIMA_PASS)
    else:
        print("Failed to connect.")
        return

    child.expect(r'\$')

    commands = [
        "docker-compose --version || docker compose version",
        "ls -la /mnt/external_hdd",
        "docker ps"
    ]
    
    for cmd in commands:
        print(f"Executing: {cmd}")
        child.sendline(cmd)
        child.expect(r'\$')
        print(child.before)
        print("-" * 20)

if __name__ == "__main__":
    run_diagnostics()
