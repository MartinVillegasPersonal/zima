import pexpect
import sys

def check_migration():
    child = pexpect.spawn('ssh casaos@192.168.0.203', encoding='utf-8', timeout=60)
    child.expect('password: ')
    child.sendline('casaos')
    child.expect(r'\$')
    
    child.sendline('sudo docker info | grep "Docker Root Dir"')
    child.expect(r'\$')
    print(child.before)
    
    child.sendline('sudo docker ps -a')
    child.expect(r'\$')
    print("Containers:")
    print(child.before)

if __name__ == "__main__":
    check_migration()
