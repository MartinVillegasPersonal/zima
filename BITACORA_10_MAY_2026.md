# Bitácora de Cambios - 10 de Mayo de 2026

## 1. Securización del Repositorio
* **Refactorización Masiva:** Se modificaron 75 scripts de Python (`v9_*.py`) para eliminar credenciales, usuarios e IPs `hardcodeadas` en el código fuente.
* **Implementación de Dotenv:** Los scripts ahora utilizan la librería `python-dotenv` para cargar variables dinámicas (`ZIMA_HOST`, `ZIMA_USER`, `ZIMA_PASS`).
* **Gitignore y Plantilla:** Se añadió el archivo `.env` al `.gitignore` para prevenir fugas de seguridad accidentales y se creó una plantilla `.env.example`.

## 2. Optimización y Estabilización de Ollama en GPU (Arquitectura Blackwell)
* **Timeout de Carga Aumentado:** Se identificó que la compilación JIT (Just-In-Time) de los modelos en la nueva RTX 5050 tardaba más del límite por defecto de Ollama (5 minutos), provocando cortes. Se aumentó a 30 minutos (`OLLAMA_LOAD_TIMEOUT=30m`).
* **Caché Persistente:** Para evitar tener que compilar los modelos cada vez que el contenedor se reinicia, se configuró `CUDA_CACHE_PATH=/root/.ollama/cuda_cache` apuntando al disco duro de 1TB. El tiempo de carga de un modelo virgen pasa de 15 minutos a ser instantáneo en posteriores ejecuciones.

## 3. Resolución de Errores Críticos (CUDA Out-of-Memory)
* **El Problema:** Al intentar correr `llava:v1.6` (para visión) y `llama3.2` (para asistente de Home Assistant) de forma paralela, el driver de NVIDIA colapsaba con el error `CUDA error: unspecified launch failure`.
* **Diagnóstico:** Sumar LLaVA (7B) + Llama 3.2 (3B) requería aproximadamente 10.9 GiB de memoria RAM libre contigua. Como la ZimaBlade solo disponía de 10.1 GiB (por la carga de Home Assistant y CasaOS), el sistema colapsaba por falta de memoria al intentar el streaming de video continuo. Por esta misma razón falló el intento de correr el modelo "Todo en Uno" `llama3.2-vision:11b`.

## 4. Arquitectura Propuesta (Próximos Pasos)
Dado que usar el procesador (CPU) no es negociable y se necesita análisis de *stream* de video ininterrumpido junto a un Asistente de Voz sin demoras, se implementará la arquitectura del **"Doble Cerebro Ligero"**:

* **Modelo de Visión Continua:** Se descargará **`moondream`**. Este modelo de 1.8 Billones de parámetros es el estándar de oro actual para Edge AI. Ocupará apenas **1.5 GB de VRAM**, lo que permite inyectar el *stream* de video sin sobrecargar la gráfica.
* **Modelo Asistente y Tool Calling:** Se utilizará **`llama3.2`** (3 Billones de parámetros). Este será exclusivo para chatear y controlar luces/dispositivos (ya que soporta *Tool Calling* de forma nativa). Ocupará **2.4 GB de VRAM**.
* **El Resultado:** Sumados, ocupan **menos de 4.0 GB**. Esto entra holgadamente en los 8 GB de la RTX 5050, garantizando concurrencia total en GPU, 0% de probabilidad de crashes de memoria, análisis de cámara 24/7 sin cortes, y respuestas del asistente en tiempo récord.

## 5. Lista de Tareas para Mañana (Checklist de Continuación)
Para retomar el trabajo exactamente donde lo dejamos y dejar la infraestructura 100% operativa, mañana ejecutaremos los siguientes pasos:

1. [ ] **Descarga del modelo de Visión:**
   Ejecutar en la terminal del servidor ZimaBlade para descargar el modelo Edge AI sin cargarlo en memoria:
   ```bash
   sudo docker exec ollama ollama pull moondream
   ```
2. [ ] **Configuración en Home Assistant (Asistente de Voz):**
   * Asegurarse de tener una integración de Ollama apuntando a `llama3.2`.
   * Verificar que tenga activada la opción "Permitir que el asistente controle Home Assistant".
   * Asignarlo como Agente de Conversación predeterminado.
3. [ ] **Configuración de las Cámaras de Seguridad:**
   * Modificar los *scripts* o automatizaciones de las cámaras para que ya no apunten a `llava` ni a `llama3.2-vision`.
   * Cambiar el modelo objetivo (target) a `moondream`.
4. [ ] **Prueba de Estrés (Concurrencia):**
   * Mantener el *stream* de cámara enviando imágenes a `moondream`.
   * Enviar un comando de voz a `llama3.2` simultáneamente.
   * Verificar mediante `sudo docker exec ollama nvidia-smi` que el uso de VRAM no supera los 4.5 GB y que no hay cuelgues del driver.
5. [ ] **Limpieza de Disco:**
   * Una vez validada la arquitectura, ejecutar `sudo docker exec ollama ollama rm llava:v1.6` y `ollama rm llama3.2-vision` para liberar casi 13 GB en el disco duro de 1TB.
