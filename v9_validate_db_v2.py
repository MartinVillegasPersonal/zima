import pexpect
import sys

def validate_db_detailed():
    child = pexpect.spawn('ssh casaos@192.168.0.203', encoding='utf-8', timeout=60)
    child.logfile = sys.stdout
    child.expect('password: ')
    child.sendline('casaos')
    child.expect(r'\$')
    
    # Check extensions
    print("Checking extensions...")
    child.sendline('sudo docker exec -i supabase-db psql -U postgres -c "SELECT extname FROM pg_extension;"')
    child.expect(r'\$')
    
    # Check schemas
    print("Checking schemas...")
    child.sendline('sudo docker exec -i supabase-db psql -U postgres -c "SELECT schema_name FROM information_schema.schemata;"')
    child.expect(r'\$')
    
    # Check if auth.users exists (good indicator)
    print("Checking auth.users table...")
    child.sendline('sudo docker exec -i supabase-db psql -U postgres -c "SELECT count(*) FROM auth.users;"')
    child.expect(r'\$')

if __name__ == "__main__":
    validate_db_detailed()
