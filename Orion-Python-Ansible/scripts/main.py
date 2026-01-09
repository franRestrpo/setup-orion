#!/usr/bin/env python3
import os
import sys
from pathlib import Path
from core.registry import ServiceRegistry
from core.config import ConfigManager
from core.templating import TemplateManager

def main():
    # Inicializar componentes
    base_dir = Path(__file__).parent
    registry = ServiceRegistry(base_dir / "registry")
    config_manager = ConfigManager()
    template_manager = TemplateManager()

    # Escanear registro de servicios
    try:
        registry.scan_registry()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Mostrar menú de categorías y servicios
    categories = registry.get_categories()
    
    while True:
        print("\n=== Orion Service Installer (Modular V2) ===")
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category}")
        print("0. Exit")

        choice = input("\nSelect a category: ").strip()
        
        if choice == '0':
            break
            
        try:
            cat_index = int(choice) - 1
            if 0 <= cat_index < len(categories):
                selected_category = categories[cat_index]
                services = registry.get_services_by_category(selected_category)
                
                print(f"\n--- {selected_category} Services ---")
                for i, service in enumerate(services, 1):
                    print(f"{i}. {service['name']} (v{service['version']})")
                print("0. Back")
                
                srv_choice = input("\nSelect a service to install: ").strip()
                
                if srv_choice == '0':
                    continue
                    
                srv_index = int(srv_choice) - 1
                if 0 <= srv_index < len(services):
                    selected_service = services[srv_index]
                    install_service(selected_service, config_manager, template_manager)
                else:
                    print("Invalid service selection.")
            else:
                print("Invalid category selection.")
        except ValueError:
            print("Please enter a valid number.")

def install_service(service_manifest, config_manager, template_manager):
    print(f"\nInstalling {service_manifest['name']}...")
    
    # 1. Cargar y solicitar variables
    variables = config_manager.load_variables(service_manifest)
    
    # 2. Generar archivo .env (opcional, si se requiere persistencia separada)
    # env_path = Path(service_manifest['path']) / ".env"
    # config_manager.generate_env_file(env_path, variables)
    
    # 3. Renderizar Stack File
    template_path = Path(service_manifest['path']) / "stack.yml.j2"
    output_path = Path.cwd() / f"{service_manifest['id']}_stack.yml"
    
    try:
        template_manager.render_template(str(template_path), variables, str(output_path))
        print(f"✅ Stack file generated at: {output_path}")
        print(f"🚀 To deploy run: docker stack deploy -c {output_path.name} {service_manifest['id']}")
    except Exception as e:
        print(f"❌ Error generating stack file: {e}")

if __name__ == "__main__":
    main()
