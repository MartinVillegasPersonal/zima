import pexpect
import sys

def deploy_openwebui():
    child = pexpect.spawn('ssh casaos@192.168.0.203', encoding='utf-8', timeout=600)
    child.logfile = sys.stdout
    child.expect('password: ')
    child.sendline('casaos')
    child.expect(r'\$')
    
    # 1. Pull first to avoid timeout during run
    print("Pulling Open WebUI image...")
    child.sendline('sudo docker pull ghcr.io/open-webui/open-webui:main')
    child.expect(r'\$', timeout=600)
    
    # 2. Run
    print("Starting Open WebUI...")
    cmd = (
        'sudo docker run -d -p 3001:8080 '
        '--add-host=host.docker.internal:host-gateway '
        '-v /mnt/external_hdd/open-webui_data:/app/backend/data '
        '--name open-webui --restart always '
        'ghcr.io/open-webui/open-webui:main'
    )
    child.sendline(cmd)
    child.expect(r'\$')
    
    # 3. Check status
    child.sendline('sudo docker ps | grep open-webui')
    child.expect(r'\$')

if __name__ == "__main__":
    deploy_openwebui()
