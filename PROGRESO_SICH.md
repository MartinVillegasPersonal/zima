# 📓 Bitácora de Migración: ZimaBlade S.I.C.H.

**Fecha:** 2026-05-09
**Estado del Sistema:** Migración de OS Completada (Fase de Reinicio)

## 🛠️ Acciones Realizadas

### 1. Diagnóstico de la GPU (RTX 5050 Blackwell)
- Se identificó que el kernel 5.10 (Debian 11) no posee el soporte de firmware necesario para la arquitectura Blackwell (GB206).
- El error `WPR2 already up` confirmó que el driver intentaba cargar firmware de la generación anterior (Ampere) por falta de compatibilidad en el núcleo del sistema.

### 2. Migración Debian 11 (Bullseye) → Debian 12 (Bookworm)
- **Inicio de Upgrade:** Se actualizaron los repositorios a `bookworm`.
- **Bloqueo Crítico:** Durante la actualización de `libc6`, el sistema se colgó por más de 1.5 horas. Esto se debió a una interrupción en el reinicio de servicios base (SSH/Systemd).
- **Rescate del Sistema:** 
    - Se eliminaron manualmente los procesos de `apt` y `dpkg` bloqueados.
    - Se liberaron los candados (`locks`) de la base de datos de paquetes.
    - Se resolvió un estado de "dependencias rotas" (Franken-Debian) usando `apt --fix-broken install`.

### 3. Estabilización de Paquetes
- Se logró actualizar `libc6`, `locales`, `binutils` y `libc-bin` a las versiones oficiales de Bookworm.
- El sistema operativo ahora se reporta como **Debian 12.13**.

### 4. Instalación del Kernel 6.1
- Se forzó la instalación del kernel **Linux 6.1.0-45-amd64** y sus cabeceras.
- Se actualizó el GRUB para asegurar que este sea el kernel por defecto.

---

# 🚀 Plan de Trabajo: Activación Final de GPU

## Fase 1: Salto al Nuevo Kernel (AHORA)
1. **Reinicio Final:** Ejecutar el comando para cargar el kernel 6.1.
2. **Validación:** Confirmar con `uname -r` que estamos en la versión 6.1.

## Fase 2: Drivers NVIDIA Bookworm
1. **Limpieza:** Eliminar restos del driver manual `575` que intentamos instalar antes.
2. **Instalación Oficial:** Instalar `nvidia-driver` y `firmware-misc-nonfree` directamente desde los repositorios de Debian 12 (que ya incluyen soporte maduro).
3. **Prueba de Fuego:** Ejecutar `nvidia-smi` y esperar ver la RTX 5050 activa.

## Fase 3: Despliegue Ollama GPU
1. **Container Toolkit:** Verificar que Docker reconozca el runtime de NVIDIA.
2. **Arranque de Ollama:** Iniciar el contenedor configurado para usar `--gpus all`.
3. **Prueba de Inferencia:** Cargar un modelo y verificar el uso de memoria VRAM.

## Fase 4: Integración SICH
1. **Open WebUI:** Conectar el frontend a la instancia de Ollama acelerada.
2. **Persistencia:** Verificar que Supabase y Uptime Kuma sigan operativos en el disco de 1TB tras la migración de OS.

---
**Próximo paso:** Reinicio para cargar Kernel 6.1.
