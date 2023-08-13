# Proxmox CLI Tool

A Python CLI tool to interact with Proxmox using the Proxmoxer library.

## Table of Contents
- [Introduction](#introduction)
- [Setup](#setup)
  - [Settings](#settings)
  - [Virtual Environment](#virtual-environment)
- [Usage](#usage)
- [Flags](#flags)
- [Examples](#examples)
- [Author](#author)

## Introduction
This command-line tool allows you to interact with Proxmox using various commands.

## Setup
1. Clone this repository:
    ```bash
    git clone https://github.com/smithlabs/proxmox-cli.git
    cd proxmox-cli
    ```

## Settings
2. Create a `settings.yaml` file in the root directory with your Proxmox credentials and settings:
    Example on a fresh out-of-the-box Proxmox install
    ```yaml
    proxmox_host: "proxmox.smithlabs.net"
    user: "root@pam"
    password: "MySecurePassword123!"
    verify_ssl: False
    target_node: "pve"  # Specify your target node name here
    ```
    Make sure to protect the `settings.yaml` file to keep your credentials secure:
    ```bash
    chmod 600 settings.yaml
    ```
## Virtual Environment
3. It's recommended to use a virtual environment for better isolation:
    ```bash
    # Create a virtual environment
    python -m venv venv

    # Activate the virtual environment
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate

    # Install required packages
    pip install -r requirements.txt
    ```

## Usage
Run the `main.py` script with the desired flags to interact with Proxmox.

## Flags
- `--users`: Retrieve and display Proxmox users' information.
- `--nodes`: List all available nodes and display their information.
- `--network-info`: Retrieve and display network information for the specified target node.

## Examples
- Display Proxmox users:
    ```bash
    python main.py --users
    ```
- List available nodes and display their information:
    ```bash
    python main.py --nodes
    ```
- Retrieve and display network information for the specified target node:
    ```bash
    python main.py --network-info
    ![python main.py --network-info screenshot](https://github.com/smithlabs/homelab/blob/main/assets/main_py_get_network_info.png?raw=true)
    ```

## Author
Sean Smith
