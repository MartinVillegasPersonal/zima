import pexpect
import os
from dotenv import load_dotenv

load_dotenv()
ZIMA_HOST = os.getenv("ZIMA_HOST")
ZIMA_USER = os.getenv("ZIMA_USER")
ZIMA_PASS = os.getenv("ZIMA_PASS")
import sys

def force_pull():
    child = pexpect.spawn(f'ssh {ZIMA_USER}@{ZIMA_HOST}', encoding='utf-8', timeout=1200) # 20 mins
    child.logfile = sys.stdout
    child.expect('password: ')
    child.sendline(ZIMA_PASS)
    child.expect(r'\$')
    
    print("Pulling Open WebUI (this will take time)...")
    child.sendline('sudo docker pull ghcr.io/open-webui/open-webui:main')
    child.expect(r'\$', timeout=1200)
    
    print("Pull finished. Creating container...")
    cmd = (
        'sudo docker run -d -p 3001:8080 '
        '--add-host=host.docker.internal:host-gateway '
        '-v /mnt/external_hdd/open-webui_data:/app/backend/data '
        '--name open-webui --restart always '
        'ghcr.io/open-webui/open-webui:main'
    )
    child.sendline(cmd)
    child.expect(r'\$')
    
    child.sendline('sudo docker ps | grep open-webui')
    child.expect(r'\$')

if __name__ == "__main__":
    force_pull()
