import pexpect
import sys

def setup_keys():
    child = pexpect.spawn('ssh casaos@192.168.0.203', encoding='utf-8', timeout=120)
    child.logfile = sys.stdout
    child.expect('password: ')
    child.sendline('casaos')
    child.expect(r'\$')
    
    # Generate keys
    print("Generating keys...")
    child.sendline('cd /mnt/external_hdd/supabase && ./utils/db-passwd.sh casaos')
    child.expect(r'\$')
    
    # Run the automated key generation if it exists or use sed to set some defaults
    # Supabase self-hosted usually requires specific JWT secrets.
    # The utils/generate-keys.sh is often there.
    child.sendline('./utils/generate-keys.sh')
    child.expect(r'\$')
    
    # Now read the generated ANON_KEY
    child.sendline('grep "ANON_KEY=" .env | cut -d "=" -f2')
    child.expect(r'\$')
    # Filter out the command itself from before
    lines = child.before.splitlines()
    anon_key = ""
    for line in lines:
        if line.strip() and "ANON_KEY=" not in line and "grep" not in line:
            anon_key = line.strip()
            break
    
    print(f"FOUND_ANON_KEY: {anon_key}")
    
    # Also need SERVICE_ROLE_KEY just in case
    child.sendline('grep "SERVICE_ROLE_KEY=" .env | cut -d "=" -f2')
    child.expect(r'\$')
    lines = child.before.splitlines()
    service_key = ""
    for line in lines:
        if line.strip() and "SERVICE_ROLE_KEY=" not in line and "grep" not in line:
            service_key = line.strip()
            break
    print(f"FOUND_SERVICE_KEY: {service_key}")

if __name__ == "__main__":
    setup_keys()
