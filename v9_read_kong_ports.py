import pexpect
import sys

def read_kong_ports():
    child = pexpect.spawn('ssh casaos@192.168.0.203', encoding='utf-8', timeout=60)
    child.expect('password: ')
    child.sendline('casaos')
    child.expect(r'\$')
    
    child.sendline('sed -n "95,110p" /mnt/external_hdd/supabase/docker-compose.yml')
    child.expect(r'\$')
    print(child.before)

if __name__ == "__main__":
    read_kong_ports()
