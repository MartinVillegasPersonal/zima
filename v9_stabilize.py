import pexpect
import sys

def stabilize():
    child = pexpect.spawn('ssh casaos@192.168.0.203', encoding='utf-8', timeout=60)
    child.expect('password: ')
    child.sendline('casaos')
    child.expect(r'\$')
    
    # 1. Restart all existing containers
    print("Restarting Supabase and others...")
    child.sendline('sudo docker start $(sudo docker ps -a -q)')
    child.expect(r'\$')
    
    # 2. Launch Open WebUI pull in background (nohup)
    print("Launching Open WebUI pull in background...")
    child.sendline('nohup sudo docker pull ghcr.io/open-webui/open-webui:main > /dev/null 2>&1 &')
    child.expect(r'\$')
    
    print("Stabilization command sent.")

if __name__ == "__main__":
    stabilize()
