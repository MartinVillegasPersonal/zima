import pexpect
import sys

def check_all():
    child = pexpect.spawn('ssh casaos@192.168.0.203', encoding='utf-8', timeout=60)
    child.expect('password: ')
    child.sendline('casaos')
    child.expect(r'\$')
    
    child.sendline('sudo docker ps -a | grep open-webui')
    child.expect(r'\$')
    print("Open WebUI Status:")
    print(child.before)
    
    child.sendline('sudo docker logs open-webui')
    child.expect(r'\$')
    print("Open WebUI Logs:")
    print(child.before)

if __name__ == "__main__":
    check_all()
