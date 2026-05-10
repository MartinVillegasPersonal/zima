import pexpect
import os
from dotenv import load_dotenv

load_dotenv()
ZIMA_HOST = os.getenv("ZIMA_HOST")
ZIMA_USER = os.getenv("ZIMA_USER")
ZIMA_PASS = os.getenv("ZIMA_PASS")

def run():
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
        "sudo docker ps -a",
        "df -h /mnt/external_hdd",
        "free -h",
        "curl -s http://127.0.0.1:11434/api/tags | head -c 200 || echo 'Ollama no responde'",
        "curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:3000 || echo 'Chatbot-UI no responde'"
    ]

    for cmd in commands:
        print(f"\n>>> {cmd}")
        child.sendline(cmd)
        while True:
            i = child.expect([r'\[sudo\] password for {ZIMA_USER}:', r'\$', pexpect.TIMEOUT, pexpect.EOF], timeout=30)
            if i == 0:
                child.sendline(ZIMA_PASS)
            elif i == 1:
                break
            else:
                break
        print(child.before)

if __name__ == "__main__":
    run()
