import pexpect
import sys

def check_fstab():
    child = pexpect.spawn('ssh casaos@192.168.0.203', encoding='utf-8', timeout=60)
    child.expect('password: ')
    child.sendline('casaos')
    child.expect(r'\$')
    
    print("Checking /etc/fstab:")
    child.sendline('cat /etc/fstab')
    child.expect(r'\$')
    print(child.before)
    
    print("Checking current mounts:")
    child.sendline('mount | grep /dev/sda1')
    child.expect(r'\$')
    print(child.before)

if __name__ == "__main__":
    check_fstab()
