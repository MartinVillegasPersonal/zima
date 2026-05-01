import pexpect
import sys

def revert_migration():
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
    
    # 2. Revert daemon.json
    print("Reverting daemon.json...")
    child.sendline('sudo rm /etc/docker/daemon.json')
    child.expect(r'\$')
    
    # 3. Start Docker (it will use /var/lib/docker again)
    print("Starting Docker...")
    child.sendline('sudo systemctl start docker')
    child.expect(r'\$')
    
    # 4. Start all containers
    print("Starting all containers...")
    child.sendline('sudo docker start $(sudo docker ps -a -q)')
    child.expect(r'\$')
    
    # 5. Final check
    child.sendline('sudo docker ps')
    child.expect(r'\$')
    print(child.before)

if __name__ == "__main__":
    revert_migration()
