# Orion Design - Infraestructura Moderna

Automatización de despliegue de infraestructura para **Orion Design** utilizando Ansible, Python y Docker Swarm.

Este proyecto permite configurar un servidor desde cero hasta tener un cluster de Docker Swarm funcional con Traefik como Reverse Proxy y Portainer para la gestión de contenedores.

## 🚀 Características Principales

- **Automatización Total:** Desde la instalación de dependencias hasta el despliegue de stacks.
- **Gestión con Ansible:** Uso de roles y playbooks para una configuración robusta e idempotente.
- **Docker Swarm & Stacks:** Orquestación nativa de contenedores para alta disponibilidad.
- **Traefik & Portainer:** Proxy inverso automático con gestión de certificados SSL y panel de administración visual.
- **Entorno Aislado:** Uso de entornos virtuales Python para evitar conflictos de dependencias.

## 📂 Estructura del Proyecto

- `setup.sh`: Script maestro de instalación. Prepara el entorno y lanza Ansible.
- `playbook.yml`: Playbook principal de Ansible.
- `deploy/`: Contiene los archivos Docker Compose/Stack para Traefik y Portainer.
- `Orion-Python-Ansible/`: Directorio con roles y configuraciones de Ansible.
- `redeploy.sh`: Script de utilidad para reiniciar los stacks rápidamente.

## 📚 Documentación

| Documento                                    | Descripción                                                 |
| :------------------------------------------- | :---------------------------------------------------------- |
| 🛠️ [**Guía de Instalación**](INSTALL.md)     | Instrucciones paso a paso para desplegar usando `setup.sh`. |
| 📖 [**Manual de Uso**](USO.md)               | Cómo actualizar y mantener la infraestructura.              |
| ⚙️ [**Funcionalidades**](FUNCIONALIDADES.md) | Detalles técnicos de la arquitectura.                       |

## ⚡ Inicio Rápido

```bash
# Entrar como root
sudo -i

# Clonar repo (si no lo tienes)
# git clone ...

# Entrar al directorio
cd setup-orion

# Ejecutar setup
./setup.sh
```

Para más detalles, consulta el archivo [INSTALL.md](INSTALL.md).
