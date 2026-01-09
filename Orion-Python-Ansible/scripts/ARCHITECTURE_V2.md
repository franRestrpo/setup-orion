# Arquitectura Modular V2 - Orion Setup

Este documento detalla la propuesta de arquitectura para la versión 2.0 del sistema de despliegue automatizado Orion. El objetivo principal es desacoplar la lógica de despliegue (`main.py`) de las definiciones de servicios, permitiendo escalar el catálogo de aplicaciones sin modificar el código base y soportando las funcionalidades avanzadas observadas en `SetupOrion.sh`.

## 1. Concepto: Service Registry

En lugar de tener funciones hardcodeadas para cada servicio (como `ferramenta_chatwoot` en bash), adoptaremos un enfoque basado en datos. Cada servicio será un "paquete" autocontenido en el directorio `registry/`.

### Estructura de Directorios Propuesta

```plaintext
Orion-Python-Ansible/
├── scripts/
│   ├── main.py                 # Punto de entrada (Orquestador)
│   ├── registry/               # Catálogo de Servicios (Service Registry)
│   │   ├── _defaults/          # Configuraciones base heredables
│   │   │   └── stack-base.yml
│   │   ├── chatwoot/
│   │   │   ├── manifest.json   # Metadatos, dependencias y definiciones
│   │   │   ├── stack.yml.j2    # Plantilla Jinja2 del Docker Stack
│   │   │   └── .env.example    # Variables requeridas
│   │   ├── typebot/
│   │   │   ├── manifest.json
│   │   │   ├── stack.yml.j2
│   │   │   └── .env.example
│   │   └── ... (otros servicios)
│   ├── modules/                # Módulos de Lógica Core
│   │   ├── menu.py             # Generador de menús dinámicos
│   │   ├── config.py           # Gestor de variables y secretos
│   │   ├── database.py         # Gestor de bases de datos (Postgres/MySQL)
│   │   ├── docker.py           # Wrapper para comandos Docker/Swarm
│   │   └── utils.py            # Utilidades generales
│   └── ...
```

## 2. Definición del Servicio (`manifest.json`)

El archivo `manifest.json` es el corazón de la nueva arquitectura. Define todo lo necesario para desplegar un servicio sin escribir código Python específico.

### Esquema del Manifiesto

```json
{
  "id": "chatwoot",
  "name": "Chatwoot",
  "category": "Customer Support",
  "description": "Plataforma de soporte al cliente open-source.",
  "version": "latest",
  "dependencies": [
    {
      "service": "postgres",
      "required": true,
      "check_command": "docker ps | grep postgres"
    },
    {
      "service": "redis",
      "required": true
    }
  ],
  "databases": [
    {
      "type": "postgres",
      "db_name_var": "POSTGRES_DB_NAME",
      "user_var": "POSTGRES_USER",
      "password_var": "POSTGRES_PASSWORD"
    }
  ],
  "variables": [
    {
      "key": "URL_CHATWOOT",
      "prompt": "Ingrese el dominio para Chatwoot (ej: chat.midominio.com)",
      "required": true,
      "validation": "domain"
    },
    {
      "key": "ADMIN_EMAIL",
      "prompt": "Email del administrador",
      "required": true,
      "validation": "email"
    }
  ],
  "secrets": [
    {
      "key": "SECRET_KEY_BASE",
      "length": 32,
      "type": "hex"
    }
  ],
  "network": {
    "use_custom": true,
    "prompt_if_missing": "Ingrese el nombre de la red Docker Swarm (default: orion_net)"
  }
}
```

## 3. Módulos Core

### 3.1 Menu Manager (`modules/menu.py`)
- Escanea el directorio `registry/` al inicio.
- Lee los archivos `manifest.json`.
- Categoriza los servicios según el campo `category`.
- Genera dinámicamente el menú de selección (paginado si es necesario).
- Permite filtrar servicios ya instalados vs. disponibles.

### 3.2 Config Manager (`modules/config.py`)
- **Carga de Variables:** Lee `.env` global y `.env` específico del servicio.
- **Interacción:** Itera sobre la lista `variables` del manifiesto y solicita input al usuario si el valor no existe.
- **Secretos:** Genera automáticamente valores para las claves definidas en `secrets` si no existen.
- **Persistencia:** Guarda las configuraciones generadas en `vps_data/<servicio>.env` para persistencia y actualizaciones futuras.

### 3.3 Database Manager (`modules/database.py`)
- Abstrae la lógica compleja de creación de bases de datos que existe en `SetupOrion.sh`.
- Funciones genéricas: `create_postgres_db(db_name)`, `create_mysql_db(db_name)`.
- Verifica si el contenedor de base de datos (dependencia) está activo antes de intentar la creación.
- Ejecuta migraciones si el manifiesto lo indica (ej: comando `bundle exec rails db:migrate`).

### 3.4 Deploy Manager (`modules/deploy.py`)
- **Renderizado:** Utiliza Jinja2 para combinar `stack.yml.j2` con las variables procesadas por `Config Manager`.
- **Pre-flight:** Verifica que todas las dependencias (definidas en `dependencies` del manifiesto) estén cumplidas.
- **Despliegue:** Ejecuta `docker stack deploy`.
- **Post-flight:** Espera a que los servicios estén `healthy` (similar a `wait_stack` en bash).

## 4. Flujo de Trabajo (Workflow)

1.  **Inicio:** El usuario ejecuta `python3 main.py`.
2.  **Escaneo:** El sistema carga todos los `manifest.json` disponibles.
3.  **Selección:** El usuario selecciona un servicio del menú dinámico.
4.  **Validación de Dependencias:** El sistema verifica si las dependencias (ej: Postgres, Traefik) están instaladas. Si no, ofrece instalarlas o aborta.
5.  **Configuración:**
    - El sistema solicita las variables definidas en el manifiesto.
    - Genera secretos automáticamente.
    - Solicita el nombre de la red Docker (si no está definida globalmente).
6.  **Preparación de Entorno:**
    - Crea bases de datos necesarias mediante `Database Manager`.
    - Crea volúmenes o directorios en el host si es necesario.
7.  **Generación de Archivos:**
    - Crea el archivo `.env` final en `vps_data/`.
    - Renderiza el `stack.yml` final.
8.  **Despliegue:** Ejecuta el despliegue en Docker Swarm.
9.  **Verificación:** Monitorea el estado hasta que el servicio esté online.

## 5. Ventajas sobre la versión Bash (SetupOrion.sh)

- **Escalabilidad:** Agregar un nuevo servicio solo requiere crear una carpeta con un JSON y un YAML. No hay que tocar el código principal.
- **Mantenibilidad:** La lógica de "cómo crear una base de datos" o "cómo pedir una variable" está centralizada, no duplicada en cada función.
- **Robustez:** Manejo de errores try/catch en Python es superior a Bash.
- **Flexibilidad:** Uso de Jinja2 permite lógica condicional compleja dentro de los archivos YAML de las stacks.