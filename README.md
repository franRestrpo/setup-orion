# Orion Design - Modern Infrastructure

Este proyecto automatiza el despliegue de servidores listos para **Orion Design**, utilizando estándares modernos de DevOps.

## Características
- **Clean Code:** Estructura modular basada en roles de Ansible.
- **Docker Moderno:** Instala la última versión oficial de Docker Engine y Docker Compose V2.
- **Sin Legacy:** Eliminados los parches de API antigua (`1.24`).
- **Idempotencia:** Puede ejecutarse múltiples veces sin romper el sistema.

## Requisitos del Sistema Destino
- SO: Debian 11/12, Ubuntu 20.04/22.04/24.04.
- Acceso: Usuario con permisos `sudo`.