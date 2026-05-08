# Plan de Despliegue y Migración S.I.C.H. (ZimaBlade)

Este documento contiene las especificaciones de arquitectura y despliegue del Sistema Integrado de Cumplimiento Hogareño (S.I.C.H.) en el entorno de producción (ZimaBlade). 

> **Nota de Seguridad e Infraestructura:** 
> - Las credenciales de acceso (protocolo SSH, usuario `casaos`, IP `192.168.0.203` y contraseña) se encuentran documentadas dentro de los scripts Python del repositorio (como `v9_ssh_tunnel.py` o `check_space.py`).
> - Las rutas de los discos externos generalmente se encuentran en `/media/devmon/external_hdd` o bajo `/var/lib/casaos/files/AppData`.
> - Las IPs y puertos deben configurarse localmente en un archivo `.env` basado en `.env.example`.

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

## 4. Optimización de Almacenamiento Docker (CasaOS)
Para garantizar que **todas** las descargas de imágenes Docker (como las de Ollama, que son muy pesadas) se almacenen en el disco de 1TB y no saturen la eMMC nativa de la ZimaBlade, es necesario redirigir el directorio raíz de Docker.

```bash
# 1. Detener Docker
sudo systemctl stop docker

# 2. Crear/Editar el archivo de configuración de Docker
sudo nano /etc/docker/daemon.json
```

Añadir el siguiente contenido (reemplazando por la ruta real del disco de 1TB, por ejemplo `/DATA/AppData/docker_data` o `/media/devmon/DISCO/docker_data`):
```json
{
  "data-root": "/ruta/real/a/tu/disco_1tb/docker_data"
}
```

```bash
# 3. Mover datos existentes (opcional pero recomendado)
sudo rsync -aP /var/lib/docker/ /ruta/real/a/tu/disco_1tb/docker_data/

# 4. Reiniciar Docker
sudo systemctl start docker
```

---

## 5. Plan de Migración Futura a GPU (RTX 5050)

### Fase 1: Desinstalación del Ollama Actual (Modo CPU)
- **Si fue instalado vía CasaOS UI**: Desinstalar directamente desde la interfaz web de CasaOS (Opciones de la app > Desinstalar) para evitar conflictos en el dashboard.
- **Si fue instalado vía terminal**:
  ```bash
  docker rm -f ollama
  ```

### Fase 2: Instalación de Hardware (Manual)
1. Apagar completamente el servidor.
2. Conectar físicamente la RTX 5050 al puerto PCIe.
3. Encender el equipo.

### Fase 3: Instalación de Controladores
Ejecutar la instalación del driver privativo de NVIDIA y el puente de Docker.
```bash
sudo apt update
sudo apt install -y nvidia-driver-550 nvidia-container-toolkit
sudo reboot
```

### Fase 4: Recreación de Ollama (Modo GPU en CasaOS)
Dado que se utiliza CasaOS, la vía más sencilla y **altamente recomendada** es usar la tienda de aplicaciones integrada:
1. Abre la **App Store** en CasaOS.
2. Busca e instala la aplicación oficial **Ollama(Nvidia GPU)**.
3. Asegúrate de que, en los ajustes de la aplicación instalada (haciendo clic en opciones > Settings), los **volúmenes** apunten al disco de 1TB (ej. `/media/devmon/external_hdd/ollama-nvidia`).

*(Alternativa)* Si la app no aparece o prefieres control absoluto, puedes desplegar manualmente. En la interfaz de CasaOS, ve a **App Store** > **Custom Install** > **Import** y pega la siguiente configuración `docker-compose.yml`:

```yaml
name: ollama-nvidia
services:
  ollama:
    image: ollama/ollama:latest
    container_name: ollama
    restart: always
    ports:
      - "${OLLAMA_PORT}:${OLLAMA_PORT}"
    volumes:
      - ${EXTERNAL_DRIVE_PATH}/ollama-nvidia:/root/.ollama
      - ${EXTERNAL_DRIVE_PATH}/ollama_models:/root/.ollama/models
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```
*(Nota: Asegúrate de que las variables como `${EXTERNAL_DRIVE_PATH}` estén resueltas a sus rutas absolutas, por ejemplo `/media/devmon/external_hdd`).*
