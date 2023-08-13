# Import required libraries
import os                 # For interacting with the operating system
import yaml               # For parsing YAML files
import logging            # For logging messages
import requests_toolbelt  # For working with HTTP requests
import urllib3            # For disabling SSL warnings
import argparse           # For parsing command-line arguments
from proxmoxer import ProxmoxAPI  # For interacting with Proxmox API

# Disable SSL warnings
urllib3.disable_warnings()

# Function to retrieve Proxmox settings from settings.yaml file
def get_settings():
    # Read settings from settings.yaml
    with open("settings.yaml", "r") as settings_file:
        settings = yaml.safe_load(settings_file)

    # Override settings with environment variables if set
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
    # Parse command-line arguments
    logger = logging.getLogger(__name__)
    logger.debug("Retrieving network information for node: %s", node)

    # Get network information using Proxmox API
    networks = proxmox.nodes(node).network.get()
    for network in networks:
        print("Network Information:")
        for key, value in network.items():
            print(f"{key}: {value}")
        print("-" * 20)

    logger.info("Network information printed.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", default=False, action="store_true", help="Enable debug mode")
    parser.add_argument("--users", default=False, action="store_true", help="Retrieve Proxmox users")
    parser.add_argument("--nodes", default=False, action="store_true", help="List all nodes")
    parser.add_argument("--network-info", default=False, action="store_true", help="Retrieve network information")
    args = parser.parse_args()

    # If no args are provided, print the help message
    if not any(vars(args).values()):
        parser.print_help()
        return

    # Configure logger for detailed logging if debug mode is enabled
    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=log_level, format="%(asctime)s - %(levelname)s - %(message)s")
    logger = logging.getLogger(__name__)

    settings = get_settings()

    # Create ProxmoxAPI instance using settings
    logger.debug("Connecting to Proxmox API...")
    proxmox = ProxmoxAPI(
        settings["proxmox_host"],
        user=settings["user"],
        password=settings["password"],
        verify_ssl=settings["verify_ssl"]
    )

    if args.users:
        get_users(proxmox)
    elif args.nodes:
        print_all_nodes(proxmox)
    elif args.network_info:
        print_network_info(proxmox, settings["target_node"])
    else:
        print_nodes_and_vms(proxmox)

if __name__ == "__main__":
    main()
