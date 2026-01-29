# Implementation Plan - Phase 2: Application Deployer Role

This plan covers the implementation of the `desplegador_aplicaciones` role to replace the monolithic setup script logic.

## Goal

Enable declarative deployment of applications via `aplicaciones.yml`, handling dependencies (Redis, Postgres) automatically.

## User Review Required

> [!IMPORTANT]
> The deployment logic communicates directly with Docker Swarm, bypassing Portainer API tokens.

## Proposed Changes

### Ansible Roles

#### [NEW] `desplegador_aplicaciones`

- **tasks/main.yml**: Entry point, iterates over configured apps.
- **tasks/procesar_aplicacion.yml**: Validates app config, generates docker-compose from template, deploys to Swarm.
- **tasks/dependencias.yml**: Creates volumes and prepares dependencies (Redis/Postgres).
- **templates/chatwoot.yml.j2**: Jinja2 template for Chatwoot stack, properly formatted.

### Configuration

#### [NEW] `aplicaciones.yml`

- Defines the catalog of desired applications, their domains, and dependencies.

### Playbook

#### [MODIFY] `playbook.yml`

- Add `desplegador_aplicaciones` to the roles list.

## Verification Plan

### Automated Verification

- **Command:** `ansible-playbook -i inventory.ini playbook.yml`
- **Success Criteria:**
  - Playbook finishes with `failed=0`.
  - `docker stack ls` shows `chatwoot`.
  - `docker service ls` shows `chatwoot_web`, `chatwoot_sidekiq`, `chatwoot_redis`, `chatwoot_postgres`.

### Manual Verification

- Access `http://chatwoot.local` (or configured domain) in browser (requires host mapping).
- Verify connection to database by creating an account.
