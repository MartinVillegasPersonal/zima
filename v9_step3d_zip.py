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
        "mkdir -p /mnt/external_hdd/supabase",
        "curl -L https://github.com/supabase/docker/archive/refs/heads/master.zip -o /tmp/supabase.zip && echo 'DL_OK'",
        "echo 'casaos' | sudo -S apt-get install -y unzip -q && echo 'UNZIP_INSTALLED'",
        "unzip -q /tmp/supabase.zip -d /tmp/supabase_extract && echo 'UNZIP_OK'",
        "cp -r /tmp/supabase_extract/docker-master/. /mnt/external_hdd/supabase/ && echo 'COPY_OK'",
        "ls /mnt/external_hdd/supabase/",
        "cp /mnt/external_hdd/supabase/.env.example /mnt/external_hdd/supabase/.env && echo 'ENV_OK'"
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
