# 🖥️ Plan de Migración: Debian Bullseye → Bookworm (ZimaBlade GPU)

## Contexto y Motivo

La ZimaBlade está corriendo **Debian 11 (Bullseye)** con kernel `5.10.0-42-amd64`.
La tarjeta gráfica instalada es una **NVIDIA RTX 5050 (Blackwell, ID PCI: `10de:2d83`)**.

### ¿Por qué migrar?
- El driver NVIDIA más nuevo disponible en Bullseye es el **470**, que no soporta la arquitectura Blackwell.
- Instalamos manualmente el driver **575.64.05** desde nvidia.com, pero **también falla** porque intenta cargar el firmware `gsp_ga10x.bin` (Ampere) en vez del firmware Blackwell correcto (`gsp_gb10x.bin`).
- El error en `dmesg`:
  ```
  NVRM: _kgspBootGspRm: unexpected WPR2 already up, cannot proceed with booting GSP
  NVRM: GPU 0000:01:00.0: RmInitAdapter failed! (0x62:0x40:1941)
  ```
- **Debian 12 (Bookworm)** incluye kernel `6.1` y drivers NVIDIA actualizados con soporte real para Blackwell.

---

## Estado Actual del Sistema (Antes de la Migración)

| Componente | Valor |
|---|---|
| **IP ZimaBlade** | `192.168.0.203` |
| **Usuario SSH** | `casaos` / contraseña: `casaos` |
| **OS** | Debian 11 (Bullseye) |
| **Kernel** | `5.10.0-42-amd64` |
| **Docker data-root** | `/mnt/external_hdd/docker_data` |
| **Disco externo** | `/mnt/external_hdd` (1TB, UUID en fstab) |
| **GPU** | NVIDIA RTX 5050, PCI `0000:01:00.0`, ID `10de:2d83` |
| **Driver instalado** | `575.64.05` (funcional a nivel módulo, falla en firmware) |

### Contenedores activos (todos en disco externo):
- `uptime-kuma` → puerto 3002
- `portainer` → puerto 9000
- `open-webui` → puerto 3001 (**unhealthy** — esperando Ollama)
- `chatbot-ui` → puerto 3000
- `ollama` → puerto 11434 (**Created**, no levanta sin GPU)
- `supabase-*` (stack completo: kong, studio, db, auth, rest, etc.) → puerto 8000
- `archivebox` → puerto 18010

---

## Plan de Migración Paso a Paso

### ⚠️ Pre-requisitos (ya completados)
- [x] Docker data-root movido a `/mnt/external_hdd/docker_data` — las imágenes sobreviven al OS upgrade.
- [x] Driver NVIDIA 575 instalado (módulo cargado, falla firmware).
- [x] `nvidia-container-toolkit` instalado y configurado en `/etc/docker/daemon.json`.
- [x] Repositorios `contrib non-free` habilitados en `/etc/apt/sources.list`.

---

### Paso 1 — Backup de configuración crítica

```bash
# Conectar por SSH
ssh casaos@192.168.0.203

# Guardar configuración de Docker
sudo cp /etc/docker/daemon.json /mnt/external_hdd/backup_daemon.json

# Guardar fstab (montaje del disco)
sudo cp /etc/fstab /mnt/external_hdd/backup_fstab.txt

# Guardar lista de contenedores
docker ps -a > /mnt/external_hdd/backup_containers.txt
```

### Paso 2 — Reemplazar fuentes de apt a Bookworm

```bash
# Cambiar "bullseye" por "bookworm" en sources.list
sudo sed -i 's/bullseye/bookworm/g' /etc/apt/sources.list
sudo sed -i 's/bullseye/bookworm/g' /etc/apt/sources.list.d/*.list 2>/dev/null || true

# Verificar
cat /etc/apt/sources.list
```

El archivo debe quedar así:
```
deb http://deb.debian.org/debian/ bookworm main contrib non-free non-free-firmware
deb http://security.debian.org/debian-security bookworm-security main contrib non-free non-free-firmware
deb http://deb.debian.org/debian/ bookworm-updates main contrib non-free non-free-firmware
```

### Paso 3 — Actualizar el sistema (puede tardar 15-30 min)

```bash
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get dist-upgrade -y --allow-downgrades
sudo apt-get autoremove -y
```

> **IMPORTANTE:** Durante el upgrade puede preguntar por archivos de configuración modificados (como `/etc/docker/daemon.json`). Responder siempre **"N" (keep current version)** para preservar la configuración del disco externo.

### Paso 4 — Reiniciar con el nuevo kernel

```bash
sudo reboot
```

Verificar tras el reboot:
```bash
uname -r
# Debe mostrar: 6.1.x-xx-amd64
```

### Paso 5 — Instalar driver NVIDIA desde Bookworm

```bash
# Instalar el driver oficial de Bookworm (ya debería soportar Blackwell)
sudo apt-get install -y nvidia-driver firmware-misc-nonfree nvidia-container-toolkit

# Verificar
nvidia-smi
```

Si `nvidia-smi` muestra la RTX 5050 correctamente: ✅ Éxito.

### Paso 6 — Configurar Docker Runtime para GPU

```bash
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

### Paso 7 — Arrancar Ollama GPU

```bash
docker start ollama
docker logs ollama
# Buscar la línea: "msg="inference compute" id=GPU-xxxxx library=cuda"
```

### Paso 8 — Verificar Open WebUI

Abrir `http://192.168.0.203:3001` y hacer una consulta. Open WebUI debería pasar de *unhealthy* a *healthy* automáticamente.

---

## Rollback (Si algo falla)

Si el sistema no levanta tras el upgrade, los datos están seguros porque:
1. Todos los volúmenes Docker están en `/mnt/external_hdd` (disco físico separado).
2. Se puede reinstalar Debian 11 o 12 limpio y restaurar Docker apuntando al mismo disco.

Comandos de recuperación desde live USB:
```bash
# Montar el disco externo
mount /dev/sda1 /mnt/external_hdd

# Restaurar daemon.json
cp /mnt/external_hdd/backup_daemon.json /etc/docker/daemon.json

# Reinstalar docker y arrancar
apt install docker.io
systemctl start docker
docker start $(docker ps -aq)
```

---

## Notificaciones
Las notificaciones de progreso se envían a Home Assistant mediante:
```bash
curl -X POST https://gi4w1f6xxevmeebulyfpapmhlowq83v6.ui.nabu.casa/api/webhook/notificacion_secreta_pro \
     -H "Content-Type: application/json" \
     -d '{"message": "mensaje aqui"}'
```

---

*Documento creado: 2026-05-09 | Estado: Listo para ejecutar Paso 1*
