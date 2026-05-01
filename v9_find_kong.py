import pexpect
import sys

def find_kong_service():
    child = pexpect.spawn('ssh casaos@192.168.0.203', encoding='utf-8', timeout=60)
    child.expect('password: ')
    child.sendline('casaos')
    child.expect(r'\$')
    
    child.sendline('grep -n "^  kong:" /mnt/external_hdd/supabase/docker-compose.yml')
    child.expect(r'\$')
    print(child.before)

if __name__ == "__main__":
    find_kong_service()
