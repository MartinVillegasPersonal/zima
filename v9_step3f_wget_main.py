import pexpect
import os
from dotenv import load_dotenv

load_dotenv()
ZIMA_HOST = os.getenv("ZIMA_HOST")
ZIMA_USER = os.getenv("ZIMA_USER")
ZIMA_PASS = os.getenv("ZIMA_PASS")

def run():
    child = pexpect.spawn(f'ssh {ZIMA_USER}@{ZIMA_HOST}', encoding='utf-8', timeout=300)
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
        "rm -f /tmp/supabase.zip && wget --no-check-certificate -O /tmp/supabase.zip 'https://codeload.github.com/supabase/docker/zip/refs/heads/main' && echo 'WGET_OK' || echo 'WGET_FAIL'",
        "ls -lh /tmp/supabase.zip",
        "rm -rf /tmp/supabase_extract && unzip -q /tmp/supabase.zip -d /tmp/supabase_extract && echo 'UNZIP_OK' || echo 'UNZIP_FAIL'",
        "ls /tmp/supabase_extract/",
        "cp -r /tmp/supabase_extract/docker-main/. /mnt/external_hdd/supabase/ && echo 'COPY_OK'",
        "ls /mnt/external_hdd/supabase/",
        "cp /mnt/external_hdd/supabase/.env.example /mnt/external_hdd/supabase/.env && echo 'ENV_OK'"
    ]

    for cmd in commands:
        print(f"\n>>> {cmd}")
        child.sendline(cmd)
        while True:
            i = child.expect([r'\[sudo\] password for {ZIMA_USER}:', r'\$', pexpect.TIMEOUT, pexpect.EOF], timeout=180)
            if i == 0:
                child.sendline(ZIMA_PASS)
            elif i == 1:
                break
            else:
                print("TIMEOUT/EOF")
                break
        print(child.before)

if __name__ == "__main__":
    run()
