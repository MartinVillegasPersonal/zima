import pexpect
import sys

def check_script_perms():
    child = pexpect.spawn('ssh casaos@192.168.0.203', encoding='utf-8', timeout=60)
    child.expect('password: ')
    child.sendline('casaos')
    child.expect(r'\$')
    
    child.sendline('ls -la /mnt/external_hdd/supabase/volumes/api/kong-entrypoint.sh')
    child.expect(r'\$')
    print(child.before)
    
    # Also try to set it to executable
    print("Setting +x...")
    child.sendline('chmod +x /mnt/external_hdd/supabase/volumes/api/kong-entrypoint.sh')
    child.expect(r'\$')
    
    child.sendline('ls -la /mnt/external_hdd/supabase/volumes/api/kong-entrypoint.sh')
    child.expect(r'\$')
    print(child.before)

if __name__ == "__main__":
    check_script_perms()
