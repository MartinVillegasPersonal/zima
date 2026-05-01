import pexpect

def run_diagnostics():
    child = pexpect.spawn('ssh casaos@192.168.0.203', encoding='utf-8', timeout=60)
    
    i = child.expect(['password: ', 'Are you sure you want to continue connecting', pexpect.EOF, pexpect.TIMEOUT])
    if i == 1:
        child.sendline('yes')
        child.expect('password: ')
        child.sendline('casaos')
    elif i == 0:
        child.sendline('casaos')
    else:
        print("Failed to connect.")
        return

    child.expect(r'\$')

    commands = [
        "docker-compose --version || docker compose version",
        "ls -la /mnt/external_hdd",
        "docker ps"
    ]
    
    for cmd in commands:
        print(f"Executing: {cmd}")
        child.sendline(cmd)
        child.expect(r'\$')
        print(child.before)
        print("-" * 20)

if __name__ == "__main__":
    run_diagnostics()
