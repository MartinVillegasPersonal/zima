import pexpect
import os
from dotenv import load_dotenv

load_dotenv()
ZIMA_HOST = os.getenv("ZIMA_HOST")
ZIMA_USER = os.getenv("ZIMA_USER")
ZIMA_PASS = os.getenv("ZIMA_PASS")
import sys

def secure_startup():
    child = pexpect.spawn(f'ssh {ZIMA_USER}@{ZIMA_HOST}', encoding='utf-8', timeout=600)
    child.logfile = sys.stdout
    child.expect('password: ')
    child.sendline(ZIMA_PASS)
    child.expect(r'\$')
    
    print("Stopping Docker for path unification...")
    child.sendline('sudo systemctl stop docker.socket && sudo systemctl stop docker')
    child.expect(r'\$')
    
    # 2. Move data to the persistent fstab path
    print("Moving Docker data to persistent fstab path...")
    child.sendline('sudo mkdir -p /mnt/external_hdd/docker_data')
    # Since it's the same disk, moving the content of the folders is better than moving the folder itself if nested
    child.sendline('sudo mv /mnt/external/docker_data_new/* /mnt/external_hdd/docker_data/')
    child.expect(r'\$')
    
    # 3. Update daemon.json
    print("Updating Docker configuration...")
    child.sendline('cat <<EOF | sudo tee /etc/docker/daemon.json\n{\n  "data-root": "/mnt/external_hdd/docker_data"\n}\nEOF')
    child.expect(r'\$')
    
    # 4. Start Docker
    print("Starting Docker...")
    child.sendline('sudo systemctl start docker')
    child.expect(r'\$')
    
    # 5. Final Check
    child.sendline('sudo docker info | grep "Docker Root Dir"')
    child.expect(r'\$')
    print(child.before)

if __name__ == "__main__":
    secure_startup()
