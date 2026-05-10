import pexpect
import os
from dotenv import load_dotenv

load_dotenv()
ZIMA_HOST = os.getenv("ZIMA_HOST")
ZIMA_USER = os.getenv("ZIMA_USER")
ZIMA_PASS = os.getenv("ZIMA_PASS")
import sys

def final_fix():
    child = pexpect.spawn(f'ssh {ZIMA_USER}@{ZIMA_HOST}', encoding='utf-8', timeout=600)
    child.logfile = sys.stdout
    child.expect('password: ')
    child.sendline(ZIMA_PASS)
    child.expect(r'\$')
    
    # 1. Pull and Run Open WebUI again (now in the correct persistent path)
    print("Redeploying Open WebUI in persistent path...")
    cmd = (
        'sudo docker run -d -p 3001:8080 '
        '--add-host=host.docker.internal:host-gateway '
        '-v /mnt/external_hdd/open-webui_data:/app/backend/data '
        '--name open-webui --restart always '
        'ghcr.io/open-webui/open-webui:main'
    )
    child.sendline(cmd)
    child.expect(r'\$')
    
    # 2. Fix Supabase Kong
    print("Fixing Supabase Kong...")
    child.sendline('sudo docker start supabase-kong')
    child.expect(r'\$')
    
    # 3. Check
    child.sendline('sudo docker ps')
    child.expect(r'\$')

if __name__ == "__main__":
    final_fix()
