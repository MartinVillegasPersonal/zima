import pexpect
import sys

def get_branch():
    child = pexpect.spawn('ssh casaos@192.168.0.203', encoding='utf-8', timeout=60)
    
    child.expect('password: ')
    child.sendline('casaos')
    child.expect(r'\$')
    
    child.sendline('git ls-remote --symref https://github.com/supabase/docker.git HEAD')
    child.expect(r'\$')
    print(child.before)

if __name__ == "__main__":
    get_branch()
