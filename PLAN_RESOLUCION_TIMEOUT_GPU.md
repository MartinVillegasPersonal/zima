# Plan de Trabajo: Solución Definitiva de Carga de Modelos en GPU (RTX 5050) post-reinicio en ZimaBlade

## 📌 Contexto y Diagnóstico del Problema

Cada vez que la ZimaBlade se reinicia, todos los contenedores Docker del stack (Supabase, Postgres, Redis, Kong, Chatbot UI, Portainer, Uptime Kuma, Open WebUI, Sich MCP y Ollama) intentan iniciar simultáneamente. Esto genera un pico de uso de CPU del 100% en el procesador integrado (Intel Celeron).

Durante este pico de carga y en el arranque inicial del sistema:
1. El driver de NVIDIA y el toolkit de Docker tardan unos segundos en inicializar la GPU RTX 5050.
2. Ollama arranca e intenta realizar el auto-descubrimiento de la GPU mediante la inicialización del contexto de CUDA.
3. Debido a la alta carga de CPU y la inicialización lenta del hardware, el proceso de descubrimiento supera el timeout interno de Ollama (30 segundos).
4. Logs de error detectados:
   `failure during GPU discovery ... error="failed to finish discovery before timeout"`
5. Al no detectar la GPU a tiempo, Ollama desactiva el backend de CUDA por completo para esa sesión y arranca en modo **CPU**.
6. Consecuentemente, el modelo `llava:v1.6` se carga en la memoria RAM del sistema y se ejecuta de forma extremadamente lenta en el CPU, a pesar de que la GPU esté encendida y activa más tarde.

---

## 🔍 Evaluación de Alternativas

### Alternativa A: Instalar la app "Ollama(Nvidia GPU)" desde la App Store de CasaOS
* **Descripción:** Reemplazar el contenedor actual por la versión empaquetada de la tienda de aplicaciones de CasaOS para GPUs NVIDIA.
* **Pros:**
  * Configuración visualmente integrada en CasaOS.
* **Cons:**
  * **No soluciona el problema de raíz:** Bajo el capó, esa app usa la misma imagen oficial de Ollama (`ollama/ollama`) y la configuración estándar de Docker Nvidia, por lo que seguirá sufriendo el timeout de 30 segundos durante la alta carga de CPU del arranque.
  * **Pérdida de persistencia personalizada:** Perderíamos el mapeo actual de los modelos en el HDD externo de 1 TB (`/mnt/external_hdd/ollama_models` y `/mnt/external_hdd/ollama-nvidia`) a menos que reconfiguremos manualmente los volúmenes del contenedor.
  * **Menos flexibilidad:** Dificulta la inyección de scripts personalizados en el punto de entrada.

### Alternativa B: Implementar un Punto de Entrada (Entrypoint) Robusto con Retardo y Verificación Dinámica (Recomendada)
* **Descripción:** Modificar el `docker-compose.yml` actual de `ollama-nvidia` para mejorar el script de `entrypoint`. Este script verificará activamente la disponibilidad de la GPU mediante un bucle de reintentos y, una vez detectada, esperará un tiempo de cortesía (30-45 segundos) para permitir que el uso de CPU de los otros servicios se estabilice antes de ceder el control a `ollama serve`.
* **Pros:**
  * **Solución definitiva y persistente:** Garantiza que la GPU esté lista y que la carga de CPU del sistema haya bajado antes de que Ollama intente el descubrimiento.
  * **Sin pérdida de datos:** Preserva intactos los volúmenes en el disco externo de 1 TB.
  * **Mantenimiento simple:** Se realiza editando únicamente el archivo de Compose actual.
* **Cons:**
  * Añade unos ~45 segundos adicionales de retardo en la disponibilidad de Ollama después de un reinicio completo (lo cual es aceptable, ya que los reinicios son poco frecuentes y asegura el uso de la GPU).

---

## 🛠️ Plan de Trabajo

### Paso 1: Documentación del Plan
Crear y guardar este documento (`PLAN_RESOLUCION_TIMEOUT_GPU.md`) en el repositorio local de Zima para mantener la trazabilidad de la arquitectura.

### Paso 2: Modificación del `docker-compose.yml` en la ZimaBlade
Modificar el servicio `ollama` en `/var/lib/casaos/apps/ollama-nvidia/docker-compose.yml` sustituyendo el entrypoint actual por el script de verificación y enfriamiento dinámico (basado en la carga de CPU real del host mediante `/proc/loadavg`):

```yaml
entrypoint: 
  - "sh"
  - "-c"
  - |
    echo '=== Iniciando verificación GPU ==='
    for i in $$(seq 1 30); do
      if nvidia-smi > /dev/null 2>&1; then
        echo 'GPU activa'
        break
      fi
      echo 'Esperando driver...'
      sleep 2
    done
    nvidia-smi > /dev/null 2>&1 || (echo 'ERROR: GPU no responde' && exit 1)
    echo '=== Esperando a que la carga del CPU baje post-boot ==='
    for i in $$(seq 1 30); do
      load_int=$$(cut -d. -f1 /proc/loadavg)
      echo "Carga de CPU actual: $$load_int (intento $$i/30)"
      if [ "$$load_int" -lt 8 ]; then
        echo "Carga de CPU aceptable ($$load_int < 8). Procediendo..."
        break
      fi
      sleep 5
    done
    exec ollama serve
```

> 💡 **Nota de Diseño:** Se cambió el delay estático de 30 segundos a una verificación dinámica basada en la carga de CPU porque, al arrancar la ZimaBlade, el stack completo de Supabase realiza migraciones de base de datos y levantamiento de contenedores pesados. Esto eleva la carga del CPU (`load average`) por encima de 24 durante los primeros 90 segundos. El bucle dinámico monitorea `/proc/loadavg` y solo permite el inicio de Ollama cuando la carga del procesador baja de 8 (o tras un timeout máximo de 150 segundos), garantizando el éxito del descubrimiento de CUDA sin timeouts.

### Paso 3: Aplicar Cambios y Desplegar
Conectarse por SSH a la ZimaBlade y ejecutar el despliegue del stack modificado para aplicar los cambios del entrypoint.
```bash
cd /var/lib/casaos/apps/ollama-nvidia/
sudo docker compose down
sudo docker compose up -d
```

### Paso 4: Pruebas de Validación
1. Confirmar en los logs del contenedor que se ejecute la secuencia de espera y el inicio exitoso de Ollama:
   ```bash
   sudo docker logs ollama --tail 50
   ```
2. Verificar mediante `nvidia-smi` en el host que el proceso de Ollama esté registrado y consumiendo memoria VRAM.
3. Forzar un reinicio físico de la ZimaBlade para simular un inicio frío.
4. Esperar 2 minutos tras el encendido y comprobar que `ollama ps` liste los modelos en la GPU (`100% GPU`) automáticamente, sin necesidad de reinicios manuales del contenedor.

### Paso 5: Confirmación y Commit en Git
Añadir y empujar los cambios de documentación en el repositorio local `zima`.
