import pexpect
import os
from dotenv import load_dotenv

load_dotenv()
ZIMA_HOST = os.getenv("ZIMA_HOST")
ZIMA_USER = os.getenv("ZIMA_USER")
ZIMA_PASS = os.getenv("ZIMA_PASS")
import sys

def restart_services():
    child = pexpect.spawn(f'ssh {ZIMA_USER}@{ZIMA_HOST}', encoding='utf-8', timeout=600)
    child.logfile = sys.stdout
    child.expect('password: ')
    child.sendline(ZIMA_PASS)
    child.expect(r'\$')
    
    # 1. Restart Supabase
    print("Restarting Supabase to apply keys...")
    child.sendline('cd /mnt/external_hdd/supabase && sudo docker compose up -d')
    i = child.expect([r'password for {ZIMA_USER}:', r'Running'], timeout=30)
    if i == 0:
        child.sendline(ZIMA_PASS)
    child.expect(r'\$', timeout=600)
    
    # 2. Restart Chatbot-UI
    print("Reconfiguring Chatbot-UI...")
    anon_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYW5vbiIsImlzcyI6InN1cGFiYXNlIiwiaWF0IjoxNzc3NjA0NTU0LCJleHAiOjE5MzUyODQ1NTR9.YaKNsOKOy0ttcbPfeOcb1fnxh7u9KcsmsJbxTIIhQ8o"
    
    commands = [
        "sudo docker stop chatbot-ui",
        "sudo docker rm chatbot-ui",
        f"sudo docker run -d -p 3000:3000 --name chatbot-ui --restart always -e NEXT_PUBLIC_SUPABASE_URL=http://192.168.0.203:8000 -e NEXT_PUBLIC_SUPABASE_ANON_KEY={anon_key} -e OLLAMA_HOST=http://192.168.0.203:11434 ghcr.io/mckaywrigley/chatbot-ui:main"
    ]
    
    for cmd in commands:
        child.sendline(cmd)
        child.expect(r'\$')
    
    print("Services restarted successfully.")

if __name__ == "__main__":
    restart_services()
