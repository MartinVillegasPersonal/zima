import subprocess
import os

def push_to_github():
    repo_url = "https://github.com/MartinVillegasPersonal/zima.git"
    scratch_path = "/home/martin/.gemini/antigravity/scratch"
    zima_path = os.path.join(scratch_path, "zima_repo_final")
    
    # Use /bin/sh specifically
    shell_path = "/bin/sh"
    
    commands = [
        f"mkdir -p {zima_path}",
        f"cp {scratch_path}/*.md {zima_path}/",
        f"cp {scratch_path}/v9_*.py {zima_path}/",
        f"cd {zima_path} && git init",
        f"cd {zima_path} && git remote add origin {repo_url}",
        f"cd {zima_path} && git fetch",
        f"cd {zima_path} && git checkout -b main",
        f"cd {zima_path} && git add .",
        f"cd {zima_path} && git commit -m 'Initial upload of ZimaBlade management scripts and docs'",
        f"cd {zima_path} && git push -f origin main"
    ]
    
    for cmd in commands:
        print(f"Running: {cmd}")
        result = subprocess.run([shell_path, "-c", cmd], capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(f"Error: {result.stderr}")

if __name__ == "__main__":
    push_to_github()
