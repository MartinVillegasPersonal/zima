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
    child.sendline('mkdir -p supabase_repo && cd supabase_repo')
    child.expect(r'\$')
    
    child.sendline('git init')
    child.expect(r'\$')
    
    child.sendline('git remote add origin https://github.com/supabase/supabase.git')
    child.expect(r'\$')
    
    child.sendline('git config core.sparseCheckout true')
    child.expect(r'\$')
    
    child.sendline('echo "docker/*" >> .git/info/sparse-checkout')
    child.expect(r'\$')
    
    # Pull ONLY the docker directory
    print("Executing git pull...")
    child.sendline('git pull --depth 1 origin master')
    i = child.expect([r'Username for', r'\$', pexpect.TIMEOUT], timeout=60)
    if i == 0:
        print("Master failed or prompt. Trying main...")
        child.sendcontrol('c')
        child.expect(r'\$')
        child.sendline('git pull --depth 1 origin main')
        child.expect(r'\$', timeout=60)
    
    child.sendline('ls -la docker/')
    child.expect(r'\$')
    
    # If successful, move to supabase folder
    child.sendline('cd .. && mv supabase_repo/docker supabase && rm -rf supabase_repo')
    child.expect(r'\$')
    
    print("Supabase docker folder prepared.")

if __name__ == "__main__":
    sparse_clone()
