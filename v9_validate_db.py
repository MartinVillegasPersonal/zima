import pexpect
import sys

def validate_db():
    child = pexpect.spawn('ssh casaos@192.168.0.203', encoding='utf-8', timeout=60)
    child.logfile = sys.stdout
    child.expect('password: ')
    child.sendline('casaos')
    child.expect(r'\$')
    
    # Connect to postgres container and list tables
    print("Checking tables in 'postgres' database...")
    child.sendline('sudo docker exec -it supabase-db psql -U postgres -c "\\dt"')
    child.expect(r'\$')
    
    # Check pgvector
    print("Checking pgvector extension...")
    child.sendline('sudo docker exec -it supabase-db psql -U postgres -c "SELECT * FROM pg_extension WHERE extname = \'vector\';"')
    child.expect(r'\$')
    
    print("Validation finished.")

if __name__ == "__main__":
    validate_db()
