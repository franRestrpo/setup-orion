import os, time
from preflight import run
from deploy import deploy

def menu():
    while True:
        os.system("clear")
        print("[1] Deploy Traefik")
        print("[2] Deploy Portainer")
        print("[99] Salir")

        opt = input("> ").strip()

        if opt == "1":
            run()
            deploy("traefik", "../stacks/traefik.yml")

        elif opt == "2":
            run()
            deploy("portainer", "../stacks/portainer.yml")

        elif opt == "99":
            break

        else:
            print("Opción inválida")
            time.sleep(1)

if __name__ == "__main__":
    menu()
