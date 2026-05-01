import pexpect
import sys

def clone_supabase():
    child = pexpect.spawn('ssh casaos@192.168.0.203', encoding='utf-8', timeout=120)
    child.logfile = sys.stdout
    
    child.expect('password: ')
    child.sendline('casaos')
    child.expect(r'\$')
    
    # Try cloning without prompt
    child.sendline('cd /mnt/external_hdd && sudo rm -rf supabase')
    child.expect(r'\$')
    
    child.sendline('GIT_TERMINAL_PROMPT=0 git clone --depth 1 https://github.com/supabase/docker.git supabase')
    child.expect(r'\$', timeout=120)
    
    child.sendline('ls -la /mnt/external_hdd/supabase')
    child.expect(r'\$')

if __name__ == "__main__":
    clone_supabase()
