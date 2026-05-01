import pexpect
import sys

def adjust_vaultwarden():
    child = pexpect.spawn('ssh casaos@192.168.0.203', encoding='utf-8', timeout=60)
    child.expect('password: ')
    child.sendline('casaos')
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
