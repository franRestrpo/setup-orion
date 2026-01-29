# Guia de Instalación Completa

Esta guía cubre desde la preparación del servidor hasta el despliegue final utilizando nuestro script automatizado `setup.sh`.

## Prerrequisitos

- **Sistema Operativo:** Ubuntu 20.04+, Debian 11+
- **Permisos:** Usuario `root` o permisos de `sudo`.
- **Conexión a Internet.**

## Instrucciones de Instalación

Para desplegar toda la infraestructura, utilizaremos el script `setup.sh`, que se encargará de:

1.  Instalar dependencias del sistema.
2.  Configurar un entorno virtual de Python.
3.  Instalar Ansible y las librerías necesarias.
4.  Ejecutar el playbook principal para configurar Docker, Swarm y otras herramientas.

### 1. Clonar el repositorio

Si aún no has clonado el repositorio, hazlo en tu directorio de trabajo:

```bash
git clone <URL_DEL_REPOSITORIO> setup-orion
cd setup-orion
```

### 2. Ejecutar el Script de Setup

El script debe ejecutarse como root para poder instalar paquetes y configurar el sistema.

```bash
sudo ./setup.sh
```

El script mostrará el progreso de cada etapa. Si todo finaliza correctamente, verás un mensaje de éxito indicando que la infraestructura está lista.

## Post-Instalación

Una vez finalizado el script, verifica que los servicios estén corriendo:

```bash
docker stack ls
docker service ls
```

Para acceder a los paneles de administración:

- **Traefik Dashboard:** `traefik.localhost` (puede requerir configuración de hosts)
- **Portainer:** `portainer.localhost` (puede requerir configuración de hosts)

## Solución de Problemas

Si el script falla:

- Revisa los logs que se imprimen en pantalla.
- Asegúrate de tener conexión a internet.
- Verifica que no haya bloqueos de apt/dpkg (`sudo lsof /var/lib/dpkg/lock-frontend`).
