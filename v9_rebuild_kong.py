import pexpect
import sys

def rebuild_kong():
    child = pexpect.spawn('ssh casaos@192.168.0.203', encoding='utf-8', timeout=300)
    child.logfile = sys.stdout
    child.expect('password: ')
    child.sendline('casaos')
    child.expect(r'\$')
    
    # Remove the failed container
    print("Removing old kong container...")
    child.sendline('sudo docker rm -f supabase-kong')
    child.expect(r'\$')
    
    # Re-up it from compose (this will use /var/lib/docker images)
    print("Re-upping kong from compose...")
    child.sendline('cd /mnt/external_hdd/supabase && sudo docker compose up -d kong')
    child.expect(r'\$')
    
    # Check status
    child.sendline('sudo docker ps | grep kong')
    child.expect(r'\$')

if __name__ == "__main__":
    rebuild_kong()
