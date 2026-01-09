# Guía de Automatización con Portainer API

Esta guía explica cómo integrar el sistema de generación de stacks de Orion con la API de Portainer para lograr un despliegue continuo y automatizado.

## 1. Autenticación

Para interactuar con la API de Portainer de forma automatizada, se recomienda utilizar **Access Tokens** (disponibles en Portainer CE 2.14+ y Business Edition).

### Generar un Access Token
1. Inicia sesión en Portainer.
2. Ve a **My account** (arriba a la derecha).
3. En la sección **Access tokens**, haz clic en **Add access token**.
4. Dale una descripción (ej: "Orion Deployer") y copia el token generado. **No podrás verlo de nuevo**.

Este token se enviará en el header `X-API-Key` de tus peticiones HTTP.

---

## 2. Endpoints Clave para Stacks

La documentación completa de la API de Portainer está disponible en tu instancia en `/api/docs` o en [documentation.portainer.io](https://documentation.portainer.io/api/).

### Listar Stacks
*   **Método:** `GET`
*   **URL:** `/api/stacks`
*   **Headers:** `X-API-Key: <tu-token>`

### Crear Stack (Swarm)
*   **Método:** `POST`
*   **URL:** `/api/stacks?type=1&method=string&endpointId=<id>`
    *   `type=1`: Docker Swarm (use `type=2` para Docker Compose/Standalone).
    *   `method=string`: Indica que enviaremos el contenido del archivo directamente en el JSON.
    *   `endpointId`: El ID del entorno donde desplegar (usualmente `1` para el entorno local principal).
*   **Body (JSON):**
    ```json
    {
      "name": "nombre-del-stack",
      "stackFileContent": "version: '3.7'\nservices:..."
    }
    ```

### Actualizar Stack
*   **Método:** `PUT`
*   **URL:** `/api/stacks/<stack_id>?endpointId=<id>`
*   **Body (JSON):**
    ```json
    {
      "stackFileContent": "version: '3.7'\nservices:...",
      "prune": true,
      "pullImage": true
    }
    ```

---

## 3. Webhooks para Actualización Automática

Los Webhooks permiten que sistemas externos (como GitHub Actions, GitLab CI, o un script cron) notifiquen a Portainer que debe actualizar un servicio específico.

### Configuración en Portainer
1. Ve a tu Stack o Servicio en Portainer.
2. Activa la opción **Service Webhook** (en la sección de configuración del servicio).
3. Portainer generará una URL única, por ejemplo: `https://portainer.tuservidor.com/api/webhooks/wd34-2342-fd23...`

### Uso del Webhook
Simplemente envía una petición `POST` a esa URL. Portainer descargará la última versión de la imagen definida en el servicio y lo actualizará (rolling update).

```bash
curl -X POST https://portainer.tuservidor.com/api/webhooks/wd34-2342-fd23...
```

---

## 4. Ejemplo Práctico en Python

Se incluye un script de ejemplo en `scripts/examples/portainer_deploy.py` que demuestra cómo:
1. Leer un archivo YAML generado por `main.py`.
2. Conectar con la API de Portainer.
3. Verificar si el stack ya existe.
4. Crearlo o Actualizarlo según corresponda.

### Uso del Script
```bash
# Exportar variables de entorno
export PORTAINER_URL="https://portainer.tuservidor.com"
export PORTAINER_API_KEY="tu-access-token"

# Ejecutar despliegue
python3 scripts/examples/portainer_deploy.py traefik deploy/traefik_stack.yml