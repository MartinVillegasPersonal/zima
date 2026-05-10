import pexpect
import os
from dotenv import load_dotenv

load_dotenv()
ZIMA_HOST = os.getenv("ZIMA_HOST")
ZIMA_USER = os.getenv("ZIMA_USER")
ZIMA_PASS = os.getenv("ZIMA_PASS")
import sys

def adjust_vaultwarden():
    child = pexpect.spawn(f'ssh {ZIMA_USER}@{ZIMA_HOST}', encoding='utf-8', timeout=60)
    child.expect('password: ')
    child.sendline(ZIMA_PASS)
    child.expect(r'\$')
    
    # Update docker-compose with DOMAIN=http://localhost:7277
    print("Adjusting Vaultwarden configuration...")
    new_compose = """
version: '3'
services:
  vaultwarden:
    image: vaultwarden/server:latest
    container_name: vaultwarden
    restart: always
    environment:
      - SIGNUPS_ALLOWED=true
      - DOMAIN=http://localhost:7277
    volumes:
      - /mnt/external_hdd/vaultwarden/data:/data
    ports:
      - 7277:80
"""
    child.sendline("cat <<EOF > /mnt/external_hdd/vaultwarden/docker-compose.yml")
    child.sendline(new_compose)
    child.sendline("EOF")
    child.expect(r'\$')
    
    # Restart
    print("Restarting Vaultwarden...")
    child.sendline('cd /mnt/external_hdd/vaultwarden && sudo docker compose up -d')
    child.expect(r'\$')
    print("Restarted.")

if __name__ == "__main__":
    adjust_vaultwarden()
