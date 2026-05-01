import pexpect

def run():
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
        "sudo docker ps -a",
        "df -h /mnt/external_hdd",
        "free -h",
        "curl -s http://127.0.0.1:11434/api/tags | head -c 200 || echo 'Ollama no responde'",
        "curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:3000 || echo 'Chatbot-UI no responde'"
    ]

    for cmd in commands:
        print(f"\n>>> {cmd}")
        child.sendline(cmd)
        while True:
            i = child.expect([r'\[sudo\] password for casaos:', r'\$', pexpect.TIMEOUT, pexpect.EOF], timeout=30)
            if i == 0:
                child.sendline('casaos')
            elif i == 1:
                break
            else:
                break
        print(child.before)

if __name__ == "__main__":
    run()
