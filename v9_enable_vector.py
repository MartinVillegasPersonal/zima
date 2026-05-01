import pexpect
import sys

def enable_vector():
    child = pexpect.spawn('ssh casaos@192.168.0.203', encoding='utf-8', timeout=60)
    child.logfile = sys.stdout
    child.expect('password: ')
    child.sendline('casaos')
    child.expect(r'\$')
    
    print("Enabling pgvector...")
    child.sendline('sudo docker exec -i supabase-db psql -U postgres -c "CREATE EXTENSION IF NOT EXISTS vector;"')
    child.expect(r'\$')
    
    print("Verifying extensions again...")
    child.sendline('sudo docker exec -i supabase-db psql -U postgres -c "SELECT extname FROM pg_extension WHERE extname = \'vector\';"')
    child.expect(r'\$')

if __name__ == "__main__":
    enable_vector()
