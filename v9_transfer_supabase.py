import pexpect
import sys

def transfer_and_extract():
    # SCP transfer
    print("Transferring tarball...")
    child = pexpect.spawn('scp supabase_docker.tar.gz casaos@192.168.0.203:/tmp/', encoding='utf-8', timeout=60)
    child.logfile = sys.stdout
    child.expect('password: ')
    child.sendline('casaos')
    child.expect(pexpect.EOF)
    
    # SSH extraction
    print("Extracting on ZimaBlade...")
    child = pexpect.spawn('ssh casaos@192.168.0.203', encoding='utf-8', timeout=60)
    child.logfile = sys.stdout
    child.expect('password: ')
    child.sendline('casaos')
    child.expect(r'\$')
    
    # Create directory and extract
    child.sendline('sudo mkdir -p /mnt/external_hdd/supabase')
    i = child.expect([r'password for casaos:', r'\$'])
    if i == 0:
        child.sendline('casaos')
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
