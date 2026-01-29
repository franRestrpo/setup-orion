# Plan de Modernización y Reemplazo de SetupOrion

Este documento detalla el análisis del script legacy `SetupOrion.sh` y define la arquitectura para la nueva solución basada en **Ansible + Docker Swarm**, incorporando los requisitos de gestión de dependencias y validaciones.

## 1. Análisis del Sistema Legacy

El script actual es un instalador monolítico de ~45,000 líneas que gestiona despliegues de forma imperativa.
**Decisión:** Se reemplazará por una arquitectura modular y declarativa, eliminando la dependencia de la API de Portainer para los despliegues.

## 2. Nueva Arquitectura Propuesta

### 2.1. Despliegue Directo en Swarm (Sin API Portainer)

A diferencia del sistema anterior que requería tokens para hablar con la API de Portainer, **Ansible se comunicará directamente con el Docker Daemon (Swarm)**.

- **Ventaja:** Mayor robustez, menos puntos de fallo, eliminación de complejidad de tokens.
- **Visualización:** Portainer seguirá mostrando los stacks desplegados automáticamente, ya que lee el mismo Docker Engine.

### 2.2. Gestión Inteligente de Dependencias

Herramientas complejas como **Chatwoot** requieren servicios auxiliares (PostgreSQL, Redis).
**Estrategia:**

1.  **Servicios Compartidos (Opcional):** Posibilidad de tener un clúster de Redis/Postgres central.
2.  **Dependencias por Stack:** El rol de Ansible verificará e inyectará las dependencias necesarias en el `docker-compose` o desplegará los servicios previos requeridos.
    - _Ejemplo:_ Al activar `chatwoot`, Ansible asegurará que existan contenedores de `db_chatwoot` y `redis_chatwoot` (o use los compartidos) antes de iniciar la app.

### 2.3. Validación de Estado Previo

Antes de desplegar, el sistema realizará verificaciones:

- **Existencia:** ¿Ya existe un stack con ese nombre? (Evitar sobrescribir accidentalmente).
- **Puertos/Dominios:** ¿El dominio configurado ya está siendo usado por otro router de Traefik?

### 2.4. Entrada de Datos de Usuario (Interactivo vs Declarativo)

Se implementará un sistema híbrido para solicitar datos sensibles (Dominio, Usuario, Contraseña):

1.  **Modo Interactivo (Wizard):** Al ejecutar el setup, si faltan variables críticas, un script solicitará:
    - Dominio para la aplicación (ej: `chatwoot.miempresa.com`)
    - Credenciales de Administrador iniciales.
2.  **Modo Archivo (Desasistido):** Lectura desde `aplicaciones.yml` para automatización total.

### 2.5. Catálogo de Servicios (Ejemplo de Configuración)

```yaml
# aplicaciones.yml
aplicaciones_orion:
  - nombre: chatwoot
    habilitado: verdadero
    dominio: "chat.miempresa.com"
    # Ansible solicitará estas claves si no están definidas
    usuario_admin: "admin@miempresa.com"
    password_admin: "SuperSecreto123"
    dependencias:
      redis: interna # Desplegar redis interno
      postgres: interna # Desplegar postgres interno
```

## 3. Hoja de Ruta de Implementación

### Fase 1: Núcleo y Orquestación (✅ Completado)

- Docker Swarm activo.
- Traefik y Portainer operativos (Base).

### Fase 2: Motor de Validaciones y Dependencias (🚧 Siguiente Paso)

- Crear validadores en Ansible:
  - `verificar_stack_existente.yml`
  - `verificar_db_disponible.yml`
- Desarrollar lógica de **Servicios Auxiliares**: Definir bloques reutilizables para Redis y Postgres.

### Fase 3: Migración de Aplicaciones Clave

Se priorizará la migración de **Chatwoot** como caso de uso complejo (App + Redis + Postgres):

1.  Definir plantilla J2 para Chatwoot.
2.  Implementar `vars_prompt` para solicitar dominio y credenciales.
3.  Probar flujo de instalación limpia (New Deployment).

### Fase 4: CLI Helper

- Script auxiliar que pregunte "¿Qué quieres instalar?" y genere el `aplicaciones.yml` validando los datos ingresados al momento.

## 4. Confirmación de Requisitos

- **Tokens:** Eliminados. Despliegue directo a Swarm.
- **Datos:** Despliegues nuevos (Greenfield).
- **Validación:** Se incluirán tareas de "pre-flight check" (puertos, stacks previos).
- **Dependencias:** Gestionadas automáticamente por Ansible (ej: levantar Postgres antes de Chatwoot).

---

**Estado:** Esperando luz verde para comenzar con la **Fase 2** (Motor de Dependencias y Validaciones).
