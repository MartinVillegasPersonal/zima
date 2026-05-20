import pexpect
import sys

def setup_ollama():
    ip = '192.168.0.203'
    user = 'casaos'
    password = 'casaos'
    
    child = pexpect.spawn(f'ssh -o StrictHostKeyChecking=no {user}@{ip}', encoding='utf-8', timeout=60)
    # child.logfile = sys.stdout # Descomentar para debug
    
    try:
        child.expect('password: ')
        child.sendline(password)
        child.expect(r'\$')
        
        print("Conectado a ZimaBlade.")
        
        # 1. Ver estado actual de Ollama
        print("Revisando contenedor Ollama...")
        child.sendline('docker inspect ollama --format "{{json .Mounts}}"')
        child.expect(r'\$')
        mounts = child.before.strip()
        print(f"Montajes actuales: {mounts}")
        
        # 2. Ver si hay modelos en el HDD
        print("Buscando modelos en HDD...")
        child.sendline('ls -R /mnt/external_hdd/ollama/models 2>/dev/null | head -n 20')
        child.expect(r'\$')
        models = child.before.strip()
        print(f"Modelos encontrados:\n{models}")
        
        # 3. Eliminar contenedor viejo para recrear con GPU
        print("Eliminando contenedor viejo (si existe)...")
        child.sendline('docker rm -f ollama')
        child.expect(r'\$')
        
        # 4. Crear nuevo contenedor Ollama con GPU Blackwell y entrypoint robusto post-boot.
        # ADVERTENCIA: No eliminar el --entrypoint ni el retardo de 30s. Evita el fallback a CPU
        # en reinicios causado por la alta carga de CPU y la lenta inicialización del driver.
        print("Creando nuevo contenedor Ollama con soporte GPU Blackwell...")
        ollama_cmd = (
            "docker run -d "
            "--name ollama "
            "--restart always "
            "--gpus all "
            "-v /mnt/external_hdd/ollama:/root/.ollama "
            "-p 11434:11434 "
            "--entrypoint sh "
            "ollama/ollama -c "
            "\"echo '=== Iniciando verificación GPU ===' && "
            "for i in \\$(seq 1 30); do "
            "if nvidia-smi > /dev/null 2>&1; then echo 'GPU activa'; break; fi; "
            "echo 'Esperando driver...'; sleep 2; done; "
            "nvidia-smi > /dev/null 2>&1 || (echo 'ERROR: GPU no responde' && exit 1); "
            "echo '=== Esperando a que la carga del CPU baje post-boot ===' && "
            "for i in \\$(seq 1 30); do "
            "load_int=\\$(cut -d. -f1 /proc/loadavg); "
            "echo \\\"Carga de CPU actual: \\$load_int (intento \\$i/30)\\\"; "
            "if [ \\\"\\$load_int\\\" -lt 8 ]; then "
            "echo \\\"Carga de CPU aceptable (\\$load_int < 8). Procediendo...\\\"; "
            "break; fi; sleep 5; done; "
            "exec ollama serve\""
        )
        child.sendline(ollama_cmd)
        child.expect(r'\$')
        print(f"Contenedor creado: {child.before.strip()}")
        
        # 5. Esperar a que inicie y verificar logs
        print("Esperando arranque...")
        import time
        time.sleep(5)
        child.sendline('docker logs ollama | tail -n 10')
        child.expect(r'\$')
        logs = child.before.strip()
        print(f"Logs de Ollama:\n{logs}")
        
        if "nvidia" in logs.lower() or "gpu" in logs.lower() or "cuda" in logs.lower():
             print("✅ Ollama detectó la GPU NVIDIA.")
        else:
             print("⚠️ Advertencia: No se detectó GPU en los logs iniciales. Verificando más a fondo...")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        child.close()

if __name__ == "__main__":
    setup_ollama()
