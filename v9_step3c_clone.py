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

    print("\n>>> Configurando git sin credenciales y clonando...")
    child.sendline("git config --global credential.helper '' && GIT_TERMINAL_PROMPT=0 git clone --depth 1 https://github.com/supabase/docker.git /mnt/external_hdd/supabase 2>&1 && echo 'CLONE_OK' || echo 'CLONE_FAIL'")
    while True:
        i = child.expect([r'CLONE_OK', r'CLONE_FAIL', r'Username', r'\$', pexpect.TIMEOUT, pexpect.EOF], timeout=180)
        if i == 0:
            print("CLONE OK!")
            child.expect(r'\$')
            break
        elif i == 2:
            print("Credential prompt - cancelling...")
            child.sendcontrol('c')
            child.expect(r'\$')
            break
        elif i in [1, 3]:
            break
        elif i in [4, 5]:
            print("TIMEOUT/EOF")
            break
    print(child.before)

    print("\n>>> Copiando .env.example...")
    child.sendline("cp /mnt/external_hdd/supabase/.env.example /mnt/external_hdd/supabase/.env && echo 'ENV_OK'")
    child.expect(r'\$', timeout=15)
    print(child.before)

    print("\n>>> Verificando contenido del directorio supabase...")
    child.sendline("ls /mnt/external_hdd/supabase/")
    child.expect(r'\$', timeout=15)
    print(child.before)

if __name__ == "__main__":
    run()
