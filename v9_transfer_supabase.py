import pexpect
import os
from dotenv import load_dotenv

load_dotenv()
ZIMA_HOST = os.getenv("ZIMA_HOST")
ZIMA_USER = os.getenv("ZIMA_USER")
ZIMA_PASS = os.getenv("ZIMA_PASS")
import sys

def transfer_and_extract():
    # SCP transfer
    print("Transferring tarball...")
    child = pexpect.spawn('scp supabase_docker.tar.gz casaos@192.168.0.203:/tmp/', encoding='utf-8', timeout=60)
    child.logfile = sys.stdout
    child.expect('password: ')
    child.sendline(ZIMA_PASS)
    child.expect(pexpect.EOF)
    
    # SSH extraction
    print("Extracting on ZimaBlade...")
    child = pexpect.spawn(f'ssh {ZIMA_USER}@{ZIMA_HOST}', encoding='utf-8', timeout=60)
    child.logfile = sys.stdout
    child.expect('password: ')
    child.sendline(ZIMA_PASS)
    child.expect(r'\$')
    
    # Create directory and extract
    child.sendline('sudo mkdir -p /mnt/external_hdd/supabase')
    i = child.expect([r'password for {ZIMA_USER}:', r'\$'])
    if i == 0:
        child.sendline(ZIMA_PASS)
        child.expect(r'\$')
    
    child.sendline('sudo tar -xzf /tmp/supabase_docker.tar.gz -C /mnt/external_hdd/supabase')
    child.expect(r'\$')
    
    child.sendline('sudo chown -R casaos:casaos /mnt/external_hdd/supabase')
    child.expect(r'\$')
    
    child.sendline('ls -la /mnt/external_hdd/supabase')
    child.expect(r'\$')
    
    print("Extraction complete.")

if __name__ == "__main__":
    transfer_and_extract()
