import pexpect

def run():
    child = pexpect.spawn('ssh casaos@192.168.0.203', encoding='utf-8', timeout=300)
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
        "echo 'casaos' | sudo -S chown -R casaos:casaos /mnt/external_hdd",
        "ls -la /mnt/external_hdd/",
        "git clone --depth 1 https://github.com/supabase/docker.git /mnt/external_hdd/supabase && echo 'CLONE_OK'",
    ]

    for cmd in commands:
        print(f"\n>>> {cmd}")
        child.sendline(cmd)
        while True:
            i = child.expect([r'\[sudo\] password for casaos:', r'\$', pexpect.TIMEOUT, pexpect.EOF], timeout=180)
            if i == 0:
                child.sendline('casaos')
            elif i == 1:
                break
            else:
                print("TIMEOUT/EOF")
                break
        print(child.before)

if __name__ == "__main__":
    run()
