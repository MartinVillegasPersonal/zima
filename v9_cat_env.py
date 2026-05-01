import pexpect
import sys

def cat_env():
    child = pexpect.spawn('ssh casaos@192.168.0.203', encoding='utf-8', timeout=60)
    child.expect('password: ')
    child.sendline('casaos')
    child.expect(r'\$')
    
    child.sendline('cat /mnt/external_hdd/supabase/.env | grep DASHBOARD')
    child.expect(r'\$')
    print(child.before)

if __name__ == "__main__":
    cat_env()
