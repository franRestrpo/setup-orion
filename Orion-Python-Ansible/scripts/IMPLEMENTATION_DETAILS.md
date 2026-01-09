# Detalles de Implementación: Arquitectura de Despliegue Modular en Python

Este documento detalla la arquitectura técnica y el flujo de trabajo del sistema de despliegue automatizado para Orion. La solución ha evolucionado desde scripts monolíticos hacia una arquitectura modular en Python, centrada en la flexibilidad, la persistencia de configuración y la generación dinámica de infraestructura.

## 1. Generación Dinámica de Archivos (`generator.py`)

El núcleo de la flexibilidad del sistema reside en `generator.py`, un módulo diseñado para transformar plantillas genéricas en archivos de configuración listos para producción.

*   **Funcionamiento:**
    *   Toma como entrada una plantilla YAML (ubicada en `scripts/stacks/`) que contiene marcadores de posición (placeholders) como `{{RED_DOCKER}}`.
    *   Recibe un diccionario de contexto con los valores reales configurados por el usuario (ej: nombre de la red, dominios).
    *   Realiza una sustitución de cadenas para inyectar estos valores en la plantilla.
    *   Escribe el archivo resultante (ej: `traefik.yml`) en el directorio de ejecución actual.
    *   Adicionalmente, genera archivos `.env` específicos para cada servicio (ej: `.env-traefik`), asegurando que las variables de entorno necesarias estén disponibles para Docker en tiempo de despliegue.

*   **Beneficio:** Elimina la necesidad de editar manualmente archivos YAML y desacopla la definición de la infraestructura (plantillas) de la configuración específica del entorno (instancias generadas).

## 2. Gestión de Redes Docker (`checks.py` y `preflight.py`)

La gestión de la red overlay es crítica para la comunicación entre servicios en un clúster Swarm.

*   **Validación y Creación (`checks.py`):**
    *   La función `network_exists(name)` ya no es pasiva. Ahora acepta el nombre de la red como argumento dinámico.
    *   Verifica si la red existe utilizando `docker network ls`.
    *   **Autorecuperación:** Si la red no existe, el script ejecuta automáticamente `docker network create --driver=overlay <nombre_red>`, garantizando que el prerrequisito de red se cumpla sin intervención manual.

*   **Orquestación (`preflight.py`):**
    *   Actúa como controlador de las validaciones previas.
    *   Recibe el nombre de la red desde el flujo principal y lo pasa a `checks.py`, asegurando que todas las validaciones se realicen contra la red configurada por el usuario, no una constante estática.

## 3. Flujo de Ejecución Principal (`main.py`)

El script `main.py` actúa como el punto de entrada y orquestador de todo el proceso. Su lógica se ha reescrito para ser interactiva y persistente.

1.  **Carga de Configuración:**
    *   Al iniciarse, intenta cargar configuraciones previas desde un archivo `.env` persistente.
    *   Si no existe o faltan variables críticas (Red, Dominios, Email), inicia un asistente de configuración (`configure()`).

2.  **Interacción con el Usuario:**
    *   Solicita al usuario:
        *   **Nombre de la Red Docker:** (Por defecto: `OrionNet`).
        *   **Dominio para Traefik:** (Ej: `traefik.midominio.com`).
        *   **Dominio para Portainer:** (Ej: `portainer.midominio.com`).
        *   **Email para SSL:** Utilizado para la generación de certificados Let's Encrypt.
    *   Guarda estas preferencias en el archivo `.env`, evitando preguntas repetitivas en futuras ejecuciones.

3.  **Orquestación del Despliegue:**
    *   Cuando el usuario selecciona desplegar un servicio (ej: Traefik):
        1.  Ejecuta las validaciones `preflight` usando la red configurada.
        2.  Invoca a `generator.py` para crear los archivos YAML y ENV específicos con los datos del usuario.
        3.  Llama a `deploy.py` pasando los archivos generados y el entorno configurado.

## 4. Estructura Modular y Responsabilidades

La arquitectura se divide en componentes especializados para facilitar el mantenimiento y la escalabilidad:

*   **`constants.py`**:
    *   Define valores por defecto globales, como `DEFAULT_NETWORK` y umbrales de recursos (RAM, CPU). Actúa como fuente de verdad para valores fallback.

*   **`deploy.py`**:
    *   Encapsula la lógica de interacción con el binario de Docker.
    *   Ejecuta `docker stack deploy` inyectando las variables de entorno necesarias para que el motor de Docker resuelva las referencias `${VAR}` en los archivos Compose.
    *   Maneja flags de limpieza (`--prune`) y resolución de imágenes para asegurar despliegues consistentes.

*   **`utils.py`**:
    *   Proporciona utilidades de bajo nivel, como la verificación de la existencia de comandos en el sistema operativo (`cmd_exists`) y wrappers para la ejecución de subprocesos.

*   **`scripts/stacks/` (Plantillas)**:
    *   Contiene las definiciones base de los servicios (`traefik.yml`, `portainer.yml`).
    *   Estos archivos ahora son **plantillas puras**, utilizando marcadores `{{RED_DOCKER}}` para la red y variables `${VAR}` para dominios, diseñadas para ser procesadas por el generador, no desplegadas directamente.