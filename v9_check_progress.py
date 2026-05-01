import pexpect
import sys

def check_progress():
    child = pexpect.spawn('ssh casaos@192.168.0.203', encoding='utf-8', timeout=60)
    child.expect('password: ')
    child.sendline('casaos')
    child.expect(r'\$')
    
    print("Docker images:")
    child.sendline('sudo docker images')
    child.expect(r'\$')
    print(child.before)
    
    print("Disk usage (HDD):")
    child.sendline('df -h /mnt/external')
    child.expect(r'\$')
    print(child.before)

if __name__ == "__main__":
    check_progress()
