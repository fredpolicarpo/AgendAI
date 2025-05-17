# Style Guide and Coding Conventions: AgendAI

**Version:** 1.0

You are an expert in Python, serverless development with Google Cloud Functions, conversation design with Dialogflow CX, and integration with Google Cloud APIs (Calendar, Sheets, Speech-to-Text, Gemini/Vertex AI).

**Key Principles**
* Write concise, technical, and accurate code and documentation.
* **Always prefer simple, elegant solutions** that are easy to understand and maintain.
* Prioritize functional and modular programming; use classes (such as Pydantic models or for encapsulating services) when they add clarity and organization.
* **Avoid code duplication (DRY - Don't Repeat Yourself)** by thoroughly checking for existing similar functionality within the codebase before writing new code. Utilize iteration and modularization (e.g., utility functions).
* Use descriptive variable and function names, preferably in English for consistency with libraries and APIs, utilizing auxiliary verbs where appropriate (e.g., `is_active`, `has_permission`, `Workspace_calendar_events`).
* Use `lowercase_with_underscores` for Python directory, file, and function names.
* Adopt the RORO (Receive an Object, Return an Object) pattern for Google Cloud Functions handling Dialogflow webhooks (JSON input, JSON output).
* Clearly document complex functions and business logic (docstrings, comments).
* **Keep the codebase exceptionally clean, well-organized,** and adhere to the defined file structure.

**Python (for Google Cloud Functions)**
* Use `def` for synchronous functions and `async def` for asynchronous operations (especially external/Google API calls).
* Utilize type hints for all function signatures and important variables.
* Prefer Pydantic models for input/output data validation (e.g., Dialogflow webhook payloads, API responses) over raw dictionaries.
* **File Structure (suggestion for Cloud Functions):**
    * `main.py` (Cloud Function entry point, with HTTP/event handlers)
    * `dialogflow_handler.py` (specific logic for processing and responding to Dialogflow webhooks)
    * `services/` (modules for interacting with external APIs, e.g., `calendar_service.py`, `sheets_service.py`, `llm_service.py`)
    * `models/` (Pydantic model definitions for payloads, configurations)
    * `utils/` (generic utility functions, e.g., `date_utils.py`, `validation_utils.py`)
    * `config.py` (for loading configurations and environment variables)
* Avoid unnecessarily nested `if/else` blocks; use "early returns" and "guard clauses."
* Keep functions small and focused on a single responsibility.
* **Aim to keep Python files concise, ideally not exceeding 200-300 lines.** Refactor larger files into smaller, focused modules or functions.

**Google Cloud Functions Specific**
* Each Cloud Function should have a clear purpose (e.g., `handle_dialogflow_webhook`, `process_stt_result`).
* Robustly handle HTTP requests (especially from Dialogflow webhooks), validating the expected payload.
* Utilize environment variables provided by Google Cloud Functions for storing API keys, project IDs, and other sensitive or environment-specific configurations. Use a `config.py` module to load and manage these variables within the application code.
* Implement structured logging using the `google-cloud-logging` library for easier debugging and monitoring in Google Cloud.
* Return appropriate HTTP responses to Dialogflow (e.g., `200 OK` with a JSON payload for fulfillment, or specific HTTP errors if processing fails critically).

**Dialogflow CX Specific (Principles for Design and Fulfillment)**
* **Clear Naming:** Use descriptive and consistent names for Intents, Entities, Pages, Flows, Transition Routes, and Parameters.
* **Modularity:** Design modular and reusable conversational flows.
* **Parameters:** Utilize parameters to collect and pass information between conversation states and to webhooks.
* **Webhook Fulfillment:** For complex business logic, integration with external APIs, or generative AI, use webhooks.
    * Webhook request and response JSON payloads should be well-defined and validated (Pydantic can assist on the Cloud Function side).
* **Flow Control:** Effectively use conditions, routes, and event handlers within Dialogflow CX to guide the conversation.
* **Dialog Error Handling:** Define routes to gracefully handle "no-match" and other errors, guiding the user.

**Google API Usage (Calendar, Sheets, Speech-to-Text, Gemini/Vertex AI)**
* Utilize the official Google Cloud client libraries for Python (e.g., `google-api-python-client`, `google-cloud-aiplatform`, `google-cloud-speech`).
* Implement asynchronous calls (`async/await`) for these APIs whenever possible to avoid blocking Cloud Function execution, especially for I/O-bound operations.
* Correctly configure authentication and authorization (OAuth 2.0 for user data like Calendar/Sheets, API Keys/Service Accounts for APIs like STT/Vertex AI, as appropriate).
* Implement robust error handling for API calls, including retries (with exponential backoff) for transient errors and specific parsing of API error codes.
* Optimize API calls (e.g., use field masks to request only necessary data, consider batch operations when supported and appropriate).

**Error Handling and Validation (in Cloud Functions)**
* Prioritize error handling and edge cases:
    * Validate incoming payloads (e.g., from Dialogflow) at the beginning of the function.
    * Use "early returns" for error conditions to avoid excessive nesting.
    * The "happy path" should be the main and final part of the function's logic.
    * Utilize `try-except` blocks granularly to isolate operations that might fail (e.g., API calls, data manipulation).
    * Log errors in detail.
    * Return structured and helpful error messages to Dialogflow (which can then decide how to present them to the user or trigger an error flow).

**Dependencies (Suggestions for `requirements.txt` for Cloud Functions)**
* `functions-framework` (for local development and deployment to Google Cloud Functions)
* `google-api-python-client`
* `google-auth-oauthlib`
* `google-cloud-logging`
* `google-cloud-speech`
* `google-cloud-aiplatform` (or `google-generativeai` for Gemini API directly)
* `google-cloud-firestore` (if using Firestore for configurations)
* `pydantic` (for data validation and serialization)
* `python-dateutil` (for advanced date/time manipulation, if needed)
* `pytz` (for robustly handling timezones)

**Performance Optimization (for Cloud Functions)**
* Minimize the impact of "cold starts" by keeping dependencies and the function's code size optimized.
* Utilize asynchronous operations for all I/O-bound calls (APIs, database if any).
* Consider caching strategies for frequently accessed, non-sensitive data that doesn't change constantly (e.g., using Google Cloud Functions' Cache or Redis/Memorystore if complexity warrants it), but be careful not to serve stale data (GCalendar is the source of truth for the schedule).

**Development Philosophy and Practices**
* **Environment Awareness:** Write code that gracefully handles differences between environments (dev, test, prod), primarily through configuration management (see Google Cloud Functions Specific).
* **Scope of Changes:** Only make changes that are directly requested or are well-understood and demonstrably related to the requested change. Discuss broader refactoring efforts separately.
*