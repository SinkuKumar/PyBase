"""
Deployment Automation Script

This script provides functions to automate the deployment of a repository,
including cloning, updating, setting permissions, and handling environment
configurations. It supports integration with a remote deployment server.

Modules Used:
- os: For environment variables and file handling.
- json: For parsing and formatting JSON responses.
- subprocess: For executing shell commands.
- requests: For making HTTP requests to the deployment server.
- yaml: For parsing configuration files.
"""

import os
import json
import subprocess
import requests
import yaml


def get_username():
    """Retrieve the username from environment variables for Windows or macOS/Linux."""
    return os.getenv("USERNAME") or os.getenv("USER")


def load_config(config_path="deployment.yaml"):
    """Load deployment configuration from a YAML file.

    Args:
        config_path (str): Path to the YAML configuration file.

    Returns:
        dict: Parsed YAML configuration.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file {config_path} not found.")

    with open(config_path, "r") as file:
        return yaml.safe_load(file)


def deploy_repo(username, server_url, repo_url, branch="main", commit_hash=None, local_dir="./test", exclude_ext=".ipynb"):
    """Deploy the repository using the provided parameters.

    Args:
        username (str): The username of the person deploying.
        server_url (str): The URL of the deployment server.
        repo_url (str): The URL of the repository.
        branch (str, optional): The branch to deploy. Defaults to "main".
        commit_hash (str, optional): Specific commit hash to deploy.
        local_dir (str, optional): Local directory for deployment.
        exclude_ext (str, optional): File extension to exclude.
    """
    payload = {
        "username": username,
        "repo_url": repo_url,
        "branch": branch,
        "commit_hash": commit_hash,
        "local_dir": local_dir,
        "exclude_ext": exclude_ext,
    }

    try:
        response = requests.post(f"{server_url}/deploy", json=payload)
        response_data = response.json()

        if response.status_code == 200:
            print("Deployment successful!")
        else:
            print("Deployment failed!")

        print(json.dumps(response_data, indent=4))
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


def execute_command(command):
    """Execute a shell command and return the result.

    Args:
        command (list): Command to be executed as a list.

    Returns:
        dict: Success status and command output or error message.
    """
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        return {"success": True, "output": result.stdout.strip()}
    except subprocess.CalledProcessError as e:
        return {"success": False, "error": e.stderr.strip() if e.stderr else str(e)}


def clone_or_update_repo(repo_url, branch, commit_hash, local_dir, logs):
    """Clone or update a Git repository based on given parameters.

    Args:
        repo_url (str): URL of the repository.
        branch (str): Branch to checkout.
        commit_hash (str, optional): Specific commit hash to checkout.
        local_dir (str): Directory where the repository is stored.
        logs (list): List to store log messages.

    Returns:
        dict: Execution result with success status and message.
    """
    if not os.path.exists(local_dir):
        logs.append(f"Cloning repository {repo_url} into {local_dir}")
        response = execute_command(["git", "clone", "-b", branch, repo_url, local_dir])
    else:
        logs.append("Repository already exists. Fetching latest changes.")
        response = execute_command(["git", "-C", local_dir, "fetch"])

    if not response["success"]:
        return response

    if commit_hash:
        logs.append(f"Checking out specific commit {commit_hash}")
        response = execute_command(["git", "-C", local_dir, "checkout", commit_hash])
    else:
        logs.append(f"Pulling latest commit from branch {branch}")
        response = execute_command(["git", "-C", local_dir, "checkout", branch])
        if response["success"]:
            response = execute_command(["git", "-C", local_dir, "pull", "origin", branch])

    return response


def set_permission_readonly(local_dir, exclude_ext, logs):
    """Set read-only permissions for files in a directory, excluding specific extensions.

    Args:
        local_dir (str): Directory to modify.
        exclude_ext (str): File extension to exclude from read-only settings.
        logs (list): List to store log messages.
    """
    for root, _, files in os.walk(local_dir):
        for file in files:
            if not file.endswith(exclude_ext):
                file_path = os.path.join(root, file)
                os.chmod(file_path, 0o444)
                logs.append(f"Set {file_path} to read-only.")


def set_permission_full(local_dir, logs):
    """Set full permissions for all files in a directory.

    Args:
        local_dir (str): Directory to modify.
        logs (list): List to store log messages.
    """
    for root, _, files in os.walk(local_dir):
        for file in files:
            file_path = os.path.join(root, file)
            os.chmod(file_path, 0o777)
            logs.append(f"Set {file_path} to full permission.")


def create_env_file(local_dir, env_config):
    """Create a .env file with environment variables in the specified directory.

    Args:
        local_dir (str): Directory where the .env file will be created.
        env_config (dict): Dictionary containing environment variables.
    """
    file_path = os.path.join(local_dir, ".env")
    print(f"Creating .env file at {file_path}")
    with open(file_path, "w") as env_file:
        for key, value in env_config.items():
            env_file.write(f"{key} = '{value}'\n")


if __name__ == "__main__":
    username = get_username()
    server_url = "http://localhost:9000"
    config = load_config()
    local_dir = config.get("local_dir", "./test")

    deploy_repo(
        username=username,
        server_url=server_url,
        repo_url=config["repo_url"],
        branch=config.get("branch", "main"),
        commit_hash=config.get("commit_hash"),
        local_dir=local_dir,
        exclude_ext=config.get("exclude_ext", ".ipynb"),
    )

    if "env" in config:
        create_env_file(local_dir, config["env"])
