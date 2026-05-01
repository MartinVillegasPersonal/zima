import pexpect
import sys

def run_ssh_commands():
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

    # 1. Clean up and Clone
    print("Cleaning and Cloning Supabase...")
    commands = [
        "sudo rm -rf /mnt/external_hdd/supabase",
        "cd /mnt/external_hdd && git clone --depth 1 https://github.com/supabase/docker.git supabase",
        "cd /mnt/external_hdd/supabase && cp .env.example .env"
    ]
    
    for cmd in commands:
        child.sendline(cmd)
        i = child.expect([r'\[sudo\] password for casaos:', r'\$', pexpect.TIMEOUT, pexpect.EOF])
        if i == 0:
            child.sendline('casaos')
            child.expect(r'\$')
    
    # 2. Modify docker-compose.yml
    # We want to replace the volume mapping for the 'db' service.
    # Looking at Supabase docker-compose, it uses:
    # volumes:
    #  - ./volumes/db/init:/docker-entrypoint-initdb.d:ro
    #  - db-data:/var/lib/postgresql/data:Z
    
    print("Modifying docker-compose.yml...")
    # Change the db-data volume to a bind mount
    sed_cmd = "sudo sed -i 's|db-data:/var/lib/postgresql/data|/mnt/external_hdd/supabase_postgres_data:/var/lib/postgresql/data|g' /mnt/external_hdd/supabase/docker-compose.yml"
    child.sendline(sed_cmd)
    child.expect(r'\$')
    
    # Also need to remove the db-data volume definition at the end to avoid errors
    sed_volumes_cmd = "sudo sed -i '/db-data:/d' /mnt/external_hdd/supabase/docker-compose.yml"
    child.sendline(sed_volumes_cmd)
    child.expect(r'\$')

    print("Supabase prepared.")

if __name__ == "__main__":
    run_ssh_commands()
