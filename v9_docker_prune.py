import pexpect
import sys

def prune_docker():
    child = pexpect.spawn('ssh casaos@192.168.0.203', encoding='utf-8', timeout=120)
    child.logfile = sys.stdout
    child.expect('password: ')
    child.sendline('casaos')
    child.expect(r'\$')
    
    print("Pruning unused Docker images...")
    child.sendline('sudo docker image prune -a -f')
    i = child.expect([r'password for casaos:', r'\$'])
    if i == 0:
        child.sendline('casaos')
        child.expect(r'\$')
    
    print("Checking space again...")
    child.sendline('df -h /')
    child.expect(r'\$')
    
    child.sendline('sudo docker system df')
    child.expect(r'\$')

if __name__ == "__main__":
    prune_docker()
