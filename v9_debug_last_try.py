import pexpect
import sys

def debug_openwebui():
    child = pexpect.spawn('ssh casaos@192.168.0.203', encoding='utf-8', timeout=60)
    child.expect('password: ')
    child.sendline('casaos')
    child.expect(r'\$')
    
    print("Docker PS:")
    child.sendline('sudo docker ps -a | grep open-webui')
    child.expect(r'\$')
    print(child.before)
    
    print("Logs:")
    child.sendline('sudo docker logs open-webui | tail -n 20')
    child.expect(r'\$')
    print(child.before)
    
    print("Network check:")
    child.sendline('sudo ss -tulpn | grep 3001')
    child.expect(r'\$')
    print(child.before)

if __name__ == "__main__":
    debug_openwebui()
