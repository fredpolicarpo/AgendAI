# AgendAI: Intelligent Scheduling Assistant

## Project Description

AgendAI is an intelligent, chatbot-based virtual assistant designed to simplify and automate the appointment scheduling process for independent professionals and their clients. Leveraging **N8N** for workflow automation and **Gemini 1.5 Flash** (via Vertex AI) for natural language understanding, AgendAI interacts with users via Telegram, supporting both text and voice commands (in Brazilian Portuguese).

The solution integrates with the following technologies:
* **N8N Workflow Automation:** For orchestrating the entire process flow, managing Telegram bot interactions, and coordinating the AI agent.
* **N8N AI Agent Node:** Configured with Gemini 1.5 Flash (via Vertex AI) as its core intelligence engine, with Google Calendar and Google Sheets integrated as tools.
* **N8N STT Node:** For converting voice inputs (received via Telegram in pt-BR) into text for processing.
* **Telegram Bot API:** As the primary interface for both professionals and clients to interact with AgendAI.
* **Google Calendar API:** Accessed as a tool by Gemini (via the N8N AI Agent Node) to manage availability and appointments.
* **Google Sheets API:** Accessed as a tool by Gemini (via the N8N AI Agent Node) for logging interactions and storing professional configurations.

The main goal of AgendAI is to optimize professionals' time management, reduce no-shows through reminders and clear cancellation policies, and significantly improve the scheduling experience for clients.

## Features (P1: Essential MVP)

AgendAI supports the complete scheduling lifecycle:
1. Professional's initial availability setup
2. Professional's cancellation policy configuration
3. Client's pre-booking requests (with voice/text input)
4. Professional's confirmation/rejection of booking requests
5. Calendar updates and client notifications
6. Professional's simple agenda querying

All interactions support both text and voice input in Brazilian Portuguese (pt-BR).

## Required Tools

To set up, develop, and deploy AgendAI, you will need the following tools:

### 1. N8N Workflow Automation

N8N is the core platform used to build the workflow automation for AgendAI.

**Installation:**

We recommend following the [official N8N installation guide](https://docs.n8n.io/hosting/) for the most up-to-date instructions. Below are summaries for common installation methods:

* **Using NPM (Recommended for local development)**
    ```bash
    npm install n8n -g
    n8n start
    ```

* **Using Docker**
    ```bash
    docker run -it --rm \
      --name n8n \
      -p 5678:5678 \
      -v ~/.n8n:/home/node/.n8n \
      n8nio/n8n
    ```

* **Cloud Hosted (Production)**
    * Consider using N8N Cloud for production deployments: https://www.n8n.cloud/

### 2. Telegram Bot

* You will need a Telegram account to:
    1. Interact with `BotFather` to create your AgendAI bot and obtain the API token.
    2. Test your AgendAI bot as an end-user (client or professional).

## How to Set Up and Run the Project

1. **Create a Telegram Bot:**
   * Open Telegram and search for "BotFather"
   * Send the command `/newbot`
   * Follow the instructions to name your bot and get the API token

2. **Set Up N8N:**
   * Install N8N as described above
   * Access the N8N workflow editor (usually at http://localhost:5678)
   * Install the following nodes:
     * Telegram Trigger (for receiving messages)
     * Telegram Sender (for sending messages)
     * N8N AI Agent Node (for Gemini integration)
     * N8N STT Node (for voice processing)
   
3. **Configure N8N Nodes:**
   * Set up the Telegram Trigger node with your bot token
   * Configure the N8N AI Agent Node with:
     * Vertex AI credentials for Gemini 1.5 Flash 
     * Tool configurations for Google Calendar and Google Sheets
   * Configure the N8N STT Node for Brazilian Portuguese
   * Set up proper error handling and logging strategies

4. **Build the Workflows:**
   * Design the workflows based on the technical specification
   * Implement all P1 functionalities with proper branching and error handling

5. **Testing:**
   * Test all P1 functionalities with both text and voice inputs
   * Verify the complete scheduling lifecycle works as expected

## Project Documentation

* **Product Specification:** [Product Specification: AgendAI](docs/product_spec_en_us.md)
* **Technical Specification:** [Technical Specification: AgendAI - P1 (MVP) - N8N AI Agent Approach](docs/tech_spec_en_us.md)
* **Style Guide & Coding Conventions:** [Style Guide and Coding Conventions: AgendAI](docs/.windsurf/rules.md)

## Contributing

(Placeholder for contribution guidelines if the project is collaborative.)

## License

(Placeholder for the project license, e.g., MIT, Apache 2.0, etc.)
