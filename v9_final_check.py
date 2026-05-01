import pexpect
import sys

def startup_and_check():
    child = pexpect.spawn('ssh casaos@192.168.0.203', encoding='utf-8', timeout=120)
    child.expect('password: ')
    child.sendline('casaos')
    child.expect(r'\$')
    
    # 1. Start all containers
    print("Starting all containers...")
    child.sendline('sudo docker start $(sudo docker ps -a -q)')
    i = child.expect([r'password for casaos:', r'\$'])
    if i == 0:
        child.sendline('casaos')
        child.expect(r'\$')
    
    # 2. Check disk usage
    print("Checking final disk usage...")
    child.sendline('df -h /')
    child.expect(r'\$')
    print(child.before)
    
    # 3. Check Docker root dir
    child.sendline('sudo docker info | grep "Docker Root Dir"')
    child.expect(r'\$')
    print(child.before)

if __name__ == "__main__":
    startup_and_check()
