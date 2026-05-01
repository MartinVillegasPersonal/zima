import pexpect
import sys

def check_containers():
    child = pexpect.spawn('ssh casaos@192.168.0.203', encoding='utf-8', timeout=60)
    
    child.expect('password: ')
    child.sendline('casaos')
    child.expect(r'\$')
    
    child.sendline('sudo docker ps -a | grep supabase')
    child.expect(r'\$')
    print("Active/Exited Supabase containers:")
    print(child.before)
    
    child.sendline('cd /mnt/external_hdd/supabase && sudo docker compose logs db | tail -n 20')
    child.expect(r'\$')
    print("DB logs:")
    print(child.before)

if __name__ == "__main__":
    check_containers()
