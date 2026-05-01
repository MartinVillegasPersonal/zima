import pexpect
import sys

def migrate_and_deploy_openwebui():
    child = pexpect.spawn('ssh casaos@192.168.0.203', encoding='utf-8', timeout=600)
    child.logfile = sys.stdout
    child.expect('password: ')
    child.sendline('casaos')
    child.expect(r'\$')
    
    # 1. Stop Chatbot-UI to save resources
    print("Stopping Chatbot-UI...")
    child.sendline('sudo docker stop chatbot-ui')
    child.expect(r'\$')
    
    # 2. Robust Docker Migration to HDD
    print("Migrating Docker images to HDD (Robust method)...")
    child.sendline('sudo systemctl stop docker.socket && sudo systemctl stop docker')
    child.expect(r'\$')
    
    # Clean up previous failed attempt and prepare
    child.sendline('sudo rm -rf /mnt/external/docker_data_new')
    child.sendline('sudo mkdir -p /mnt/external/docker_data_new')
    # Use -aHAX to preserve everything perfectly
    child.sendline('sudo rsync -aHAX /var/lib/docker/ /mnt/external/docker_data_new/')
    child.expect(r'\$', timeout=600)
    
    # Configure daemon.json
    child.sendline('cat <<EOF | sudo tee /etc/docker/daemon.json\n{\n  "data-root": "/mnt/external/docker_data_new"\n}\nEOF')
    child.expect(r'\$')
    
    # Start Docker
    print("Starting Docker from HDD...")
    child.sendline('sudo systemctl start docker')
    child.expect(r'\$')
    
    # 3. Fix Kong permission if it fails again (proactive)
    print("Fixing entrypoint permissions proactively...")
    child.sendline('sudo find /mnt/external/docker_data_new/overlay2 -name "kong-entrypoint.sh" -exec chmod +x {} +')
    child.expect(r'\$')
    
    # 4. Deploy Open WebUI
    print("Deploying Open WebUI...")
    child.sendline('sudo mkdir -p /mnt/external_hdd/open-webui_data')
    cmd = (
        'sudo docker run -d -p 3001:8080 '
        '--add-host=host.docker.internal:host-gateway '
        '-v /mnt/external_hdd/open-webui_data:/app/backend/data '
        '--name open-webui --restart always '
        'ghcr.io/open-webui/open-webui:main'
    )
    child.sendline(cmd)
    child.expect(r'\$', timeout=600)
    
    # 5. Check status
    child.sendline('sudo docker ps')
    child.expect(r'\$')
    print(child.before)

if __name__ == "__main__":
    migrate_and_deploy_openwebui()
