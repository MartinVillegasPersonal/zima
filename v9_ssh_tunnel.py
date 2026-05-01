import pexpect
import sys
import time

def open_tunnel():
    print("Opening SSH Tunnel...")
    # -N means do not execute remote command, just forward ports
    cmd = 'ssh -L 7277:localhost:7277 casaos@192.168.0.203 -N'
    child = pexpect.spawn(cmd, encoding='utf-8', timeout=60)
    
    try:
        child.expect('password: ')
        child.sendline('casaos')
        print("Tunnel established. Keep this running.")
        
        # Keep alive loop
        while True:
            if not child.isalive():
                print("Tunnel lost. Restarting...")
                return
            time.sleep(10)
            
    except pexpect.EOF:
        print("SSH connection closed.")
    except pexpect.TIMEOUT:
        print("SSH connection timed out.")

if __name__ == "__main__":
    open_tunnel()
