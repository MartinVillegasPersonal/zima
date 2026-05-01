import pexpect

def run():
    child = pexpect.spawn('ssh casaos@192.168.0.203', encoding='utf-8', timeout=120)
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
        # Paso 2: Crear directorios
        "echo 'casaos' | sudo -S mkdir -p /mnt/external_hdd/supabase_postgres_data",
        "echo 'casaos' | sudo -S chown -R casaos:casaos /mnt/external_hdd/supabase_postgres_data",
        "ls -la /mnt/external_hdd/",
    ]

    for cmd in commands:
        print(f"\n>>> {cmd}")
        child.sendline(cmd)
        while True:
            i = child.expect([r'\[sudo\] password for casaos:', r'\$', pexpect.TIMEOUT, pexpect.EOF], timeout=60)
            if i == 0:
                child.sendline('casaos')
            elif i == 1:
                break
            else:
                break
        print(child.before)

if __name__ == "__main__":
    run()
