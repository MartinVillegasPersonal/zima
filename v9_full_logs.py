import pexpect
import sys

def get_final_logs():
    child = pexpect.spawn('ssh casaos@192.168.0.203', encoding='utf-8', timeout=60)
    child.expect('password: ')
    child.sendline('casaos')
    child.expect(r'\$')
    
    print("Checking docker ps:")
    child.sendline('sudo docker ps | grep open-webui')
    child.expect(r'\$')
    print(child.before)
    
    print("Full Logs of Open WebUI:")
    child.sendline('sudo docker logs open-webui')
    child.expect(r'\$')
    print(child.before)

if __name__ == "__main__":
    get_final_logs()
