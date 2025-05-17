# AgendAI: Manual Google Cloud Setup Steps

This document details the manual configuration steps required in the Google Cloud Platform (GCP) to complete the AgendAI project setup, following the successful execution of the Terraform scripts. The Terraform scripts create the base infrastructure, but certain application-specific configurations, user interfaces, and external processes require manual intervention.

## Prerequisites

* An active Google Cloud account with a created GCP project and an associated billing account.
* The `gcloud` CLI installed and authenticated with sufficient permissions to perform the configurations below.
* Terraform installed and the AgendAI project's Terraform scripts successfully applied.
* A Telegram account to create the bot.

## Manual Configuration Steps

### 1. Google Cloud Project (If not already existing)

* **Action:** If you do not already have a dedicated GCP project for AgendAI, create one via the [Google Cloud Console](https://console.cloud.google.com/).
* **Details:** Ensure a billing account is associated with the project. Note down the **Project ID**, as it will be used in various configurations and the Terraform scripts (as `var.gcp_project_id`).
* **Terraform:** Terraform assumes the project already exists and that APIs will be enabled within it.

### 2. Detailed Dialogflow CX Agent Configuration

The Terraform scripts create the basic Dialogflow CX agent. The conversation logic needs to be configured manually:

* **Action:** Access [Dialogflow CX in the GCP Console](https://console.cloud.google.com/dialogflow).
* **Details:**
    1.  **Select Agent:** Find and select the agent created by Terraform (the display name was set in `var.dialogflow_cx_agent_display_name`).
    2.  **Create Flows:** Define the main conversation flows, such as "ConfiguracoesProfissional" (ProfessionalSettings), "FluxoAgendamentoCliente" (ClientBookingFlow), "TarefasProfissional" (ProfessionalTasks), "NotificacaoCliente" (ClientNotification), as per the technical specification.
    3.  **Create Intents:** Within each flow, define the intents the user might express (e.g., `configurar_disponibilidade` (configure_availability), `solicitar_agendamento` (request_appointment), `confirmar_agendamento` (confirm_appointment)). Provide training phrases in Brazilian Portuguese.
    4.  **Create Entities:** Define custom entities to extract specific information from user phrases (e.g., `tipo_servico` (service_type), `periodo_dia` (day_period)). Use system entities for dates, times, etc.
    5.  **Create Pages:** Build the pages within flows to manage different conversation states and collect parameters.
    6.  **Define Transition Routes:** Configure how the conversation flows between pages based on user intents or conditions.
    7.  **Configure Webhooks:**
        * Obtain the URLs of your Google Cloud Functions (generated as output by Terraform, `cloud_functions_urls`).
        * In the "Manage" -> "Webhooks" section of your Dialogflow CX agent, create and configure webhooks to point to the correct Cloud Function URLs that will handle the backend logic (e.g., `handle_dialogflow_webhook`).
        * Configure authentication for the webhooks if necessary (the current Terraform scripts configure functions to be invoked by `allUsers` for testing, but for production, you should restrict this and set up webhook authentication).
    8.  **Configure Fulfillment:** In the appropriate pages or routes, configure fulfillment to call the webhooks when backend logic is needed.
* **Language:** Confirm that the agent's primary language is set to `pt-BR`.

### 3. Creation and Configuration of Google Sheets

AgendAI uses Google Sheets for logging and configuration. These need to be created manually:

* **Action:** Access [Google Sheets](https://sheets.google.com) with the Google account that will be used by the professional or a service account (if applicable and configured).
* **Details:**
    1.  **Create "Professional_Config" Sheet:**
        * Name the sheet (e.g., `AgendAI - Professional Config`).
        * Define the following columns in the first row: `ProfessionalID`, `AvailabilityPatternJSON`, `CancellationLimitHours`, `CancellationFeeAmount`, `Currency`.
        * Note down the **Sheet ID**. You can find it in the URL (e.g., `https://docs.google.com/spreadsheets/d/THIS_IS_THE_ID/edit`).
    2.  **Create "Booking_Logs" Sheet:**
        * Name the sheet (e.g., `AgendAI - Booking Logs`).
        * Define the following columns in the first row: `Timestamp`, `LogID`, `ClientID`, `ProfessionalID`, `RequestedSlot_StartTime`, `RequestedSlot_EndTime`, `Service`, `Status`, `CalendarEventID`, `ClientNotifiedTimestamp`, `CancellationFeeApplied`.
        * Note down the **Sheet ID**.
    3.  **Provide Sheet IDs to Cloud Functions:**
        * These Sheet IDs need to be provided as environment variables to your Cloud Functions. You can update your `variables.tf` or `terraform.tfvars` file to include these IDs and re-apply the Cloud Functions configuration, or configure them directly in the Cloud Function console (less ideal for IaC).
        * Example in `variables.tf`:
            ```terraform
            variable "professional_config_sheet_id" {
              description = "The ID of the Google Sheet for professional configuration."
              type        = string
            }
            variable "booking_logs_sheet_id" {
              description = "The ID of the Google Sheet for booking logs."
              type        = string
            }
            ```
            And then use them in the environment variables of the functions in `cloud_functions.tf`.
    4.  **Permissions (Important for Access by Gemini Tools/Cloud Functions):**
        * If Gemini (via tools) or Cloud Functions (using their service account) need to directly access these sheets, you will have to share the sheets with the relevant service account (e.g., `YOUR_FUNCTION_NAME@YOUR_PROJECT_ID.iam.gserviceaccount.com` or the service account Gemini uses for tools) with edit permissions.
        * However, the preferred method for accessing user data (like these sheets, if considered professional's data) is through the OAuth 2.0 flow, where the professional grants permission.

### 4. Creation of the Telegram Bot

* **Action:** Create your bot on the Telegram platform.
* **Details:**
    1.  Open Telegram and search for `BotFather`.
    2.  Start a chat with BotFather and send the `/newbot` command.
    3.  Follow the instructions to give your bot a name and a username.
    4.  BotFather will provide you with an **HTTP API Token**.
    5.  **Save this token securely.** This is the value you should provide to the `telegram_bot_token_value` variable in your `terraform.tfvars` file so it can be stored in Google Secret Manager.

### 5. Source Code and Deployment of Cloud Functions

The Terraform scripts create the Cloud Function resources, but not the code itself.

* **Action:** Develop the Python code for your Cloud Functions.
* **Details:**
    1.  **Write the Code:** Create the Python files (e.g., `main.py`, `dialogflow_handler.py`, `services/calendar_service.py`, etc.) with the backend logic described in the technical specification.
    2.  **Create `requirements.txt`:** List all Python dependencies for your project (e.g., `google-api-python-client`, `google-auth-oauthlib`, `pydantic`, `functions-framework`, `google-cloud-aiplatform`).
    3.  **Create a ZIP File:** Compress the folder containing your Python code and `requirements.txt` into a ZIP file (e.g., `dialogflow_handler.zip`, as defined in `var.cloud_functions_config` in Terraform).
    4.  **Upload to Cloud Storage:**
        * Access the Cloud Storage bucket created by Terraform (the name is in `var.cloud_function_source_bucket_name`).
        * Upload your ZIP file to this bucket. The ZIP object name must match what was defined in `source_archive_object` in the Terraform function configuration.
    5.  **Deploy (if not done by Terraform `apply` after upload):** If you applied Terraform before uploading the ZIP, you might need to force a new deployment of the function for it to use the new code, or the next `terraform apply` (if it detects a change in the source object, which might not happen automatically) could update it. The most reliable way is to upload the ZIP *before* applying the Cloud Function configuration in Terraform for the first time or when updating the code.

### 6. Configuration of OAuth 2.0 Consent Screen and Client ID

This is crucial to allow AgendAI (specifically Gemini tools) to access the professional's Google Calendar and Google Sheets data on their behalf.

* **Action:** Configure the consent screen and create an OAuth 2.0 Client ID in the [GCP Console under APIs & Services -> Credentials](https://console.cloud.google.com/apis/credentials).
* **Details:**
    1.  **OAuth Consent Screen:**
        * Select User Type: "External" (if users outside your GCP organization will use it) or "Internal".
        * Fill in application information: Application name (e.g., AgendAI), User support email, App logo (optional).
        * **Scopes:** Add the necessary scopes. For AgendAI P1, you will need at least:
            * `https://www.googleapis.com/auth/calendar` (or more specific like `.../auth/calendar.events`)
            * `https://www.googleapis.com/auth/spreadsheets` (or more specific if only read/write to certain sheets is needed)
        * Add authorized domains if applicable.
        * Provide links to your privacy policy and terms of service (even if they are placeholders for development).
        * Save and continue.
    2.  **Credentials -> Create Credentials -> OAuth client ID:**
        * Application type: "Web application".
        * Name: A name for your OAuth client (e.g., "AgendAI Web Client for Gemini Tools").
        * **Authorized redirect URIs:** This is important. For the OAuth 2.0 flow, you'll need a URI where Google will redirect the user after authorization. If Gemini tools manage the OAuth flow internally (which is likely for GCP tool integrations), the Vertex AI / Gemini documentation for "tool use" with OAuth should specify what URIs are needed or how this flow is managed. For local testing or if your Cloud Function needs to initiate the flow, it might be `http://localhost:8080/oauth2callback` or an endpoint on your Cloud Function.
        * Click "Create".
    3.  **Note down the Client ID and Client Secret.** The Client ID will likely be needed to configure Gemini tools in Vertex AI. The Client Secret should be stored securely (Secret Manager is an option if your Cloud Function needs it, but for Gemini "tool use," the flow might be more integrated).
    4.  **App Verification (for external apps):** If your application is "External" and uses sensitive/restricted scopes, you might need to submit it for verification by Google. For development and internal testing, this might not be immediately necessary.

### 7. Configuration of Gemini Tools in Vertex AI

* **Action:** Configure your Gemini model in Vertex AI to use the Google Calendar and Google Sheets tools.
* **Details:**
    1.  Access the [Vertex AI Studio in the GCP Console](https://console.cloud.google.com/vertex-ai/studio).
    2.  Select or create your Gemini model (e.g., Gemini Pro).
    3.  In the model configuration or when calling it via API from your Cloud Function, you will need to:
        * **Declare Tool Functions:** Provide the schema (name, description, input and output parameters) for each function Gemini can invoke (e.g., `Calendar`, `read_sheet_config`, `list_calendar_events`, etc., as defined in the technical specification).
        * **Configure Tool Authentication:** Specify how Gemini will authenticate to the Google Calendar/Sheets APIs. This will involve using the OAuth 2.0 Client ID you configured in the previous step, allowing Gemini to act on behalf of the professional user who granted consent. Refer to the latest Vertex AI documentation on "tool use" and authentication for tools accessing user data.
* **Important:** The exact way to configure this may vary with updates to the Gemini API and Vertex AI. Always consult the official Google Cloud documentation.

### 8. Testing and Verification

* **Action:** Exhaustively test all P1 flows.
* **Details:**
    1.  Test the professional's availability and cancellation policy setup.
    2.  Test the client's pre-booking flow, including the presentation of the cancellation policy.
    3.  Test the confirmation and rejection of appointments by the professional.
    4.  Verify that events in Google Calendar are created/updated/deleted correctly (titles, colors, attendees).
    5.  Verify that logs in Google Sheets are being written correctly.
    6.  Test agenda queries by the professional.
    7.  Check Cloud Logging for any errors and resolve them.
    8.  Confirm that voice and text interactions in Brazilian Portuguese work as expected.

By following these manual steps in conjunction with the infrastructure created by Terraform, you should be able to get your AgendAI P1 project functional. Remember to consult the official Google Cloud documentation for each service, as interfaces and features can evolve.