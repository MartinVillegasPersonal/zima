import pexpect
import sys

def deploy_supabase():
    child = pexpect.spawn('ssh casaos@192.168.0.203', encoding='utf-8', timeout=600)
    child.logfile = sys.stdout
    child.expect('password: ')
    child.sendline('casaos')
    child.expect(r'\$')
    
    # 1. Config .env
    child.sendline('cd /mnt/external_hdd/supabase && cp .env.example .env')
    child.expect(r'\$')
    
    # 2. Modify docker-compose.yml
    # Replace the volumes section for 'db' service
    # From:
    #   db:
    #     ...
    #     volumes:
    #       - ./volumes/db/init:/docker-entrypoint-initdb.d:ro
    #       - db-data:/var/lib/postgresql/data:Z
    # To use a bind mount to the HDD
    
    print("Modifying docker-compose.yml...")
    # Change the volume mapping
    child.sendline("sed -i 's|db-data:/var/lib/postgresql/data|/mnt/external_hdd/supabase_postgres_data:/var/lib/postgresql/data|g' docker-compose.yml")
    child.expect(r'\$')
    
    # Remove the named volume definition at the end
    child.sendline("sed -i '/db-data:/d' docker-compose.yml")
    child.expect(r'\$')
    
    # 3. Deploy
    print("Starting Docker Compose...")
    child.sendline('sudo docker compose up -d')
    i = child.expect([r'password for casaos:', r'Running'], timeout=30)
    if i == 0:
        child.sendline('casaos')
    
    # This might take a long time to pull images
    print("Waiting for containers to start (this can take 5-10 mins)...")
    child.expect(r'\$', timeout=600)
    
    child.sendline('sudo docker ps')
    child.expect(r'\$')
    
    print("Supabase deployment command finished.")

if __name__ == "__main__":
    deploy_supabase()
