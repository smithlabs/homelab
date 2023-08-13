import os
import yaml
import logging
import requests_toolbelt
import urllib3
import argparse
from proxmoxer import ProxmoxAPI

urllib3.disable_warnings()

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

def print_nodes_and_vms(proxmox):
    logger = logging.getLogger(__name__)

    logger.debug("Retrieving nodes and their associated virtual machines...")
    for node in proxmox.nodes.get():
        for vm in proxmox.nodes(node["node"]).qemu.get():
            print(f"{vm['vmid']}. {vm['name']} => {vm['status']}")
    logger.info("Nodes and their associated virtual machines printed.")

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

def get_all_nodes(proxmox):
    nodes = proxmox.nodes.get()
    return [node["node"] for node in nodes]

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

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", default=False, action="store_true", help="Enable debug mode")
    parser.add_argument("--users", default=False, action="store_true", help="Retrieve Proxmox users")
    parser.add_argument("--nodes", default=False, action="store_true", help="List all nodes")
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
    else:
        print_nodes_and_vms(proxmox)

if __name__ == "__main__":
    main()
