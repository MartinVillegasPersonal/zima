import pexpect
import sys

def list_disk():
    child = pexpect.spawn('ssh casaos@192.168.0.203', encoding='utf-8', timeout=60)
    child.expect('password: ')
    child.sendline('casaos')
    child.expect(r'\$')
    
    print("Listing /mnt/external:")
    child.sendline('ls -d /mnt/external/*')
    child.expect(r'\$')
    print(child.before)
    
    print("Listing /mnt/external_hdd:")
    child.sendline('ls -d /mnt/external_hdd/*')
    child.expect(r'\$')
    print(child.before)

if __name__ == "__main__":
    list_disk()
