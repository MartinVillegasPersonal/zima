# Plan de Despliegue y Migración S.I.C.H. (ZimaBlade)

Este documento contiene las especificaciones de arquitectura y despliegue del Sistema Integrado de Cumplimiento Hogareño (S.I.C.H.) en el entorno de producción (ZimaBlade). 

> **Nota de Seguridad:** Las credenciales de acceso, IPs y puertos han sido extraídos de este documento y deben configurarse localmente en un archivo `.env` basado en `.env.example`.

## 1. Arquitectura de Almacenamiento (Realizado)
Para proteger la eMMC interna del servidor, los modelos pesados se alojan en un disco externo de 1TB.
- Montaje persistente de la unidad mediante `fstab` (UUID configurado en `.env`).
- Creación de directorios para volúmenes de Docker (`ollama_models` y `open-webui-data`).

## 2. Despliegue de Motores de IA en CPU (Realizado)
Despliegue inicial de contenedores Docker con persistencia de datos en el disco externo.

### Ollama (Modo CPU)
```bash
docker run -d --name ollama \
  -p ${OLLAMA_PORT}:${OLLAMA_PORT} \
  -v ${EXTERNAL_DRIVE_PATH}/ollama-nvidia:/root/.ollama \
  -v ${EXTERNAL_DRIVE_PATH}/ollama_models:/root/.ollama/models \
  --restart always \
  ollama/ollama:0.9.5
```

### Pre-caching de Modelos
```bash
docker exec -i ollama ollama pull llava:v1.6
docker exec -i ollama ollama pull llama3
```

## 3. Despliegue de Interfaz Gráfica (Realizado)
Se utiliza una interfaz web ligera desplegada vía Docker.

```bash
docker run -d \
  -p ${WEBUI_PORT}:3000 \
  -e NEXT_PUBLIC_OLLAMA_URL=http://${SERVER_IP}:${OLLAMA_PORT} \
  --add-host=host.docker.internal:host-gateway \
  --name chatbot-ui \
  --restart always \
  ghcr.io/mckaywrigley/chatbot-ui:main
```

---

## 4. Plan de Migración Futura a GPU (RTX 5050)

### Fase 1: Instalación de Hardware (Manual)
1. Apagar completamente el servidor.
2. Conectar físicamente la RTX 5050 al puerto PCIe.
3. Encender el equipo.

### Fase 2: Instalación de Controladores
Ejecutar la instalación del driver privativo de NVIDIA y el puente de Docker.
```bash
sudo apt update
sudo apt install -y nvidia-driver-550 nvidia-container-toolkit
sudo reboot
```

### Fase 3: Recreación de Ollama (Modo GPU)
```bash
docker rm -f ollama

docker run -d --gpus all --name ollama \
  -p ${OLLAMA_PORT}:${OLLAMA_PORT} \
  -v ${EXTERNAL_DRIVE_PATH}/ollama-nvidia:/root/.ollama \
  -v ${EXTERNAL_DRIVE_PATH}/ollama_models:/root/.ollama/models \
  --restart always \
  ollama/ollama:0.9.5
```
