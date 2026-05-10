import pexpect
import os
from dotenv import load_dotenv

load_dotenv()
ZIMA_HOST = os.getenv("ZIMA_HOST")
ZIMA_USER = os.getenv("ZIMA_USER")
ZIMA_PASS = os.getenv("ZIMA_PASS")
import sys
import json

def migrate_docker_root():
    child = pexpect.spawn(f'ssh {ZIMA_USER}@{ZIMA_HOST}', encoding='utf-8', timeout=600)
    child.logfile = sys.stdout
    child.expect('password: ')
    child.sendline(ZIMA_PASS)
    child.expect(r'\$')
    
    # 1. Stop all containers
    print("Stopping all containers...")
    child.sendline('sudo docker stop $(sudo docker ps -q)')
    i = child.expect([r'password for {ZIMA_USER}:', r'\$'])
    if i == 0:
        child.sendline(ZIMA_PASS)
        child.expect(r'\$')
    
    # 2. Stop Docker services
    print("Stopping Docker services...")
    child.sendline('sudo systemctl stop docker.socket && sudo systemctl stop docker')
    child.expect(r'\$')
    
    # 3. Create destination directory
    print("Creating destination directory...")
    child.sendline('sudo mkdir -p /mnt/external/docker_data')
    child.expect(r'\$')
    
    # 4. Sync data
    print("Syncing Docker data to HDD (this may take a few minutes)...")
    child.sendline('sudo rsync -aqxP /var/lib/docker/ /mnt/external/docker_data')
    child.expect(r'\$', timeout=600)
    
    # 5. Configure daemon.json
    print("Configuring /etc/docker/daemon.json...")
    # Read existing if any
    child.sendline('sudo cat /etc/docker/daemon.json')
    child.expect(r'\$')
    existing_content = child.before.strip().splitlines()
    config = {}
    # Find the actual JSON content in the output
    for line in existing_content:
        if line.strip().startswith('{'):
            try:
                config = json.loads(line)
            except:
                pass
    
    config["data-root"] = "/mnt/external/docker_data"
    config_json = json.dumps(config)
    
    # Write new daemon.json
    child.sendline(f"echo '{config_json}' | sudo tee /etc/docker/daemon.json")
    child.expect(r'\$')
    
    # 6. Start Docker
    print("Starting Docker service...")
    child.sendline('sudo systemctl start docker')
    child.expect(r'\$')
    
    # 7. Verification
    print("Verifying migration...")
    child.sendline('sudo docker info | grep "Docker Root Dir"')
    child.expect(r'\$')
    
    print("Migration finished.")

if __name__ == "__main__":
    migrate_docker_root()
