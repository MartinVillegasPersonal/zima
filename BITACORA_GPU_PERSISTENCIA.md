# Bitácora de Incidencias: Resolución de Carga de Modelos en CPU y Timeout de GPU

## 📌 Identificación del Problema
* **Fecha:** 17 de Mayo de 2026 (Local) / 18 de Mayo de 2026 (UTC)
* **Servidor:** ZimaBlade (S.I.C.H. Infrastructure Stack)
* **Sintomatología:** Al iniciar conversaciones o realizar consultas en Open WebUI / Chatbot-UI, el sistema respondía con extrema lentitud. Al analizar el proceso, se detectó que el modelo se estaba ejecutando en el **CPU** en lugar de utilizar la aceleración por hardware de la GPU dedicada. 
* **Tiempos de carga observados:**
  * **Carga en CPU:** **257.76 segundos** (~4.3 minutos)
  * **Carga en GPU (Esperada):** **~25 segundos**

---

## 🔍 Diagnóstico Técnico
Al conectarse de forma remota a la ZimaBlade y ejecutar el escaneo de logs del contenedor de Ollama, se identificó el siguiente mensaje recurrente durante la secuencia de inicio:

```text
time=2026-05-18T02:46:14.775Z level=INFO source=runner.go:67 msg="discovering available GPUs..."
time=2026-05-18T02:46:44.793Z level=INFO source=runner.go:462 msg="failure during GPU discovery" OLLAMA_LIBRARY_PATH="[/usr/lib/ollama /usr/lib/ollama/cuda_v12]" error="failed to finish discovery before timeout"
time=2026-05-18T02:47:14.821Z level=INFO source=runner.go:462 msg="failure during GPU discovery" OLLAMA_LIBRARY_PATH="[/usr/lib/ollama /usr/lib/ollama/cuda_v13]" error="failed to finish discovery before timeout"
time=2026-05-18T02:47:15.034Z level=WARN source=cpu_linux.go:130 msg="failed to parse CPU allowed micro secs"
```

### 💡 Causa Raíz
1. **Persistence Mode Inactivo:** Al realizar la consulta directa a `nvidia-smi` en el host, se constató que el modo de persistencia estaba apagado (`Persistence-M: Off`).
2. **Ciclo de Suspensión de la GPU:** Cuando no hay clientes de renderizado o computación activos, el controlador de NVIDIA descarga por completo los módulos y apaga físicamente la tarjeta gráfica para reducir el consumo eléctrico.
3. **Timeout de Descubrimiento:** En hardware embebido o de bajo consumo como la ZimaBlade, el tiempo que requiere el controlador de NVIDIA para inicializar el chip gráfico, cargar el firmware GSP y enlazar las librerías CUDA desde el estado de reposo supera el límite fijo de descubrimiento que Ollama tiene configurado (30 segundos). Como consecuencia, el proceso interno de Ollama falla por *timeout*, asume que no hay GPU compatible disponible y revierte silenciosamente al modo CPU.

---

## 🛠️ Solución Aplicada

### Paso 1: Activación Manual del Persistence Mode
Se forzó al driver a mantener la GPU despierta y las librerías en caché permanentemente con el siguiente comando en el host:
```bash
sudo nvidia-smi -pm 1
```
*Resultado:* `Enabled Legacy persistence mode for GPU 00000000:01:00.0.`

### Paso 2: Automatización Permanente en el Host
Para garantizar que esta optimización sobreviva a reinicios y apagados físicos de la ZimaBlade, se diseñó e implementó un servicio de sistema personalizado en el path `/etc/systemd/system/nvidia-persistence-mode.service`:

```ini
[Unit]
Description=Enable NVIDIA Persistence Mode
After=syslog.target network.target
Before=docker.service

[Service]
Type=oneshot
ExecStart=/usr/bin/nvidia-smi -pm 1
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
```

* **Explicación del Flujo:** El servicio se ejecuta inmediatamente después de levantar la red/logs (`After=syslog.target network.target`) y estrictamente **antes** de que comience el demonio de Docker (`Before=docker.service`). Esto asegura que cuando Ollama arranque dentro de Docker, la GPU ya esté despierta y lista.
* **Habilitación en el sistema:**
  ```bash
  sudo systemctl daemon-reload
  sudo systemctl enable nvidia-persistence-mode.service
  sudo systemctl start nvidia-persistence-mode.service
  ```

---

## 🧪 Pruebas de Validación y Rendimiento

Tras reiniciar el stack completo, los resultados fueron sumamente exitosos:

### 1. Detección Expreso en Ollama Logs
Ollama completó el descubrimiento en milisegundos sin reportar timeouts:
```text
time=2026-05-18T03:17:21.372Z level=INFO source=types.go:42 msg="inference compute" id=GPU-caca97d4-fc68-767e-07e7-1a3c16f4242d library=CUDA compute=12.0 name=CUDA0 description="NVIDIA GeForce RTX 5050" total="8.0 GiB" available="7.5 GiB"
```

### 2. Offloading 100% en GPU
Al realizar una petición de inferencia con el modelo `llama3.2:latest`, el modelo se colocó por completo en la memoria dedicada:
```text
load_tensors: offloading 28 repeating layers to GPU
load_tensors: offloading output layer to GPU
load_tensors: offloaded 29/29 layers to GPU
load_tensors:   CUDA0 model buffer size =  1918.35 MiB
time=2026-05-18T03:18:13.457Z level=INFO source=server.go:1432 msg="llama runner started in 25.27 seconds"
```

### 3. Diagnóstico Activo de VRAM en Caliente
Al ejecutar `nvidia-smi` en el host durante el uso, el proceso de Ollama figura correctamente en la GPU con asignación estática:
```text
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 595.71.05              Driver Version: 595.71.05      CUDA Version: 13.2     |
|=========================================+========================+======================|
|   0  NVIDIA GeForce RTX 5050        On  |   00000000:01:00.0 Off |                  N/A |
|  0%   44C    P1             43W /  130W |    2560MiB /   8151MiB |      0%      Default |
+-----------------------------------------+------------------------+----------------------+
| Processes:                                                                              |
|  GPU   GI   CI              PID   Type   Process name                        GPU Memory |
|=========================================+========================+======================|
|    0   N/A  N/A          113234      C   /usr/bin/ollama                        2550MiB |
+-----------------------------------------------------------------------------------------+
```

---

## 📈 Conclusiones
La estabilización del driver NVIDIA y de los contenedores Docker mediante la persistencia automatizada elimina por completo los arranques lentos del sistema S.I.C.H., garantizando latencias mínimas y la residencia total en VRAM bajo las directivas optimizadas de `OLLAMA_FLASH_ATTENTION=1` y `OLLAMA_KEEP_ALIVE=-1`.
