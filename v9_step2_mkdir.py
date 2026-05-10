import pexpect
import os
from dotenv import load_dotenv

load_dotenv()
ZIMA_HOST = os.getenv("ZIMA_HOST")
ZIMA_USER = os.getenv("ZIMA_USER")
ZIMA_PASS = os.getenv("ZIMA_PASS")

def run():
    child = pexpect.spawn(f'ssh {ZIMA_USER}@{ZIMA_HOST}', encoding='utf-8', timeout=120)
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
        # Paso 2: Crear directorios
        "echo 'casaos' | sudo -S mkdir -p /mnt/external_hdd/supabase_postgres_data",
        "echo 'casaos' | sudo -S chown -R casaos:casaos /mnt/external_hdd/supabase_postgres_data",
        "ls -la /mnt/external_hdd/",
    ]

    for cmd in commands:
        print(f"\n>>> {cmd}")
        child.sendline(cmd)
        while True:
            i = child.expect([r'\[sudo\] password for {ZIMA_USER}:', r'\$', pexpect.TIMEOUT, pexpect.EOF], timeout=60)
            if i == 0:
                child.sendline(ZIMA_PASS)
            elif i == 1:
                break
            else:
                break
        print(child.before)

if __name__ == "__main__":
    run()
