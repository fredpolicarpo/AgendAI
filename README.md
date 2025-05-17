# AgendAI: Intelligent Scheduling Assistant

## Project Description

AgendAI is an intelligent, chatbot-based virtual assistant designed to simplify and automate the appointment scheduling process for independent professionals and their clients. Utilizing generative artificial intelligence (Google Gemini) for natural and fluid communication, AgendAI interacts with users via Telegram, supporting text and voice commands (in Brazilian Portuguese).

The solution deeply integrates with the Google Cloud ecosystem:
* **Google Dialogflow CX:** For advanced dialogue management and natural language understanding (NLU).
* **Google Cloud Functions (Python):** As an orchestration layer that interacts with Dialogflow CX and the Gemini API.
* **Gemini API (via Vertex AI):** As the agent's brain, capable of understanding complex requests and using "tools" to interact with other services.
* **Google Calendar API (via Gemini Tools):** To check availability and manage events (creation, updates, cancellation) in the professional's calendar.
* **Google Sheets API (via Gemini Tools):** For logging interactions and storing/reading professional configurations.
* **Google Cloud Speech-to-Text:** To transcribe user voice commands.

The main goal of AgendAI is to optimize professionals' time management, reduce no-shows through reminders and clear cancellation policies, and significantly improve the scheduling experience for clients.

## Required Tools

To set up, develop, and deploy AgendAI, you will need the following tools:

### 1. Terraform

Terraform is used to manage infrastructure as code (IaC) on the Google Cloud Platform.

**Installation:**

We recommend following the [official Terraform installation guide from HashiCorp](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli) for the most up-to-date instructions. Below are summaries for common operating systems:

* **Linux (APT-based: Debian, Ubuntu, etc.)**
    1.  Ensure you have `gnupg`, `software-properties-common`, and `curl` installed:
        ```bash
        sudo apt-get update
        sudo apt-get install -y gnupg software-properties-common curl
        ```
    2.  Add the HashiCorp GPG key:
        ```bash
        curl -fsSL [https://apt.releases.hashicorp.com/gpg](https://apt.releases.hashicorp.com/gpg) | sudo apt-key add -
        ```
    3.  Add the official HashiCorp repository:
        ```bash
        sudo apt-add-repository "deb [arch=amd64] [https://apt.releases.hashicorp.com](https://apt.releases.hashicorp.com) $(lsb_release -cs) main"
        ```
    4.  Install Terraform:
        ```bash
        sudo apt-get update
        sudo apt-get install terraform
        ```
    5.  Verify the installation:
        ```bash
        terraform -v
        ```

* **Windows (using Chocolatey or Manually)**
    * **With Chocolatey (recommended):**
        1.  Install [Chocolatey](https://chocolatey.org/install).
        2.  In a PowerShell terminal as Administrator, run:
            ```powershell
            choco install terraform
            ```
    * **Manually:**
        1.  Download the Terraform executable for Windows from the [HashiCorp downloads page](https://www.terraform.io/downloads.html).
        2.  Extract the `terraform.exe` file to a folder on your system (e.g., `C:\Terraform`).
        3.  Add this folder to your `PATH` environment variable.
        4.  Verify the installation by opening a new terminal and running:
            ```powershell
            terraform -v
            ```

* **macOS (using Homebrew or Manually)**
    * **With Homebrew (recommended):**
        1.  Install [Homebrew](https://brew.sh/) if you haven't already.
        2.  In a terminal, run:
            ```bash
            brew tap hashicorp/tap
            brew install hashicorp/tap/terraform
            ```
    * **Manually:**
        1.  Download the Terraform binary for macOS from the [HashiCorp downloads page](https://www.terraform.io/downloads.html).
        2.  Extract the `terraform` file.
        3.  Move the binary to a directory included in your `PATH` (e.g., `/usr/local/bin`).
        4.  Verify the installation:
            ```bash
            terraform -v
            ```

### 2. Google Cloud SDK (gcloud CLI)

The Google Cloud SDK is essential for interacting with your GCP project, authenticating, and managing resources. Terraform uses the credentials configured via the `gcloud CLI`.

* **Installation:** Follow the [official Google Cloud SDK installation instructions](https://cloud.google.com/sdk/docs/install).
* **After installation, authenticate and configure your project:**
    ```bash
    gcloud auth login
    gcloud auth application-default login
    gcloud config set project YOUR_PROJECT_ID
    ```
    Replace `YOUR_PROJECT_ID` with your Google Cloud project ID.

### 3. Python

Python is the programming language used for the Google Cloud Functions that serve as the backend for AgendAI.

* **Installation:** Python 3.9 or higher is recommended.
    * Visit [python.org](https://www.python.org/downloads/) to download the installer for your operating system.
    * On Linux, it usually comes pre-installed or can be installed via a package manager (e.g., `sudo apt install python3 python3-pip python3-venv`).
    * Ensure `pip` (Python package manager) is installed and up to date.
* **Virtual Environments:** It is good practice to use virtual environments to manage project dependencies:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # Linux/macOS
    # .venv\Scripts\activate   # Windows
    ```

### 4. Telegram Account

* You will need a Telegram account to:
    1.  Interact with `BotFather` to create your AgendAI bot and obtain the API token.
    2.  Test your AgendAI bot as an end-user (client or professional).

## How to Set Up and Run the Project

1.  **Clone the Repository:** (If applicable, when the code is in a Git repository)
    ```bash
    # git clone REPOSITORY_URL
    # cd PROJECT_FOLDER_NAME
    ```
2.  **Configure Terraform Variables:**
    * Create a `terraform.tfvars` file in the folder containing your `.tf` files.
    * Fill this file with the necessary values, such as `gcp_project_id`, `gemini_api_key_value`, `telegram_bot_token_value`, `cloud_function_source_bucket_name`, etc. (as per the `variables.tf` file). **Do not add this file to version control if it contains secrets.**
3.  **Prepare the Cloud Function Code:**
    * Develop the Python code for your Cloud Functions.
    * Create a `requirements.txt` file with the Python dependencies.
    * Create a ZIP file of your function's code folder.
    * Upload this ZIP to the Google Cloud Storage bucket that will be created by Terraform (the bucket name is defined in the `cloud_function_source_bucket_name` variable).
4.  **Apply the Infrastructure with Terraform:**
    * Navigate to the folder with your Terraform files.
    * Run `terraform init`
    * Run `terraform plan -var-file="terraform.tfvars"`
    * Run `terraform apply -var-file="terraform.tfvars"`
5.  **Manual Post-Terraform Configuration:**
    * Refer to the `AgendAI_Manual_GCP_Setup_Steps.md` document (or similar) for configuration steps that need to be done manually in the Google Cloud console, such as detailed Dialogflow CX configuration, creation of Google Sheets, OAuth 2.0 consent screen setup, and Gemini Tools configuration in Vertex AI.
6.  **Development and Testing:**
    * Continue developing the Cloud Functions code and the conversation logic in Dialogflow CX.
    * Test all flows exhaustively.

## Project Documentation

* **Product Requirements Document (PRD):** `PRD_AgendAI.md` (or link to the document)
* **Technical Specification:** `TechSpec_AgendAI_P1.md` (or link to the document)
* **Style Guide & Coding Conventions:** `StyleGuide_AgendAI.md` (or link to the document)
* **Manual GCP Setup Steps:** `Manual_GCP_Setup_AgendAI.md` (or link to the document)

*(Adapt file names according to your organization)*

## Contributing

(Placeholder for contribution guidelines if the project is collaborative.)

## License

(Placeholder for the project license, e.g., MIT, Apache 2.0, etc.)
