import pexpect
import sys

def rescue_migration():
    child = pexpect.spawn('ssh casaos@192.168.0.203', encoding='utf-8', timeout=600)
    child.logfile = sys.stdout
    child.expect('password: ')
    child.sendline('casaos')
    child.expect(r'\$')
    
    # 1. Stop Docker
    print("Stopping Docker...")
    child.sendline('sudo systemctl stop docker.socket && sudo systemctl stop docker')
    i = child.expect([r'password for casaos:', r'\$'])
    if i == 0:
        child.sendline('casaos')
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
