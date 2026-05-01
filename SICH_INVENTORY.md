# 🛰️ Inventario de Servicios S.I.C.H. - ZimaBlade

Este documento contiene los puntos de acceso y propósitos de los aplicativos desplegados en el nodo ZimaBlade (192.168.0.203) bajo la Fase 9 de Persistencia.

| Servicio | URL / Acceso | Propósito |
| :--- | :--- | :--- |
| **Open WebUI** | [http://192.168.0.203:3001](http://192.168.0.203:3001) | Interfaz principal de IA (Chat, RAG, Documentos). |
| **Supabase Studio** | [http://192.168.0.203:8000](http://192.168.0.203:8000) | Gestión de base de datos relacional y vectorial. |
| **Ollama API** | [http://192.168.0.203:11434](http://192.168.0.203:11434) | Motor de ejecución de LLMs (Llama 3, Mistral, etc.). |
| **Portainer** | [http://192.168.0.203:9000](http://192.168.0.203:9000) | Monitoreo y gestión de contenedores Docker. |
| **SAMBA Share** | `\\192.168.0.203\SICH_Data` | Carpeta compartida en red para el disco de 1TB. |
| **Vaultwarden (HA)** | [https://192.168.0.200:7277](https://192.168.0.200:7277) | Gestión segura de credenciales y secretos. |

---

## 🛠️ Notas de Infraestructura
- **Almacenamiento:** Los datos y las imágenes Docker persisten en el HDD externo montado en `/mnt/external_hdd`.
- **Auto-arranque:** Configurado mediante `/etc/fstab` y políticas de reinicio de Docker para estabilidad post-reinicio.
- **Seguridad:** Las credenciales maestras de Postgres y Supabase están resguardadas en la bóveda de Vaultwarden.

*Última actualización: 2026-05-01*
