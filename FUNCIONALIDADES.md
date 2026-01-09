# Funcionalidades del Proyecto Orion Design

Este documento detalla las capacidades técnicas y los procesos automatizados que realiza el núcleo del proyecto (basado en Ansible y Python), excluyendo los scripts de inicialización del entorno (`setup/`).

## 1. Orquestación de Infraestructura (Ansible)

El sistema utiliza Ansible para garantizar un estado deseado en los servidores, asegurando idempotencia y estandarización. La lógica se divide en roles modulares:

### A. Rol `common` (Configuración Base)
Prepara el sistema operativo con las herramientas esenciales antes de cualquier despliegue mayor.

*   **Detección del Sistema Operativo:** Carga variables específicas según la familia del SO (ej. Debian).
*   **Limpieza de Conflictos:** Busca y elimina repositorios de Docker antiguos o conflictivos en `/etc/apt/sources.list.d/`.
*   **Instalación de Paquetes del Sistema:**
    *   Herramientas de red y descarga: `curl`, `wget`.
    *   Monitorización y sistema: `htop`, `neofetch`, `apt-utils`.
    *   Utilidades varias: `git`, `dialog`, `jq`, `apache2-utils`.
*   **Entorno Python:** Asegura la presencia de `python3`, `python3-pip` y `python3-venv`.
*   **Verificación:** Comprueba y registra la versión instalada de Git.

### B. Rol `docker` (Motor de Contenedores)
Implementa un entorno Docker moderno y listo para producción.

*   **Gestión de Repositorios Oficiales:**
    *   Instala dependencias para gestión de claves (`gnupg-agent`, `software-properties-common`, etc.).
    *   Añade la clave GPG oficial de Docker.
    *   Configura el repositorio estable de Docker adaptado a la distribución de Linux detectada.
*   **Instalación de Componentes:**
    *   `docker-ce` (Community Edition).
    *   `docker-ce-cli`.
    *   `containerd.io`.
    *   `docker-compose-plugin` (Docker Compose V2).
*   **Gestión del Servicio:** Habilita y arranca el servicio `docker` mediante systemd.
*   **Docker Swarm:**
    *   Verifica el estado actual del nodo.
    *   Inicializa el cluster Swarm (`docker swarm init`) si no está activo.
*   **Redes:**
    *   Crea una red interna tipo overlay llamada `OrionNet` para la comunicación entre servicios.

### C. Informe de Despliegue
Al finalizar la ejecución, el playbook genera un reporte en consola que resume:
*   Versión de Git.
*   Versión de Docker Engine.
*   Versión de Docker Compose.
*   Estado de Docker Swarm (Activo/Inactivo).

## 2. Interfaz de Gestión (Python)

El script `Orion-Python-Ansible/scripts/main.py` actúa como el punto de entrada interactivo para el administrador del sistema.

*   **Menú Interactivo:** Interfaz CLI limpia para seleccionar operaciones (ej. Instalar Infraestructura).
*   **Lectura de Configuración:** Capacidad para leer datos de la VPS desde `~/datos_vps/datos_vps` (Nombre del servidor, Red interna).
*   **Ejecución de Ansible:** Llama a los playbooks de Ansible mediante subprocesos, integrando la potencia de la automatización con la facilidad de uso de un menú.
*   **Información del Proyecto:** Muestra versiones, licencias y créditos del proyecto Orion Design.

## 3. Estructura de Archivos del Núcleo

*   `ansible/`: Contiene la lógica de automatización.
    *   `playbooks/`: Playbooks principales (ej. `infra.yml` para infraestructura base).
    *   `roles/`: Unidades de automatización reutilizables (`common`, `docker`).
*   `scripts/`: Contiene scripts de soporte y gestión.
    *   `main.py`: Interfaz CLI principal.