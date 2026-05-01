import pexpect
import sys

def cleanup_vaultwarden():
    child = pexpect.spawn('ssh casaos@192.168.0.203', encoding='utf-8', timeout=60)
    child.expect('password: ')
    child.sendline('casaos')
    child.expect(r'\$')
    
    print("Cleaning up Vaultwarden...")
    child.sendline('sudo docker rm -f vaultwarden')
    child.expect(r'\$')
    
    # Optional: remove data directory? 
    # Better keep it for now in case user changes mind, or delete if they want.
    # I will just stop and remove the container for now.
    
    print("Vaultwarden removed. System clean.")

if __name__ == "__main__":
    cleanup_vaultwarden()
