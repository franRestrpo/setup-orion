# Orion Design - Modern Infrastructure

Este proyecto automatiza el despliegue de servidores listos para **Orion Design**, utilizando estándares modernos de DevOps.

## Características
- **Clean Code:** Estructura modular basada en roles de Ansible, validada con `ansible-lint`.
- **Docker Moderno:** Instala la última versión oficial de Docker Engine y Docker Compose V2.
- **Verificación Automática:** El playbook comprueba que `git`, `docker` y `docker compose` están instalados y muestra un informe final.
- **Idempotencia:** Puede ejecutarse múltiples veces sin alterar el estado del sistema si no hay cambios.
- **Compatibilidad Futura:** Código actualizado para eliminar advertencias de obsolescencia (`deprecation warnings`) de Ansible.

## Documentación

| Archivo | Descripción |
|---|---|
| [`INSTALL.md`](INSTALL.md) | Guía detallada para la preparación del entorno y la primera ejecución. |
| [`USO.md`](USO.md) | Instrucciones sobre cómo actualizar y verificar el despliegue. |

## Requisitos del Sistema Destino
- **SO:** Debian 11/12, Ubuntu 20.04/22.04/24.04.
- **Acceso:** Usuario con permisos `sudo`.

Para empezar, consulta la [**Guía de Instalación**](INSTALL.md).