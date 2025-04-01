# PyBase

- A minimal, Python repository template with .gitignore, .vscode extensions, code formatter and linter.
- Built in CI-CD for better deployments.

<p align="center">
  <img src="https://s3.dualstack.us-east-2.amazonaws.com/pythondotorg-assets/media/community/logos/python-logo-only.png" alt="Python Logo" height="100">
  &nbsp; &nbsp; &nbsp; &nbsp;
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Visual_Studio_Code_1.35_icon.svg/480px-Visual_Studio_Code_1.35_icon.svg.png" alt="VS Code Logo" height="100">
</p>

## VS Code Configuration for Python Development

This repo includes a recommended set of VS Code extensions and settings to enhance Python development.

## 📦 Recommended Extensions

To ensure a smooth development experience, install the following extensions by adding them to your `.vscode/extensions.json` file:

```json
{
  "recommendations": [
    "ms-python.isort", // Sorts Python imports automatically
    "ms-python.flake8", // Linter for enforcing code quality
    "ms-python.python", // Core Python extension for VS Code
    "ms-python.pylint", // Another Python linter
    "ms-python.debugpy", // Debugging support for Python
    "yzane.markdown-pdf", // Converts Markdown to PDF
    "ms-toolsai.jupyter", // Jupyter Notebook support
    "qwtel.sqlite-viewer", // View SQLite databases
    "ritwickdey.liveserver", // Live server for web development
    "ms-python.vscode-pylance", // Python language server
    "ms-toolsai.jupyter-keymap", // Key bindings for Jupyter
    "ms-python.black-formatter", // Black code formatter
    "ms-toolsai.jupyter-renderers", // Jupyter notebook renderers
    "ms-toolsai.vscode-jupyter-slideshow", // Jupyter slideshow support
    "ms-toolsai.vscode-jupyter-cell-tags" // Jupyter cell tagging
  ]
}
```

## ⚙️ VS Code Settings

To maintain consistent formatting and linting, use the following settings in `.vscode/settings.json`:

```json
{
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter", // Use Black for formatting
    "editor.formatOnSave": true // Auto-format on save
  },
  "black-formatter.args": ["--line-length", "200"],
  "flake8.args": ["--max-line-length=200"],
  "pylint.args": ["--max-line-length=200"],
  "editor.formatOnSave": true,
  "editor.formatOnPaste": true,
  "diffEditor.codeLens": true, // Show inline code lens in diff view
  "editor.codeActionWidget.includeNearbyQuickFixes": true // Enable quick fixes
}
```

---

This setup ensures consistent formatting, efficient linting, and an improved development workflow. 🚀

# Deployment

## Project Setup

### 1. Use Git Template

Always use the Git template repository to create your project. It contains the necessary template code required for developing automation scripts. You can access it here: [PyBase GitHub Repository](https://github.com/Graphxsys/PyBase).

### 2. Set Up a Virtual Environment

To develop your script, always create a new virtual environment using Python **3.10.11**, as this is the version used in the production server.

#### Steps to Set Up the Virtual Environment:

```sh
python3 -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate     # For Windows
```

Once the virtual environment is activated, install the required dependencies:

```sh
pip install -r requirements.txt
```

### 3. Install and Manage Dependencies

During development, use `pip` to install additional packages. Before pushing changes to GitHub, update the `requirements.txt` file:

```sh
pip freeze > requirements.txt
```

This ensures that all required dependencies are stored and can be installed in production.

## Deployment Setup

### 1. Prepare `deployment.yaml`

Before deploying the script, ensure your `deployment.yaml` file is available at the root of the project. This file specifies the necessary environment variables and deployment settings.

Example `deployment.yaml` format:

```yaml
repo_url: "https://github.com/SinkuKumar/PyBase.git"
branch: "main"
commit_hash: ""
local_dir: "./Users/Sinku/Desktop/Deployment"
exclude_ext: ".ipynb"

env:
  # SMTP Server Credentials
  SMTP_ADDRESS: "smtp.office365.com"
  SMTP_PORT: 587
  SMTP_ACCOUNT: "email@domian.com"
  SMTP_PASSWORD: "secret-password"

  # SQL Server Credentials
  SQL_SERVER: "127.0.0.1"
  SQL_DATABASE: "DB_Name"
  SQL_USERNAME: "username"
  SQL_PASSWORD: "password"
```

### 2. Push Changes to GitHub

To commit and push your changes, use the following commands:

```sh
git add .
git commit -m "Your commit message"
git pull
git push
```

### 3. Trigger Deployment

Once the code is pushed to GitHub, trigger the deployment script by running:

```sh
python utils/deployment.py
```

## Rollback to a Previous Commit

If you encounter an issue after deployment, you can revert to a previous commit using `git log`, which provides commit history.

Example:

```sh
(venv) Sinku@Macbook4 CI-CD-Python % git log
commit f96b8b261cf08040c023e2328366dfb751404629 (HEAD -> main, origin/main, origin/HEAD)
Author: SinkuKumar <sudosinku@gmail.com>
Date:   Tue Mar 11 14:32:25 2025 +0530

    Add deployment configuration and enhance deployment functionality
```

To deploy a specific commit, update the `commit_hash` in `deployment.yaml` and redeploy the script. This ensures that your project rolls back to the desired checkpoint.
