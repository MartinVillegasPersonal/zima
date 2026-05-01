import pexpect
import sys

def debug_ssh():
    child = pexpect.spawn('ssh casaos@192.168.0.203', encoding='utf-8', timeout=60)
    child.logfile = sys.stdout
    
    i = child.expect(['password: ', 'Are you sure you want to continue connecting', pexpect.EOF, pexpect.TIMEOUT])
    if i == 1:
        child.sendline('yes')
        child.expect('password: ')
        child.sendline('casaos')
    elif i == 0:
        child.sendline('casaos')
    
    child.expect(r'\$')
    
    # Check if we can run sudo
    child.sendline('sudo -v')
    i = child.expect([r'password for casaos:', r'\$'])
    if i == 0:
        child.sendline('casaos')
        child.expect(r'\$')
    
    # Try the clone again with more verbosity
    child.sendline('sudo rm -rf /mnt/external_hdd/supabase')
    child.expect(r'\$')
    
    child.sendline('cd /mnt/external_hdd && git clone --depth 1 https://github.com/supabase/docker.git supabase')
    child.expect(r'\$', timeout=120)
    
    child.sendline('ls -la /mnt/external_hdd/supabase')
    child.expect(r'\$')

if __name__ == "__main__":
    debug_ssh()
