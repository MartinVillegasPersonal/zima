import pexpect
import sys
import time
import requests

def setup_ollama():
    ip = '192.168.0.203'
    user = 'casaos'
    password = 'casaos'
    webhook_url = "https://gi4w1f6xxevmeebulyfpapmhlowq83v6.ui.nabu.casa/api/webhook/notificacion_secreta_pro"
    
    def notify(msg):
        print(f"NOTIFY: {msg}")
        try:
            requests.post(webhook_url, json={"message": msg})
        except:
            pass

    child = pexpect.spawn(f'ssh -o StrictHostKeyChecking=no {user}@{ip}', encoding='utf-8', timeout=60)
    
    try:
        child.expect('password: ')
        child.sendline(password)
        child.expect(r'\$')
        
        notify("🛠️ Re-configurando contenedor Ollama con acceso a GPU Blackwell y modelos en HDD.")
        
        # 1. Eliminar contenedor existente
        print("Eliminando contenedor previo...")
        child.sendline('sudo docker rm -f ollama')
        child.expect(['password for casaos:', r'\$'])
        if 'password' in child.after:
            child.sendline(password)
            child.expect(r'\$')
        
        # 2. Crear el nuevo contenedor con entrypoint robusto para evitar el timeout de CUDA post-boot.
        # ADVERTENCIA: No eliminar el --entrypoint ni el retardo de 30s. Sin esto, Ollama
        # fallará la detección de la GPU durante picos de CPU al reiniciar y revertirá a CPU.
        print("Lanzando Ollama con GPU...")
        ollama_cmd = (
            "sudo docker run -d "
            "--name ollama "
            "--restart always "
            "--gpus all "
            "-v /mnt/external_hdd/ollama_models:/root/.ollama/models "
            "-p 11434:11434 "
            "--entrypoint sh "
            "ollama/ollama -c "
            "\"echo '=== Iniciando verificación GPU ===' && "
            "for i in \\$(seq 1 30); do "
            "if nvidia-smi > /dev/null 2>&1; then echo 'GPU activa'; break; fi; "
            "echo 'Esperando driver...'; sleep 2; done; "
            "nvidia-smi > /dev/null 2>&1 || (echo 'ERROR: GPU no responde' && exit 1); "
            "echo 'Esperando 30s para estabilizar CPU...'; sleep 30; "
            "exec ollama serve\""
        )
        child.sendline(ollama_cmd)
        child.expect(r'\$')
        
        notify("✅ Contenedor Ollama iniciado. Esperando inicialización de GPU...")
        time.sleep(10)
        
        # 3. Verificar si detectó la GPU
        child.sendline('sudo docker logs ollama')
        child.expect(r'\$')
        logs = child.before
        if "nvidia" in logs.lower() or "cuda" in logs.lower():
            notify("🚀 GPU NVIDIA detectada correctamente por Ollama.")
        else:
            notify("⚠️ Alerta: Ollama no parece haber detectado la GPU en los logs. Revisando configuración.")

        # 4. Listar modelos cargados
        print("Listando modelos...")
        child.sendline('sudo docker exec ollama ollama list')
        child.expect(r'\$')
        model_list = child.before.strip()
        print(f"Modelos:\n{model_list}")
        
        # 5. Si hay modelos, hacer que uno se presente
        lines = model_list.splitlines()
        if len(lines) > 1: # La primera es el header
            first_model = lines[1].split()[0]
            notify(f"🤖 Modelo detectado: {first_model}. Solicitando presentación...")
            
            # Comando para que el modelo se presente
            presentation_cmd = f'sudo docker exec ollama ollama run {first_model} "Preséntate brevemente al sistema SICH, confirma que tienes acceso a la GPU Blackwell y que tus datos están en el HDD de 1TB."'
            child.sendline(presentation_cmd)
            # Esto puede tardar
            child.expect(r'\$', timeout=120)
            presentation_text = child.before.strip()
            
            # Limpiar el texto (quitar el comando eco)
            clean_text = "\n".join(presentation_text.splitlines()[1:])
            notify(f"📢 Presentación de Ollama:\n{clean_text}")
        else:
            notify("❌ No se encontraron modelos pre-descargados en /mnt/external_hdd/ollama_models.")

    except Exception as e:
        notify(f"❌ Error en la configuración: {str(e)}")
    finally:
        child.close()

if __name__ == "__main__":
    setup_ollama()
