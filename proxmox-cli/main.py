import os
import requests
import yaml
import logging
import argparse
from proxmoxer import ProxmoxAPI
import urllib3

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# Function to retrieve Proxmox settings from settings.yaml file
def get_settings():
    with open("settings.yaml", "r") as settings_file:
        settings = yaml.safe_load(settings_file)

    settings["proxmox_host"] = os.environ.get("PROXMOX_HOST", settings["proxmox_host"])
    settings["user"] = os.environ.get("PROXMOX_USER", settings["user"])
    settings["password"] = os.environ.get("PROXMOX_PASSWORD", settings["password"])
    settings["verify_ssl"] = os.environ.get("PROXMOX_VERIFY_SSL", settings["verify_ssl"])

    return settings

# Function to print nodes and their associated virtual machines
def print_nodes_and_vms(proxmox):
    logger = logging.getLogger(__name__)
    logger.debug("Retrieving nodes and their associated virtual machines...")
    for node in proxmox.nodes.get():
        for vm in proxmox.nodes(node["node"]).qemu.get():
            print(f"{vm['vmid']}. {vm['name']} => {vm['status']}")
    logger.info("Nodes and their associated virtual machines printed.")

# Function to retrieve and print Proxmox users' information
def get_users(proxmox):
    logger = logging.getLogger(__name__)
    logger.debug("Retrieving Proxmox users...")
    users = proxmox.access.users.get()
    for user in users:
        print(f"User ID: {user['userid']}")
        print(f"Email: {user.get('email', 'N/A')}")
        print(f"Realm Type: {user.get('realm-type', 'N/A')}")
        print(f"Enable: {user.get('enable', 'N/A')}")
        print(f"Expire: {user.get('expire', 'N/A')}")
        print("-" * 20)
    logger.info("Proxmox users printed.")

# Function to retrieve all available nodes
def get_all_nodes(proxmox):
    nodes = proxmox.nodes.get()
    return [node["node"] for node in nodes]

# Function to print all available nodes
def print_all_nodes(proxmox):
    logger = logging.getLogger(__name__)
    logger.debug("Retrieving Proxmox nodes...")
    nodes = get_all_nodes(proxmox)
    if nodes:
        print("Nodes found:")
        for node in nodes:
            print(node)
            print("-" * 20)
        logger.info("Proxmox nodes printed.")
    else:
        print("No nodes found.")

# Function to print network information
def print_network_info(proxmox, node):
    logger = logging.getLogger(__name__)
    logger.debug("Retrieving network information for node: %s", node)
    networks = proxmox.nodes(node).network.get()
    for network in networks:
        print("Network Information:")
        for key, value in network.items():
            print(f"{key}: {value}")
        print("-" * 20)
    logger.info("Network information printed.")

# Function to retrieve Proxmox ticket
def get_ticket(settings):
    url = f"https://{settings['proxmox_host']}:8006/api2/json/access/ticket"
    data = {
        "username": settings["user"],
        "password": settings["password"],
    }
    try:
        response = requests.post(url, data=data, verify=settings["verify_ssl"])
        response_data = response.json()
        if "data" in response_data and "ticket" in response_data["data"]:
            return response_data["data"]["ticket"]
        else:
            logger.error("Failed to get a valid ticket.")
            return None
    except requests.exceptions.RequestException as e:
        logger.error("Error getting ticket: %s", e)
        return None

# Function to fetch and print available ISOs
def get_isos(settings):
    url = f"https://{settings['proxmox_host']}:8006/api2/json/nodes/{settings['target_node']}/storage/{settings['storage']}/content"
    response = requests.get(url, headers={"Cookie": f"PVEAuthCookie={settings['ticket']}"}, verify=settings["verify_ssl"])
    response_data = response.json()

    if response.status_code != 200:
        print(f"Failed to fetch ISOs. Status code: {response.status_code}")
        return

    print("Available ISOs:")
    for iso in response_data.get("data", []):
        print(f"ISO ID: {iso['volid']}")

# Main function
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", default=False, action="store_true", help="Enable debug mode")
    parser.add_argument("--users", default=False, action="store_true", help="Retrieve Proxmox users")
    parser.add_argument("--nodes", default=False, action="store_true", help="List all nodes")
    parser.add_argument("--network-info", default=False, action="store_true", help="Retrieve network information")
    parser.add_argument("--isos", default=False, action="store_true", help="Show ISOs available on the node")
    args = parser.parse_args()

    if not any(vars(args).values()):
        parser.print_help()
        return

    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=log_level, format="%(asctime)s - %(levelname)s - %(message)s")
    logger = logging.getLogger(__name__)

    settings = get_settings()
    proxmox = ProxmoxAPI(
        settings["proxmox_host"],
        user=settings["user"],
        password=settings["password"],
        verify_ssl=settings["verify_ssl"]
    )

    if args.isos:
        ticket = get_ticket(settings)
        settings['ticket'] = ticket
        get_isos(settings)
    elif args.users:
        get_users(proxmox)
    elif args.nodes:
        print_all_nodes(proxmox)
    elif args.network_info:
        print_network_info(proxmox, settings["target_node"])
    else:
        print_nodes_and_vms(proxmox)

if __name__ == "__main__":
    main()
