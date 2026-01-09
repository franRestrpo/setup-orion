from checks import require, swarm_active, network_exists
from resources import validate

def run():
    require("docker")
    swarm_active()
    network_exists()
    validate()
