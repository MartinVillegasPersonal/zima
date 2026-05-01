import pexpect
import sys

def restart_kong():
    child = pexpect.spawn('ssh casaos@192.168.0.203', encoding='utf-8', timeout=60)
    child.expect('password: ')
    child.sendline('casaos')
    child.expect(r'\$')
    
    child.sendline('cd /mnt/external_hdd/supabase && sudo docker compose up -d kong')
    child.expect(r'\$')
    
    child.sendline('sudo docker ps | grep kong')
    child.expect(r'\$')
    print(child.before)

if __name__ == "__main__":
    restart_kong()
