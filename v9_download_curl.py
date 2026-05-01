import pexpect
import sys

def download_supabase_curl():
    child = pexpect.spawn('ssh casaos@192.168.0.203', encoding='utf-8', timeout=120)
    child.logfile = sys.stdout
    
    child.expect('password: ')
    child.sendline('casaos')
    child.expect(r'\$')
    
    child.sendline('cd /mnt/external_hdd && sudo rm -rf supabase_tmp.zip supabase')
    child.expect(r'\$')
    
    # Try master.zip
    child.sendline('curl -L https://github.com/supabase/docker/archive/refs/heads/master.zip -o supabase_tmp.zip')
    child.expect(r'\$', timeout=120)
    
    child.sendline('unzip supabase_tmp.zip')
    child.expect(r'\$', timeout=60)
    
    # Rename folder (it might be docker-master or supabase-master)
    child.sendline('mv docker-master supabase || mv supabase-master supabase')
    child.expect(r'\$')
    
    child.sendline('ls -la /mnt/external_hdd/supabase')
    child.expect(r'\$')

if __name__ == "__main__":
    download_supabase_curl()
