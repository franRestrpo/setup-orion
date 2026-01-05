# Orion-Python-Ansible

Este proyecto es una versión refactorizada y mejorada del script `SetupOrion.txt`, migrado a Python y Ansible para una gestión de infraestructura más robusta y escalable.

## Estructura del Proyecto

- `ansible/`: Contiene los playbooks y roles de Ansible.
  - `playbooks/`: Contiene los playbooks principales para orquestar la configuración.
    - `infra.yml`: Playbook para configurar la infraestructura base (Docker, etc.).
  - `roles/`: Contiene los roles reutilizables.
    - `common/`: Tareas comunes como actualizar el sistema e instalar paquetes base.
    - `docker/`: Tareas para instalar y configurar Docker.
- `scripts/`: Contiene los scripts de Python.
  - `main.py`: Script principal para interactuar con el usuario y ejecutar los playbooks.

## Requisitos

- Python 3.6+
- Ansible 2.9+
- `sshpass` (si se usa autenticación con contraseña para SSH)

## Uso

1.  **Configurar el inventario de Ansible:**

    Crea un archivo de inventario (p. ej., `inventario.ini`) con los hosts a los que quieres aplicar la configuración.

    ```ini
    [servers]
    tu_servidor ansible_host=IP_DEL_SERVIDOR ansible_user=USUARIO
    ```

2.  **Ejecutar el script principal:**

    El script `main.py` proporciona una interfaz interactiva para ejecutar las tareas de configuración.

    ```bash
    cd scripts
    python3 main.py
    ```

    El script presentará un menú de opciones. Selecciona la opción deseada para iniciar el despliegue.

3.  **Ejecutar Playbooks directamente (Opcional):**

    También puedes ejecutar los playbooks de Ansible directamente desde la línea de comandos.

    ```bash
    cd ansible
    ansible-playbook -i tu_inventario.ini playbooks/infra.yml
    ```

    Si necesitas proporcionar una contraseña para SSH, puedes usar el flag `--ask-pass`:

    ```bash
    ansible-playbook -i tu_inventario.ini playbooks/infra.yml --ask-pass
    ```

## Personalización

- **Añadir nuevas tareas:** Agrega nuevas tareas a los archivos `main.yml` dentro de los directorios de roles correspondientes.
- **Añadir nuevos roles:** Crea nuevos directorios de roles dentro de `ansible/roles` y añádelos al playbook `infra.yml`.
- **Modificar paquetes:** Edita los archivos `defaults/main.yml` dentro de cada rol para cambiar las listas de paquetes.
