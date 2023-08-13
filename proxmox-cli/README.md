# Proxmox CLI Tool

A Python CLI tool to interact with Proxmox using the Proxmoxer library.

## Table of Contents
- [Introduction](#introduction)
- [Setup](#setup)
  - [Pip Requirements](#pip-requirements)
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
    git clone https://github.com/yourusername/proxmox-cli.git
    cd proxmox-cli
    ```

2. Create a `settings.yaml` file in the root directory with your Proxmox credentials and settings:
    ```yaml
    proxmox_host: "your-proxmox-hostname"
    user: "your-username"
    password: "your-password"
    verify_ssl: false
    ```
    Make sure to protect the `settings.yaml` file to keep your credentials secure:
    ```bash
    chmod 600 settings.yaml
    ```

3. Install the required Python packages using pip:
    ```bash
    pip install -r requirements.txt
    ```

4. It's recommended to use a virtual environment for better isolation:
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

## Examples
- Display Proxmox users:
    ```bash
    python main.py --users
    ```
- List available nodes and display their information:
    ```bash
    python main.py --nodes
    ```

## Author
Sean Smith
