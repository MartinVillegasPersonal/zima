import pexpect
import os
from dotenv import load_dotenv

load_dotenv()
ZIMA_HOST = os.getenv("ZIMA_HOST")
ZIMA_USER = os.getenv("ZIMA_USER")
ZIMA_PASS = os.getenv("ZIMA_PASS")
import sys

def rescue_migration():
    child = pexpect.spawn(f'ssh {ZIMA_USER}@{ZIMA_HOST}', encoding='utf-8', timeout=600)
    child.logfile = sys.stdout
    child.expect('password: ')
    child.sendline(ZIMA_PASS)
    child.expect(r'\$')
    
    # 1. Stop Docker
    print("Stopping Docker...")
    child.sendline('sudo systemctl stop docker.socket && sudo systemctl stop docker')
    i = child.expect([r'password for {ZIMA_USER}:', r'\$'])
    if i == 0:
        child.sendline(ZIMA_PASS)
        child.expect(r'\$')
    
    # 2. Install rsync
    print("Installing rsync...")
    child.sendline('sudo apt-get update && sudo apt-get install -y rsync')
    child.expect(r'\$', timeout=300)
    
    # 3. Copy data properly
    print("Copying Docker data from eMMC to HDD...")
    child.sendline('sudo rsync -aqxP /var/lib/docker/ /mnt/external/docker_data')
    child.expect(r'\$', timeout=600)
    
    # 4. Start Docker
    print("Starting Docker...")
    child.sendline('sudo systemctl start docker')
    child.expect(r'\$')
    
    # 5. Verify
    print("Verifying containers...")
    child.sendline('sudo docker ps -a')
    child.expect(r'\$')
    
    print("Rescue complete.")

if __name__ == "__main__":
    rescue_migration()
