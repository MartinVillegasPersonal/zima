import pexpect
import sys

def check_revert():
    child = pexpect.spawn('ssh casaos@192.168.0.203', encoding='utf-8', timeout=60)
    child.expect('password: ')
    child.sendline('casaos')
    child.expect(r'\$')
    
    child.sendline('sudo docker info | grep "Docker Root Dir"')
    child.expect(r'\$')
    print(child.before)
    
    child.sendline('ls -la /etc/docker/daemon.json')
    child.expect(r'\$')
    print(child.before)

if __name__ == "__main__":
    check_revert()
