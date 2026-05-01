import pexpect
import sys

def diagnose_openwebui():
    child = pexpect.spawn('ssh casaos@192.168.0.203', encoding='utf-8', timeout=60)
    child.expect('password: ')
    child.sendline('casaos')
    child.expect(r'\$')
    
    # 1. Check if container exists
    print("Checking container status:")
    child.sendline('sudo docker ps -a | grep open-webui')
    child.expect(r'\$')
    print(child.before)
    
    # 2. Check logs if it exists
    print("Checking logs:")
    child.sendline('sudo docker logs open-webui | tail -n 20')
    child.expect(r'\$')
    print(child.before)
    
    # 3. Check port listening
    print("Checking listening ports:")
    child.sendline('sudo ss -tulpn | grep 3001')
    child.expect(r'\$')
    print(child.before)

if __name__ == "__main__":
    diagnose_openwebui()
