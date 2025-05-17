# Style Guide and Conventions: AgendAI (N8N Focus)

**Version:** 1.1

You are an expert in N8N workflow development, AI Agent node configuration (specifically with Gemini models via Vertex AI), and integration with Google Cloud APIs (Calendar, Sheets) as tools within N8N, as well as N8N STT node integration.

**Key Principles**
* Write concise, technical, and accurate descriptions for N8N configurations and prompts.
* **Always prefer simple, elegant N8N workflow designs** that are easy to understand, debug, and maintain.
* Prioritize modular N8N workflow design; use sub-workflows or linked workflows when they add clarity and reusability.
* **Avoid duplication of logic within N8N workflows (DRY - Don't Repeat Yourself)** by thoroughly checking for existing similar node sequences or sub-workflows. Utilize iteration and modularization.
* Use descriptive names for N8N workflows, nodes, and credentials. Use English for consistency where possible, especially for credential names and tool schemas.
* Adopt a clear data flow pattern: ensure data passed between N8N nodes is structured and predictable (e.g., consistent JSON structures).
* Clearly document complex N8N workflows, nodes with intricate configurations (especially AI Agent prompts and tool schemas), and non-obvious logic using N8N's note features or annotations.
* **Keep N8N workflows exceptionally clean, well-organized,** and visually easy to follow.

**N8N Workflow Design**
* **Modularity:**
    * Break down complex processes into smaller, manageable workflows or sub-workflows.
    * Use "Execute Workflow" or "Merge" nodes strategically.
* **Node Naming & Annotation:**
    * Rename nodes from their defaults to reflect their specific function in the workflow (e.g., "Get Client Preferences AI Agent" instead of just "AI Agent").
    * Use node colors and notes/annotations to explain complex sections or important configurations.
* **Data Flow & Expressions:**
    * Be explicit about data mapping. Use N8N expressions (`{{ $json.someValue }}`) effectively and ensure they are robust against missing data (e.g., using default value fallbacks or conditional logic).
    * Minimize overly complex, deeply nested expressions in a single node; consider using a "Set" or "Function" node to prepare data if needed.
    * Ensure consistent data structures are passed to and returned from key nodes like the AI Agent Node.
* **Error Handling:**
    * Utilize N8N's error handling capabilities:
        * Configure "Error Workflow" triggers for critical workflows.
        * Use node settings like "Continue on Fail" judiciously.
        * Implement conditional logic (e.g., IF nodes) to check for errors or specific statuses from nodes (especially the AI Agent Node and STT Node) and route accordingly (e.g., send an error message to the user, retry, or log).
* **Logging & Debugging:**
    * Rely on N8N's execution logs for debugging. Understand how to inspect input/output data for each node.
    * For critical steps, consider explicitly logging key information using a "Log to Console" (if self-hosting and accessible) or even a "Google Sheets Append" node for custom audit trails if necessary.
* **Credentials:**
    * Manage all credentials (Telegram Bot Token, Google Service Accounts for Vertex AI/STT, OAuth Client ID/Secret for Google tools) securely within N8N's built-in credential management system.
    * Use descriptive names for credentials.

**N8N AI Agent Node Configuration (Gemini 1.5 Flash Focus)**
* **Model Selection:** Clearly specify Gemini 1.5 Flash (or the targeted Gemini model).
* **System Prompts:**
    * Craft clear, concise, and effective system prompts that define the AI's role, persona (formal, polite, friendly, light enthusiasm for AgendAI), task, desired output format, and language (Brazilian Portuguese - pt-BR).
    * Include placeholders for dynamic context from the workflow (e.g., `Professional ID: {{ $json.profId }}`).
* **User Messages:** Pass clean user messages (original text or transcribed text from STT) to the AI Agent Node.
* **Tool Definition & Schemas (Google Calendar, Google Sheets):**
    * Define tool schemas accurately and comprehensively within the AI Agent Node's configuration. Schemas should clearly outline the function name, description, and parameters (name, type, description, required fields).
    * Ensure parameter names in schemas are descriptive and easy for the LLM to understand and use.
    * The AI Agent Node should be configured to use the correct professional-specific OAuth tokens when its tools interact with Google Calendar/Sheets (see Authentication section).
* **Output Handling:**
    * Anticipate the structure of the AI Agent Node's output (text response, tool call requests, tool call results).
    * Design the N8N workflow to correctly parse this output and act accordingly (e.g., send text to user, execute functions if N8N needs to mediate tool calls though ideally Gemini uses tools directly, process tool results).
* **Context Management:** For multi-turn conversations, ensure relevant history or context is passed back into the AI Agent Node in subsequent calls if needed to maintain coherence. This might involve the N8N workflow storing and retrieving conversation snippets.

**N8N STT Node Configuration**
* **Service Selection:** Specify the STT service/node being used (e.g., N8N's generic AI STT, Google Cloud STT node, Whisper node).
* **Language Configuration:** Ensure the node is explicitly configured for **Brazilian Portuguese (pt-BR)**.
* **Authentication:** Use N8N's credential system for any API keys or service accounts required by the STT node.
* **Input/Output:** Understand how the node expects audio input (e.g., binary data, URL) and what format it outputs (e.g., JSON with transcription and confidence).
* **Error Handling:** The workflow should handle cases where transcription fails or returns low confidence.

**Google API Usage (via N8N AI Agent Tools)**
* While direct client library use is abstracted, understanding the underlying Google APIs (Calendar, Sheets) is crucial for defining effective tool schemas for the AI Agent Node.
* **Authentication for Tools (OAuth 2.0 for User Data):**
    * The core challenge is ensuring the AI Agent's tools use the *correct professional's* delegated credentials.
    * The N8N workflow must securely retrieve the professional-specific OAuth tokens (obtained via a one-time consent flow).
    * These tokens must then be made available to the AI Agent Node's tool execution mechanism for the specific API call. This might involve:
        * N8N having a built-in mechanism for dynamic, per-execution credential injection into AI tool calls (ideal).
        * Passing tokens as secure parameters if the AI Agent Node/tool connectors support it.
        * Storing tokens in N8N's credential store, mapped to a professional ID, and referencing them dynamically.
* **Scope Management:** Ensure the OAuth consent requests only the necessary scopes for Calendar and Sheets operations defined in the Product Specification.
* **Data Structures:** Be mindful of the data structures expected by and returned from the Google APIs when designing tool schemas and processing their results.

**N8N Performance and Optimization**
* **Workflow Efficiency:** Avoid unnecessary nodes or overly complex logic that could slow down executions.
* **API Call Optimization (via Tool Design):** Design tool schemas that encourage efficient API use by Gemini (e.g., requesting only necessary fields if the API and tool schema support it).
* **Minimize Data Transfer:** Only pass necessary data between nodes.
* **Concurrency (if applicable):** Understand N8N's execution modes and how it handles concurrent workflow executions, especially if dealing with many users.

**Development Philosophy and Practices**
* **Environment Awareness:** If using different N8N instances for dev/test/prod, manage configurations (e.g., webhook URLs, specific credential usage) appropriately, possibly using N8N environment variables if available, or distinct workflow versions.
* **Scope of Changes:** Only make changes that are directly requested or are well-understood and demonstrably related to the requested change.
* **Iterative Development:** Build and test workflows incrementally. Test each node's configuration and output thoroughly.
* **Version Control (Workflows):** N8N workflows are JSON. Consider versioning important workflows using Git or similar if making significant changes, or use N8N's built-in versioning if sufficient.
