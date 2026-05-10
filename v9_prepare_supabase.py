import pexpect
import os
from dotenv import load_dotenv

load_dotenv()
ZIMA_HOST = os.getenv("ZIMA_HOST")
ZIMA_USER = os.getenv("ZIMA_USER")
ZIMA_PASS = os.getenv("ZIMA_PASS")
import sys

def run_ssh_commands():
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

    # 1. Clean up and Clone
    print("Cleaning and Cloning Supabase...")
    commands = [
        "sudo rm -rf /mnt/external_hdd/supabase",
        "cd /mnt/external_hdd && git clone --depth 1 https://github.com/supabase/docker.git supabase",
        "cd /mnt/external_hdd/supabase && cp .env.example .env"
    ]
    
    for cmd in commands:
        child.sendline(cmd)
        i = child.expect([r'\[sudo\] password for {ZIMA_USER}:', r'\$', pexpect.TIMEOUT, pexpect.EOF])
        if i == 0:
            child.sendline(ZIMA_PASS)
            child.expect(r'\$')
    
    # 2. Modify docker-compose.yml
    # We want to replace the volume mapping for the 'db' service.
    # Looking at Supabase docker-compose, it uses:
    # volumes:
    #  - ./volumes/db/init:/docker-entrypoint-initdb.d:ro
    #  - db-data:/var/lib/postgresql/data:Z
    
    print("Modifying docker-compose.yml...")
    # Change the db-data volume to a bind mount
    sed_cmd = "sudo sed -i 's|db-data:/var/lib/postgresql/data|/mnt/external_hdd/supabase_postgres_data:/var/lib/postgresql/data|g' /mnt/external_hdd/supabase/docker-compose.yml"
    child.sendline(sed_cmd)
    child.expect(r'\$')
    
    # Also need to remove the db-data volume definition at the end to avoid errors
    sed_volumes_cmd = "sudo sed -i '/db-data:/d' /mnt/external_hdd/supabase/docker-compose.yml"
    child.sendline(sed_volumes_cmd)
    child.expect(r'\$')

    print("Supabase prepared.")

if __name__ == "__main__":
    run_ssh_commands()
