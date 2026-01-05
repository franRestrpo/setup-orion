# Guía de Uso y Mantenimiento

## Actualizar el Repositorio

Para asegurarte de tener la última versión del código de automatización, sigue estos pasos en tu nodo de control, dentro de la carpeta del proyecto.

1.  **Verificar Cambios Locales:**
    Antes de actualizar, comprueba si tienes cambios que no se han subido al repositorio.
    ```bash
    git status
    ```

2.  **Descargar Cambios del Repositorio Remoto:**
    Usa `git pull` para descargar y fusionar los cambios más recientes.
    ```bash
    git pull
    ```

## Ejecutar el Playbook

Una vez que tu repositorio local esté actualizado, puedes aplicar la configuración a tus servidores.

```bash
# Activa tu entorno virtual si no lo has hecho
source venv/bin/activate

# Ejecuta el playbook
ansible-playbook -i inventory.ini playbook.yml --ask-become-pass