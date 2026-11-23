# GitHub Actions Secrets vs Variables & Multi-Environment Configuration Demo

A clean, production-grade demonstration project designed for a 15-minute DevOps knowledge-sharing session. It illustrates how modern applications consume configuration from environment variables, how to cleanly separate **sensitive credentials** (`secrets`) from **non-sensitive settings** (`vars`), and how GitHub Environments allow the same workflow and application code to adapt across **DEV**, **STAGING**, and **PRODUCTION**.

---

## Table of Contents

1. [Key Concepts Demonstrated](#key-concepts-demonstrated)
2. [Project Structure](#project-structure)
3. [Local Development Setup](#local-development-setup)
   - [Virtual Environment Setup](#1-virtual-environment-setup)
   - [Dependency Installation](#2-dependency-installation)
   - [Running Locally](#3-running-the-application-locally)
   - [Expected Local Output](#4-expected-local-output)
4. [GitHub Repository Setup (Git Commands)](#github-repository-setup)
5. [GitHub Environments Configuration](#github-environments-configuration)
   - [Creating GitHub Environments](#1-creating-environments-in-github)
   - [Variables vs Secrets Reference Matrix](#2-variables-and-secrets-matrix)
   - [Repository-Level vs Environment-Level Configuration](#3-repository-level-vs-environment-level-configuration)
6. [Running the GitHub Actions Workflow](#running-the-github-actions-workflow)
7. [Expected Workflow Outputs across Environments](#expected-workflow-outputs)
8. [Important Technical Details](#important-technical-details)
9. [Troubleshooting Common Issues](#troubleshooting-common-issues)
10. [15-Minute Live Presentation Sequence](#15-minute-live-presentation-sequence)

---

## Key Concepts Demonstrated

- **Local Configuration (`.env`)**: A developer-friendly local convention used to supply environment variables without polluting the global OS environment.
- **`.env` is NOT sent to CI/CD**: `.env` is deliberately excluded by `.gitignore`. GitHub Actions runs in a fresh, isolated VM and does not receive local files.
- **GitHub Actions Contexts (`vars` vs `secrets`)**:
  - `vars`: Stores non-sensitive, human-readable configuration (e.g., URLs, log levels, environment names). These are visible in workflow logs and GitHub settings.
  - `secrets`: Encrypted storage for sensitive credentials (API tokens, passwords, private keys). Values are masked (`***`) in workflow logs automatically by GitHub.
- **Environment Isolation (`DEV`, `STAGING`, `PRODUCTION`)**: By assigning the `environment` property to a job, GitHub Actions pulls variables and secrets specifically scoped to that target environment.
- **Single Source of Truth**: The application code (`app.py`) remains 100% agnostic to whether it is running on a laptop or inside GitHub Actions.
- **Process Environment Precedence**: `load_dotenv(override=False)` ensures that runtime process environment variables supplied by GitHub Actions take precedence over any `.env` file.
- **Zero Log Leakage**: Secrets are never printed in application logs or standard output—only their configuration status (`True`/`False`) is reported.

---

## Project Structure

```text
github-actions-config-demo/
│
├── .github/
│   └── workflows/
│       └── config-demo.yml   # Workflow dispatching jobs across DEV, STAGING, PRODUCTION
│
├── .env                      # Local development dummy values (IGNORED BY GIT)
├── .env.example              # Template showing required variables (COMMITTED)
├── .gitignore                # Protects secrets, caches, and virtual environments
├── app.py                    # Demonstration Python application
├── requirements.txt          # Python dependencies (python-dotenv)
└── README.md                 # Complete documentation and presentation guide
```

---

## Local Development Setup

### 1. Virtual Environment Setup

Open your terminal in the project directory and create a virtual environment:

```bash
# On Linux / macOS
python3 -m venv .venv
source .venv/bin/activate

# On Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Dependency Installation

Install the required packages:

```bash
pip install -r requirements.txt
```

### 3. Running the Application Locally

The local `.env` file is pre-populated with development dummy values:

```env
APP_ENV=development
API_BASE_URL=https://dev-api.example.com
LOG_LEVEL=debug

API_TOKEN=local-demo-token
DATABASE_PASSWORD=local-demo-password
```

Run the application:

```bash
python app.py
```

### 4. Expected Local Output

```text
========================================
APPLICATION CONFIGURATION
========================================

Environment: development
API Base URL: https://dev-api.example.com
Log Level: debug

API Token configured: True
Database password configured: True

========================================
```

> **Note**: Notice how `API Token` and `Database password` only output `True`. Even during local development, actual secret strings are never logged to the console.

---

## GitHub Repository Setup

To push this demonstration project to your GitHub account, run the following Git commands locally:

```bash
# 1. Initialize local git repository (if not already initialized)
git init

# 2. Set the default branch to main
git branch -M main

# 3. Verify that .env is ignored and not staged
git status

# 4. Stage all project files (.env is ignored automatically)
git add .

# 5. Commit the files
git commit -m "feat: setup GitHub Actions secrets and variables demonstration project"

# 6. Add your remote GitHub repository URL (replace with your repo URL)
git remote add origin https://github.com/<YOUR-USERNAME>/<YOUR-REPO-NAME>.git

# 7. Push to GitHub
git push -u origin main
```

---

## GitHub Environments Configuration

### 1. Creating Environments in GitHub

Follow these steps in your GitHub repository web interface:

1. Navigate to **Settings** (top tab in your repository).
2. In the left sidebar, click **Environments** (under the "Code and automation" section).
3. Click the **New environment** button.
4. Name the environment **`DEV`** (uppercase) and click **Configure environment**.
5. Repeat steps 3–4 to create **`STAGING`** and **`PRODUCTION`**.

---

### 2. Variables and Secrets Matrix

In each environment's configuration page:
- Click **Add variable** under **Environment variables** for non-sensitive values.
- Click **Add secret** under **Environment secrets** for credentials.

Configure the following dummy values:

#### Environment Variables (Non-Sensitive)

| Variable Name | DEV | STAGING | PRODUCTION |
|---|---|---|---|
| `APP_ENV` | `development` | `staging` | `production` |
| `API_BASE_URL` | `https://dev-api.example.com` | `https://staging-api.example.com` | `https://api.example.com` |
| `LOG_LEVEL` | `debug` | `info` | `warning` |

#### Environment Secrets (Sensitive Credentials)

| Secret Name | DEV | STAGING | PRODUCTION |
|---|---|---|---|
| `API_TOKEN` | `dev-demo-token` | `staging-demo-token` | `production-demo-token` |
| `DATABASE_PASSWORD` | `dev-demo-password` | `staging-demo-password` | `production-demo-password` |

*(All values above are safe dummy strings for presentation purposes).*

---

### 3. Repository-Level vs Environment-Level Configuration

| Feature | Repository Level | Environment Level |
|---|---|---|
| **Location** | `Settings -> Secrets and variables -> Actions` | `Settings -> Environments -> [Env Name]` |
| **Scope** | Available to any workflow job in the repository. | Available **only** to jobs specifying `environment: <name>`. |
| **Use Case** | Shared tools, global tokens, registry credentials. | Environment-specific endpoints, credentials, tier configs. |
| **Governance** | No approval gates. | Supports protection rules, reviewers, and branch policies. |

#### Why These Configuration Items Belong at the Environment Level
- **Isolation of Blast Radius**: A developer running a test job should never accidentally access the production database password or write to the production API.
- **Configuration Parity**: The variable names (`API_BASE_URL`, `DATABASE_PASSWORD`) remain identical across environments. Only their underlying values change depending on the targeted environment.
- **Deployment Protection Rules**: In real-world enterprise environments, GitHub Environments can enforce manual approval gates or restrict execution to the `main` branch for `PRODUCTION`.

---

## Running the GitHub Actions Workflow

1. Navigate to the **Actions** tab in your repository.
2. In the left sidebar, select **Configuration Demo**.
3. Click the **Run workflow** dropdown button on the right.
4. In the **Select target environment** dropdown, choose:
   - `DEV`, `STAGING`, or `PRODUCTION`
5. Click the green **Run workflow** button.
6. Click into the newly triggered run and open the **Run application with environment configuration** step to view the output.

---

## Expected Workflow Outputs

### When DEV is selected:

```text
========================================
APPLICATION CONFIGURATION
========================================

Environment: development
API Base URL: https://dev-api.example.com
Log Level: debug

API Token configured: True
Database password configured: True

========================================
```

### When STAGING is selected:

```text
========================================
APPLICATION CONFIGURATION
========================================

Environment: staging
API Base URL: https://staging-api.example.com
Log Level: info

API Token configured: True
Database password configured: True

========================================
```

### When PRODUCTION is selected:

```text
========================================
APPLICATION CONFIGURATION
========================================

Environment: production
API Base URL: https://api.example.com
Log Level: warning

API Token configured: True
Database password configured: True

========================================
```

---

## Important Technical Details

1. **Explicit Workflow Mapping**:
   GitHub Actions does not inject all repository secrets or variables automatically into step processes. They must be explicitly mapped in the workflow step's `env` block:
   ```yaml
   env:
     APP_ENV: ${{ vars.APP_ENV }}
     API_TOKEN: ${{ secrets.API_TOKEN }}
   ```
2. **Context Distinction**:
   - `vars.<NAME>` reads from the non-sensitive configuration store.
   - `secrets.<NAME>` reads from the encrypted credentials vault.
3. **`override=False` in `load_dotenv`**:
   `load_dotenv(override=False)` ensures that environment variables provided by GitHub Actions (or Docker, Kubernetes, etc.) take precedence over values from any local `.env` file.
4. **Environment Binding**:
   The job specifies `environment: ${{ inputs.environment }}`. If this line is omitted, GitHub Actions has no access to environment-scoped secrets or variables.
5. **Decoupled from Git Branches**:
   Because `workflow_dispatch` accepts the environment as an input, you can test DEV, STAGING, or PRODUCTION on any branch without changing code.

---

## Troubleshooting Common Issues

| Symptom | Cause | Solution |
|---|---|---|
| `Environment: [NOT SET]` or empty in CI | Variable not mapped in workflow `env` block or missing from GitHub Environment variables. | Ensure variable exists in GitHub Settings -> Environments -> [Env] -> Variables and is mapped in `config-demo.yml`. |
| `API Token configured: False` | Secret name typo or missing in GitHub Environment secrets. | Verify secret name matches `API_TOKEN` exactly (case-sensitive) under Environment secrets. |
| Job fails with "Environment does not exist" | Name mismatch in dropdown choice vs GitHub environment name. | Check that the environment name in GitHub Settings is exactly `DEV`, `STAGING`, or `PRODUCTION`. |
| Local values appear instead of GitHub Actions values | `override=True` was passed to `load_dotenv()`, or process env was not mapped. | Ensure `load_dotenv(override=False)` is used and variables are mapped under `env:` in the workflow step. |
| Secrets exposed in logs | Printing secret variables directly in `print()` statements. | Never log raw secret variables. Always evaluate presence via booleans or length checks. |

---

## 15-Minute Live Presentation Sequence

Use this structured schedule during your team session:

| Timestamp | Phase | What to Show / Say |
|---|---|---|
| **0:00 - 2:00** | **The Problem Statement** | • Why we don't hardcode config or credentials.<br>• Why `.env` files belong only on local machines.<br>• The 12-Factor App principle: config stored in the environment. |
| **2:00 - 5:00** | **Code Walkthrough (`app.py`)** | • Show `load_dotenv(override=False)` and explain precedence.<br>• Explain the split: `vars` (logged) vs `secrets` (masked as booleans).<br>• Run `python app.py` locally to show development output. |
| **5:00 - 8:00** | **GitHub Settings Tour** | • Open GitHub: **Settings -> Environments**.<br>• Show `DEV`, `STAGING`, and `PRODUCTION`.<br>• Show the distinction between Environment Variables vs Environment Secrets.<br>• Highlight protection rules (e.g. required reviewers for PRODUCTION). |
| **8:00 - 11:00** | **Workflow Walkthrough (`config-demo.yml`)** | • Show `workflow_dispatch` with the dropdown choices.<br>• Point out `environment: ${{ inputs.environment }}` (the bridge).<br>• Show the `env:` block mapping `${{ vars.* }}` and `${{ secrets.* }}`. |
| **11:00 - 13:30** | **Live Execution & Verification** | • Trigger workflow with `DEV` -> Inspect logs.<br>• Trigger workflow with `PRODUCTION` -> Notice `api.example.com` & `warning` level without changing any code.<br>• Point out that `API_TOKEN` shows `True` while keeping secret values hidden. |
| **13:30 - 15:00** | **Q&A & Key Takeaways** | • Never commit `.env`.<br>• Use `vars` for non-sensitive, `secrets` for credentials.<br>• Use GitHub Environments for environment-specific isolation. |
