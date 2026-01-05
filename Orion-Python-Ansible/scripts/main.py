# -*- coding: utf-8 -*-

import os
import getpass
import subprocess
import time

# ===================================================================================================
#                                       VARIABLES GLOBALES
# ===================================================================================================

# Colores para la consola
AMARILLO = "\033[33m"
VERDE = "\033[32m"
BLANCO = "\033[97m"
ROJO = "\033[91m"
RESET = "\033[0m"

# Directorios
HOME_DIRECTORY = os.path.expanduser("~")
DATOS_VPS_FILE = os.path.join(HOME_DIRECTORY, "datos_vps", "datos_vps")

# ===================================================================================================
#                                       FUNCIONES DE MENSAJES
# ===================================================================================================

def mostrar_version():
    """Muestra la versión del script y los enlaces a los grupos de WhatsApp."""
    print(f"{BLANCO}Versión de SetupOrion: {VERDE}v3.0.0 (Python){RESET}")
    print(f"{VERDE}hub.setuporion.com.br/grupo3      {BLANCO}<----- Grupos no WhatsApp ----->     {VERDE}hub.setuporion.com.br/grupo4{RESET}")
    print("\n")

def mostrar_licencia():
    """Muestra el mensaje sobre la licencia del script."""
    print(f"{AMARILLO}==================================================================================================={RESET}")
    print(f"{AMARILLO}=  {BLANCO}Este autoinstalador fue desarrollado para ayudar en la instalación de las principales aplicaciones de código abierto.{AMARILLO}  =")
    print(f"{AMARILLO}=  {BLANCO}Todos los créditos a los desarrolladores de cada aplicación disponible aquí.                  {AMARILLO}  =")
    print(f"{AMARILLO}=  {BLANCO}Este Setup está licenciado bajo la Licencia MIT.                                              {AMARILLO}  =")
    print(f"{AMARILLO}=  {BLANCO}Debe declarar que OrionDesign (contato@oriondesign.art.br) es el autor original.        {AMARILLO}  =")
    print(f"{AMARILLO}=  {BLANCO}Atribuir un enlace a https://oriondesign.art.br/setup                                        {AMARILLO}  =")
    print(f"{AMARILLO}==================================================================================================={RESET}")
    print("\n")

def aceptar_terminos():
    """Solicita al usuario que acepte los términos de la licencia."""
    while True:
        choice = input(f"Al escribir 'Y', aceptas y estás de acuerdo con las orientaciones anteriores (Y/N): ").strip().lower()
        if choice == 'y':
            return True
        elif choice == 'n':
            print("Qué pena que no estés de acuerdo. Finalizando el instalador. ¡Hasta luego!")
            time.sleep(2)
            exit(1)
        else:
            print("Por favor, introduce solo Y o N.")

def mostrar_creditos():
    """Muestra los créditos y formas de contribuir al proyecto."""
    print(f"{AMARILLO}==================================================================================================={RESET}")
    print(f"{AMARILLO}=           {BLANCO}¿Te gustaría contribuir para continuar con el desarrollo de este proyecto?            {AMARILLO}={RESET}")
    print(f"{AMARILLO}=                              {BLANCO}Puedes hacer una donación vía PIX:                               {AMARILLO}={RESET}")
    print(f"{AMARILLO}=                                     {AMARILLO}pix@oriondesign.art.br                                     {AMARILLO}={RESET}")
    print(f"{AMARILLO}=                                                                                                 {AMARILLO}={RESET}")
    print(f"{AMARILLO}=          {BLANCO}O únete a nuestra comunidad VIP en Discord y contribuye con el proyecto.             {AMARILLO}={RESET}")
    print(f"{AMARILLO}=                       {BLANCO}Nuestra comunidad:{AMARILLO} https://join.oriondesign.art.br                        {AMARILLO}={RESET}")
    print(f"{AMARILLO}==================================================================================================={RESET}")
    print("\n")

# ===================================================================================================
#                                       FUNCIONES PRINCIPALES
# ===================================================================================================

def obtener_datos_servidor():
    """Lee y extrae datos del archivo de configuración de la VPS."""
    try:
        with open(DATOS_VPS_FILE, 'r') as f:
            lines = f.readlines()
        
        server_data = {}
        for line in lines:
            if "Nome do Servidor:" in line:
                server_data['nombre_servidor'] = line.split(': ')[1].strip()
            if "Rede interna:" in line:
                server_data['nombre_rede_interna'] = line.split(': ')[1].strip()
        return server_data
    except FileNotFoundError:
        return {}

def menu_principal():
    """Muestra el menú principal de opciones."""
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        print(f"{AMARILLO}================================= MENU PRINCIPAL ====================================={RESET}")
        mostrar_version()
        
        # Aquí se añadirán las opciones del menú a medida que se migren
        print(f"{AMARILLO}[ 1 ]{RESET} - {BLANCO}Instalar Infraestructura Base (Docker, etc.){RESET}")
        print(f"{AMARILLO}[ 99 ]{RESET} - {BLANCO}Salir{RESET}")
        print(f"{AMARILLO}======================================================================================{RESET}\n")

        opcion = input("Digite el NÚMERO de la opción deseada: ").strip()

        if opcion == '1':
            # Llamar a la función de Ansible para instalar la infraestructura
            print("Ejecutando playbook de Ansible para la infraestructura base...")
            # subprocess.run(["ansible-playbook", "../ansible/playbooks/infra.yml"]) # Descomentar cuando esté listo
        elif opcion == '99':
            print("Saliendo del instalador.")
            break
        else:
            print(f"{ROJO}Opción no válida. Inténtalo de nuevo.{RESET}")
            time.sleep(2)

# ===================================================================================================
#                                       PUNTO DE ENTRADA
# ===================================================================================================

if __name__ == "__main__":
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"{BLANCO}==================== SETUP ORION - PYTHON EDITION ===================={RESET}")
    mostrar_licencia()
    
    if aceptar_terminos():
        menu_principal()
        mostrar_creditos()
