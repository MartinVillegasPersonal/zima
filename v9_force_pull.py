import pexpect
import sys

def force_pull():
    child = pexpect.spawn('ssh casaos@192.168.0.203', encoding='utf-8', timeout=1200) # 20 mins
    child.logfile = sys.stdout
    child.expect('password: ')
    child.sendline('casaos')
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
