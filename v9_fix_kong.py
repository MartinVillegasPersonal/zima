import pexpect
import sys

def fix_kong_conflict():
    child = pexpect.spawn('ssh casaos@192.168.0.203', encoding='utf-8', timeout=120)
    child.logfile = sys.stdout
    child.expect('password: ')
    child.sendline('casaos')
    child.expect(r'\$')
    
    # 1. Stop Portainer
    print("Stopping Portainer to free port 8000...")
    child.sendline('sudo docker stop portainer')
    i = child.expect([r'password for casaos:', r'\$'])
    if i == 0:
        child.sendline('casaos')
        child.expect(r'\$')
    
    # 2. Try starting Kong again
    print("Starting Kong...")
    child.sendline('cd /mnt/external_hdd/supabase && sudo docker compose up -d kong')
    child.expect(r'\$')
    
    # 3. Check logs
    child.sendline('sudo docker logs supabase-kong')
    child.expect(r'\$')
    
    # 4. Check status
    child.sendline('sudo docker ps | grep kong')
    child.expect(r'\$')

if __name__ == "__main__":
    fix_kong_conflict()
