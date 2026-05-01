import pexpect
import sys

def download_supabase():
    child = pexpect.spawn('ssh casaos@192.168.0.203', encoding='utf-8', timeout=120)
    child.logfile = sys.stdout
    
    child.expect('password: ')
    child.sendline('casaos')
    child.expect(r'\$')
    
    # Install unzip if not present
    child.sendline('sudo apt-get update && sudo apt-get install -y unzip')
    child.expect('password for casaos:', timeout=10)
    child.sendline('casaos')
    child.expect(r'\$', timeout=60)
    
    # Download ZIP
    child.sendline('cd /mnt/external_hdd && sudo rm -rf supabase_tmp.zip supabase_docker-master')
    child.expect(r'\$')
    
    child.sendline('wget https://github.com/supabase/docker/archive/refs/heads/main.zip -O supabase_tmp.zip')
    child.expect(r'\$', timeout=60)
    
    # Unzip
    child.sendline('unzip supabase_tmp.zip')
    child.expect(r'\$', timeout=60)
    
    # Rename folder to supabase
    child.sendline('sudo rm -rf supabase && mv docker-main supabase')
    child.expect(r'\$')
    
    # Cleanup
    child.sendline('rm supabase_tmp.zip')
    child.expect(r'\$')
    
    print("Supabase downloaded and unzipped.")

if __name__ == "__main__":
    download_supabase()
