#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ANSIBLE_DIR = BASE_DIR / "ansible"
PLAYBOOKS = ANSIBLE_DIR / "playbooks"

GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
RESET = "\033[0m"

def run(cmd, fatal=True):
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        if fatal:
            print(f"{RED}[ERROR]{RESET} Falló: {' '.join(cmd)}")
            sys.exit(1)

def banner():
    print(f"{GREEN}=== Setup Orion ==={RESET}")

def confirm(msg):
    r = input(f"{YELLOW}{msg} (y/N): {RESET}").lower()
    return r == "y"

def playbook(name):
    run([
        "ansible-playbook",
        str(PLAYBOOKS / name),
        "-i", "localhost,",
        "-c", "local"
    ])

def main():
    banner()

    playbook("prechecks.yml")

    if not confirm("Continuar con instalación base"):
        sys.exit(0)

    playbook("install.yml")
    playbook("docker.yml")
    playbook("swarm.yml")
    playbook("orion.yml")

    print(f"{GREEN}[OK]{RESET} Instalación finalizada")

if __name__ == "__main__":
    main()
