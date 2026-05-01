import pexpect
import sys

def sparse_clone():
    child = pexpect.spawn('ssh casaos@192.168.0.203', encoding='utf-8', timeout=300)
    child.logfile = sys.stdout
    
    child.expect('password: ')
    child.sendline('casaos')
    child.expect(r'\$')
    
    child.sendline('cd /mnt/external_hdd && sudo rm -rf supabase_repo')
    child.expect(r'\$')
    
    # Sparse clone
    print("Starting sparse clone...")
    child.sendline('mkdir -p supabase_repo && cd supabase_repo')
    child.expect(r'\$')
    
    # We might need to initialize git first
    child.sendline('git init')
    child.expect(r'\$')
    
    child.sendline('git remote add origin https://github.com/supabase/supabase.git')
    child.expect(r'\$')
    
    child.sendline('git config core.sparseCheckout true')
    child.expect(r'\$')
    
    # Echo the directory to sparse checkout
    child.sendline('echo "docker/*" >> .git/info/sparse-checkout')
    child.expect(r'\$')
    
    # Pull ONLY the docker directory
    print("Pulling docker directory...")
    child.sendline('git pull --depth 1 origin master || git pull --depth 1 origin main')
    i = child.expect([r'Username for', r'\$', pexpect.TIMEOUT], timeout=120)
    if i == 0:
        print("Still asking for credentials. Switching to ZIP method with correct URL.")
        child.sendcontrol('c')
        child.expect(r'\$')
    
    # Check if files are there
    child.sendline('ls -la docker/')
    child.expect(r'\$')

if __name__ == "__main__":
    sparse_clone()
