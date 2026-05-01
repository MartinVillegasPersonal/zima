import pexpect
import sys

def final_fix():
    child = pexpect.spawn('ssh casaos@192.168.0.203', encoding='utf-8', timeout=600)
    child.logfile = sys.stdout
    child.expect('password: ')
    child.sendline('casaos')
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
