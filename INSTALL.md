# Guía de Instalación Completa

Esta guía cubre desde la preparación de la máquina de control hasta el despliegue final.

## Paso 1: Preparación del Entorno Python (Control Node)
Ansible requiere Python. Recomendamos usar un entorno virtual para no ensuciar tu sistema.

1. **Instalar Python y herramientas base:**
   ```bash
   sudo apt update
   sudo apt install -y python3 python3-venv python3-pip git
   # Crear carpeta del proyecto
mkdir orion-setup && cd orion-setup

# Crear entorno virtual llamado 'venv'
python3 -m venv venv
source venv/bin/activate
pip install ansible ansible-lint

# Instalar roles de Ansible Galaxy (si existen en requirements.yml)
ansible-galaxy install -r requirements.yml
# Si tienes clave SSH configurada:
# Antes de ejecutar, es buena práctica verificar la sintaxis del playbook
ansible-playbook -i inventory.ini playbook.yml --syntax-check

# También puedes ejecutar el linter para asegurar la calidad del código
ansible-lint

# Si tienes clave SSH configurada:
ansible-playbook -i inventory.ini playbook.yml

# Si necesitas escribir la contraseña de SUDO:
ansible-playbook -i inventory.ini playbook.yml --ask-become-pass
# Verificar versión de Docker (debe ser 24.x, 25.x o superior)
docker version

# Verificar Docker Compose V2
docker compose version