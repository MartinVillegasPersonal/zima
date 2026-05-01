import pexpect
import sys

def reconfigure_portainer():
    child = pexpect.spawn('ssh casaos@192.168.0.203', encoding='utf-8', timeout=120)
    child.logfile = sys.stdout
    child.expect('password: ')
    child.sendline('casaos')
    child.expect(r'\$')
    
    # Remove Portainer
    print("Removing Portainer to reconfigure ports...")
    child.sendline('sudo docker rm -f portainer')
    i = child.expect([r'password for casaos:', r'\$'])
    if i == 0:
        child.sendline('casaos')
        child.expect(r'\$')
    
    # Run Portainer without 8000
    print("Starting Portainer on ports 9000 and 9443...")
    cmd = "sudo docker run -d -p 9000:9000 -p 9443:9443 --name portainer --restart always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce:latest"
    child.sendline(cmd)
    child.expect(r'\$')
    
    print("Portainer reconfigured.")

if __name__ == "__main__":
    reconfigure_portainer()
