# Orion Design - Infraestructura Moderna

Automatización de despliegue de servidores para **Orion Design** utilizando Ansible y Python, siguiendo estándares modernos de DevOps.

## 🚀 Características Principales

*   **Código Limpio y Modular:** Estructura basada en roles de Ansible, validada con `ansible-lint` para garantizar calidad y mantenibilidad.
*   **Docker de Última Generación:** Instalación automatizada de Docker Engine oficial y Docker Compose V2.
*   **Orquestación Inteligente:** Verificación automática de componentes (`git`, `docker`, `compose`) e informes de estado al finalizar.
*   **Idempotencia Garantizada:** Ejecuciones seguras y repetibles sin efectos secundarios no deseados.
*   **Preparado para el Futuro:** Código optimizado y libre de advertencias de obsolescencia.

## 📚 Documentación

Toda la información necesaria para desplegar, usar y entender el proyecto está organizada en los siguientes documentos:

| Documento | Propósito |
| :--- | :--- |
| 🛠️ [**Guía de Instalación**](INSTALL.md) | Paso a paso para preparar el entorno y realizar el primer despliegue. |
| 📖 [**Manual de Uso**](USO.md) | Instrucciones para actualizaciones, mantenimiento y verificación. |
| ⚙️ [**Funcionalidades Técnicas**](FUNCIONALIDADES.md) | Detalles profundos sobre la arquitectura, roles de Ansible y scripts internos. |

## 📋 Requisitos del Sistema

El sistema destino debe cumplir con lo siguiente:

*   **Sistema Operativo:**
    *   Debian 11 (Bullseye) / 12 (Bookworm)
    *   Ubuntu 20.04 LTS / 22.04 LTS / 24.04 LTS
*   **Permisos:** Acceso root o usuario con privilegios `sudo`.

## ⚡ Inicio Rápido

Para comenzar inmediatamente con la configuración de tu servidor, dirígete a la [**Guía de Instalación**](INSTALL.md).
