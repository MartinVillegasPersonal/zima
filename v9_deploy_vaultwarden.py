import pexpect
import sys

def deploy_vaultwarden():
    child = pexpect.spawn('ssh casaos@192.168.0.203', encoding='utf-8', timeout=300)
    child.logfile = sys.stdout
    child.expect('password: ')
    child.sendline('casaos')
    child.expect(r'\$')
    
    # 1. Create directory
    print("Creating storage directory on HDD...")
    child.sendline('sudo mkdir -p /mnt/external_hdd/vaultwarden/data')
    child.sendline('sudo chown -R casaos:casaos /mnt/external_hdd/vaultwarden')
    child.expect(r'\$')
    
    # 2. Create docker-compose.yml
    print("Creating docker-compose.yml for Vaultwarden...")
    compose_content = """
version: '3'
services:
  vaultwarden:
    image: vaultwarden/server:latest
    container_name: vaultwarden
    restart: always
    environment:
      - SIGNUPS_ALLOWED=true
      - DOMAIN=http://192.168.0.203:7277
    volumes:
      - /mnt/external_hdd/vaultwarden/data:/data
    ports:
      - 7277:80
"""
    # Use heredoc to write file
    child.sendline("cat <<EOF > /mnt/external_hdd/vaultwarden/docker-compose.yml")
    child.sendline(compose_content)
    child.sendline("EOF")
    child.expect(r'\$')
    
    # 3. Deploy
    print("Deploying Vaultwarden...")
    child.sendline('cd /mnt/external_hdd/vaultwarden && sudo docker compose up -d')
    child.expect(r'\$', timeout=300)
    
    # 4. Verification
    child.sendline('sudo docker ps | grep vaultwarden')
    child.expect(r'\$')
    print(child.before)

if __name__ == "__main__":
    deploy_vaultwarden()
