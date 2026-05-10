import pexpect
import os
from dotenv import load_dotenv

load_dotenv()
ZIMA_HOST = os.getenv("ZIMA_HOST")
ZIMA_USER = os.getenv("ZIMA_USER")
ZIMA_PASS = os.getenv("ZIMA_PASS")
import sys

def setup_samba():
    child = pexpect.spawn(f'ssh {ZIMA_USER}@{ZIMA_HOST}', encoding='utf-8', timeout=300)
    child.logfile = sys.stdout
    child.expect('password: ')
    child.sendline(ZIMA_PASS)
    child.expect(r'\$')
    
    # 1. Install Samba
    print("Installing Samba...")
    child.sendline('sudo apt update && sudo apt install -y samba')
    child.expect(r'\$')
    
    # 2. Add Samba user (casaos) with password (casaos)
    print("Setting Samba password for user 'casaos'...")
    child.sendline('sudo smbpasswd -a casaos')
    child.expect('New SMB password:')
    child.sendline(ZIMA_PASS)
    child.expect('Retype new SMB password:')
    child.sendline(ZIMA_PASS)
    child.expect(r'\$')
    
    # 3. Configure Share
    print("Configuring SICH share...")
    smb_config = """
[SICH_Data]
   path = /mnt/external_hdd
   browseable = yes
   read only = no
   guest ok = no
   valid users = casaos
   create mask = 0775
   directory mask = 0775
"""
    # Append to smb.conf
    child.sendline("cat <<EOF | sudo tee -a /etc/samba/smb.conf")
    child.sendline(smb_config)
    child.sendline("EOF")
    child.expect(r'\$')
    
    # 4. Restart Samba
    print("Restarting Samba...")
    child.sendline('sudo systemctl restart smbd nmbd')
    child.expect(r'\$')
    
    print("SAMBA setup complete.")

if __name__ == "__main__":
    setup_samba()
