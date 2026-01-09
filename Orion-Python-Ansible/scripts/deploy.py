import subprocess

def deploy(stack: str, compose_file: str):
    subprocess.run(
        ["docker", "stack", "deploy", "-c", compose_file, stack],
        check=True
    )
