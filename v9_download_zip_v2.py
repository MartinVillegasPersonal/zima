import pexpect
import sys

def download_supabase():
    child = pexpect.spawn('ssh casaos@192.168.0.203', encoding='utf-8', timeout=120)
    child.logfile = sys.stdout
    
    child.expect('password: ')
    child.sendline('casaos')
    child.expect(r'\$')
    
    # Download ZIP
    child.sendline('cd /mnt/external_hdd && sudo rm -rf supabase_tmp.zip supabase_docker-main docker-main supabase')
    i = child.expect([r'password for casaos:', r'\$'])
    if i == 0:
        child.sendline('casaos')
        child.expect(r'\$')
    
    # Try different URLs if main.zip fails
    child.sendline('wget https://github.com/supabase/docker/archive/refs/heads/main.zip -O supabase_tmp.zip')
    child.expect(r'\$', timeout=60)
    
    # Unzip
    child.sendline('unzip supabase_tmp.zip')
    child.expect(r'\$', timeout=60)
    
    # Move and rename
    child.sendline('mv docker-main supabase')
    child.expect(r'\$')
    
    # Cleanup
    child.sendline('rm supabase_tmp.zip')
    child.expect(r'\$')
    
    print("Supabase downloaded.")

if __name__ == "__main__":
    download_supabase()
