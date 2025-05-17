"""
Gemini API Service for AgendAI

This module provides functionality to interact with Google's Gemini API via Vertex AI.
It handles:
1. Setting up the Gemini client with proper authentication
2. Configuring tool definitions for Google Calendar and Google Sheets
3. Generating content with the Gemini model
4. Processing Gemini's responses, including tool calls

Author: Frederico Policarpo Martins Boaventura
Date: May 17, 2025
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional, Union, Tuple

# Google Cloud and Vertex AI imports
from google.cloud import aiplatform
from vertexai.preview.generative_models import GenerativeModel, Tool, FunctionDeclaration, Part
from vertexai.preview.generative_models import Content, ChatSession
from vertexai.generative_models import GenerationConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class GeminiService:
    """Service class for interacting with the Gemini API via Vertex AI."""
    
    def __init__(
        self,
        project_id: str,
        location: str = "us-central1",
        model_name: str = "gemini-1.5-pro",
        temperature: float = 0.2,
        max_output_tokens: int = 1024,
        top_p: float = 0.8,
        top_k: int = 40
    ):
        """
        Initialize the Gemini service.
        
        Args:
            project_id: Google Cloud project ID
            location: Google Cloud region
            model_name: Gemini model name to use
            temperature: Controls randomness in responses (0.0-1.0)
            max_output_tokens: Maximum number of tokens in the response
            top_p: Nucleus sampling parameter
            top_k: Top-k sampling parameter
        """
        self.project_id = project_id
        self.location = location
        self.model_name = model_name
        
        # Initialize Vertex AI with project and location
        aiplatform.init(project=project_id, location=location)
        
        # Generation parameters
        self.generation_config = GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            top_p=top_p,
            top_k=top_k
        )
        
        # Initialize the model
        self.model = GenerativeModel(model_name)
        
        # Tool definitions will be set up when needed
        self.tools = None
        self.chat_session = None
    
    def _define_calendar_tools(self) -> List[FunctionDeclaration]:
        """
        Define the Google Calendar tool functions for Gemini.
        
        Returns:
            List of FunctionDeclaration objects for Calendar operations
        """
        return [
            FunctionDeclaration(
                name="list_calendar_events",
                description="Lists events from a professional's Google Calendar within a specified date range",
                parameters={
                    "type": "object",
                    "properties": {
                        "professional_id": {
                            "type": "string",
                            "description": "ID of the professional whose calendar to access"
                        },
                        "start_date": {
                            "type": "string",
                            "description": "Start date in ISO format (YYYY-MM-DD)"
                        },
                        "end_date": {
                            "type": "string",
                            "description": "End date in ISO format (YYYY-MM-DD)"
                        },
                        "status_filter": {
                            "type": "string",
                            "description": "Optional filter for event status (confirmed, pending, all)",
                            "enum": ["confirmed", "pending", "all"]
                        }
                    },
                    "required": ["professional_id", "start_date", "end_date"]
                }
            ),
            FunctionDeclaration(
                name="get_calendar_free_busy",
                description="Gets free/busy information for a professional's calendar",
                parameters={
                    "type": "object",
                    "properties": {
                        "professional_id": {
                            "type": "string",
                            "description": "ID of the professional whose calendar to access"
                        },
                        "start_date": {
                            "type": "string",
                            "description": "Start date in ISO format (YYYY-MM-DD)"
                        },
                        "end_date": {
                            "type": "string",
                            "description": "End date in ISO format (YYYY-MM-DD)"
                        },
                        "time_zone": {
                            "type": "string",
                            "description": "Time zone for the query (e.g., 'America/Sao_Paulo')"
                        }
                    },
                    "required": ["professional_id", "start_date", "end_date"]
                }
            ),
            FunctionDeclaration(
                name="create_calendar_event",
                description="Creates a new event in a professional's Google Calendar",
                parameters={
                    "type": "object",
                    "properties": {
                        "professional_id": {
                            "type": "string",
                            "description": "ID of the professional whose calendar to access"
                        },
                        "summary": {
                            "type": "string",
                            "description": "Event title/summary"
                        },
                        "start_datetime": {
                            "type": "string",
                            "description": "Start date and time in ISO format (YYYY-MM-DDTHH:MM:SS)"
                        },
                        "end_datetime": {
                            "type": "string",
                            "description": "End date and time in ISO format (YYYY-MM-DDTHH:MM:SS)"
                        },
                        "client_email": {
                            "type": "string",
                            "description": "Email of the client to invite"
                        },
                        "description": {
                            "type": "string",
                            "description": "Event description"
                        },
                        "status": {
                            "type": "string",
                            "description": "Event status (pending or confirmed)",
                            "enum": ["pending", "confirmed"]
                        },
                        "color_id": {
                            "type": "string",
                            "description": "Google Calendar color ID (orange=6 for pending, green=10 for confirmed)"
                        }
                    },
                    "required": ["professional_id", "summary", "start_datetime", "end_datetime", "status"]
                }
            ),
            FunctionDeclaration(
                name="update_calendar_event",
                description="Updates an existing event in a professional's Google Calendar",
                parameters={
                    "type": "object",
                    "properties": {
                        "professional_id": {
                            "type": "string",
                            "description": "ID of the professional whose calendar to access"
                        },
                        "event_id": {
                            "type": "string",
                            "description": "ID of the event to update"
                        },
                        "summary": {
                            "type": "string",
                            "description": "Updated event title/summary"
                        },
                        "status": {
                            "type": "string",
                            "description": "Updated event status (pending or confirmed)",
                            "enum": ["pending", "confirmed"]
                        },
                        "color_id": {
                            "type": "string",
                            "description": "Updated Google Calendar color ID"
                        }
                    },
                    "required": ["professional_id", "event_id"]
                }
            ),
            FunctionDeclaration(
                name="delete_calendar_event",
                description="Deletes an event from a professional's Google Calendar",
                parameters={
                    "type": "object",
                    "properties": {
                        "professional_id": {
                            "type": "string",
                            "description": "ID of the professional whose calendar to access"
                        },
                        "event_id": {
                            "type": "string",
                            "description": "ID of the event to delete"
                        }
                    },
                    "required": ["professional_id", "event_id"]
                }
            )
        ]
    
    def _define_sheets_tools(self) -> List[FunctionDeclaration]:
        """
        Define the Google Sheets tool functions for Gemini.
        
        Returns:
            List of FunctionDeclaration objects for Sheets operations
        """
        return [
            FunctionDeclaration(
                name="read_sheet_config",
                description="Reads configuration data from a professional's Google Sheet",
                parameters={
                    "type": "object",
                    "properties": {
                        "professional_id": {
                            "type": "string",
                            "description": "ID of the professional whose sheet to access"
                        },
                        "sheet_id": {
                            "type": "string",
                            "description": "ID of the Google Sheet"
                        },
                        "config_type": {
                            "type": "string",
                            "description": "Type of configuration to read",
                            "enum": ["availability", "cancellation_policy", "service_types"]
                        }
                    },
                    "required": ["professional_id", "sheet_id", "config_type"]
                }
            ),
            FunctionDeclaration(
                name="update_sheet_config",
                description="Updates configuration data in a professional's Google Sheet",
                parameters={
                    "type": "object",
                    "properties": {
                        "professional_id": {
                            "type": "string",
                            "description": "ID of the professional whose sheet to access"
                        },
                        "sheet_id": {
                            "type": "string",
                            "description": "ID of the Google Sheet"
                        },
                        "config_type": {
                            "type": "string",
                            "description": "Type of configuration to update",
                            "enum": ["availability", "cancellation_policy", "service_types"]
                        },
                        "config_data": {
                            "type": "object",
                            "description": "Configuration data to write (structure depends on config_type)"
                        }
                    },
                    "required": ["professional_id", "sheet_id", "config_type", "config_data"]
                }
            ),
            FunctionDeclaration(
                name="log_booking_action",
                description="Logs a booking-related action in the booking log sheet",
                parameters={
                    "type": "object",
                    "properties": {
                        "professional_id": {
                            "type": "string",
                            "description": "ID of the professional"
                        },
                        "sheet_id": {
                            "type": "string",
                            "description": "ID of the Google Sheet for booking logs"
                        },
                        "client_name": {
                            "type": "string",
                            "description": "Name of the client"
                        },
                        "client_email": {
                            "type": "string",
                            "description": "Email of the client"
                        },
                        "service_type": {
                            "type": "string",
                            "description": "Type of service requested"
                        },
                        "datetime": {
                            "type": "string",
                            "description": "Date and time of the appointment in ISO format"
                        },
                        "action": {
                            "type": "string",
                            "description": "Action being logged",
                            "enum": ["pre_booking", "confirmed", "rejected", "canceled", "completed", "no_show"]
                        },
                        "event_id": {
                            "type": "string",
                            "description": "Google Calendar event ID (if applicable)"
                        },
                        "notes": {
                            "type": "string",
                            "description": "Additional notes or details"
                        }
                    },
                    "required": ["professional_id", "sheet_id", "client_name", "service_type", "datetime", "action"]
                }
            ),
            FunctionDeclaration(
                name="get_booking_stats",
                description="Retrieves booking statistics from the booking log sheet",
                parameters={
                    "type": "object",
                    "properties": {
                        "professional_id": {
                            "type": "string",
                            "description": "ID of the professional"
                        },
                        "sheet_id": {
                            "type": "string",
                            "description": "ID of the Google Sheet for booking logs"
                        },
                        "start_date": {
                            "type": "string",
                            "description": "Start date for the statistics period in ISO format (YYYY-MM-DD)"
                        },
                        "end_date": {
                            "type": "string",
                            "description": "End date for the statistics period in ISO format (YYYY-MM-DD)"
                        },
                        "stat_type": {
                            "type": "string",
                            "description": "Type of statistics to retrieve",
                            "enum": ["confirmed_count", "cancellation_rate", "no_show_rate", "cancellation_fees"]
                        }
                    },
                    "required": ["professional_id", "sheet_id", "start_date", "end_date", "stat_type"]
                }
            )
        ]
    
    def setup_tools(self) -> None:
        """Configure the tools that Gemini can use (Calendar and Sheets)."""
        calendar_functions = self._define_calendar_tools()
        sheets_functions = self._define_sheets_tools()
        
        # Combine all function declarations
        all_functions = calendar_functions + sheets_functions
        
        # Create Tool objects
        self.tools = [
            Tool(
                function_declarations=all_functions
            )
        ]
        
        logger.info(f"Configured {len(all_functions)} tool functions for Gemini")
    
    def create_chat_session(self) -> None:
        """Create a new chat session with the Gemini model."""
        if self.tools is None:
            self.setup_tools()
        
        self.chat_session = ChatSession(
            model=self.model,
            tools=self.tools
        )
        
        logger.info("Created new Gemini chat session")
    
    def generate_content(
        self, 
        prompt: str, 
        context: Optional[Dict[str, Any]] = None
    ) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Generate content using the Gemini model with the provided prompt and context.
        
        Args:
            prompt: The prompt to send to Gemini
            context: Optional additional context to include
        
        Returns:
            Tuple containing:
                - The text response from Gemini
                - A list of tool calls made by Gemini
        """
        if self.tools is None:
            self.setup_tools()
        
        # Prepare the prompt with context if provided
        prompt_with_context = prompt
        if context:
            context_str = json.dumps(context, ensure_ascii=False, indent=2)
            prompt_with_context = f"{prompt}\n\nContext:\n{context_str}"
        
        logger.info(f"Sending prompt to Gemini: {prompt[:100]}...")
        
        try:
            # Generate content with the model
            response = self.model.generate_content(
                prompt_with_context,
                generation_config=self.generation_config,
                tools=self.tools
            )
            
            # Extract text response
            text_response = response.text
            
            # Extract tool calls if any
            tool_calls = []
            if hasattr(response, 'candidates') and response.candidates:
                for candidate in response.candidates:
                    if hasattr(candidate, 'content') and candidate.content:
                        for part in candidate.content.parts:
                            if hasattr(part, 'function_call'):
                                tool_calls.append({
                                    'name': part.function_call.name,
                                    'args': part.function_call.args
                                })
            
            logger.info(f"Received response from Gemini with {len(tool_calls)} tool calls")
            
            return text_response, tool_calls
            
        except Exception as e:
            logger.error(f"Error generating content with Gemini: {str(e)}")
            raise
    
    def send_chat_message(
        self, 
        message: str, 
        context: Optional[Dict[str, Any]] = None
    ) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Send a message in an ongoing chat session with Gemini.
        
        Args:
            message: The message to send
            context: Optional additional context to include
        
        Returns:
            Tuple containing:
                - The text response from Gemini
                - A list of tool calls made by Gemini
        """
        if self.chat_session is None:
            self.create_chat_session()
        
        # Prepare the message with context if provided
        message_with_context = message
        if context:
            context_str = json.dumps(context, ensure_ascii=False, indent=2)
            message_with_context = f"{message}\n\nContext:\n{context_str}"
        
        logger.info(f"Sending chat message to Gemini: {message[:100]}...")
        
        try:
            # Send message to the chat session
            response = self.chat_session.send_message(
                message_with_context,
                generation_config=self.generation_config
            )
            
            # Extract text response
            text_response = response.text
            
            # Extract tool calls if any
            tool_calls = []
            if hasattr(response, 'candidates') and response.candidates:
                for candidate in response.candidates:
                    if hasattr(candidate, 'content') and candidate.content:
                        for part in candidate.content.parts:
                            if hasattr(part, 'function_call'):
                                tool_calls.append({
                                    'name': part.function_call.name,
                                    'args': part.function_call.args
                                })
            
            logger.info(f"Received chat response from Gemini with {len(tool_calls)} tool calls")
            
            return text_response, tool_calls
            
        except Exception as e:
            logger.error(f"Error sending chat message to Gemini: {str(e)}")
            raise
    
    def process_tool_response(
        self, 
        tool_name: str, 
        tool_response: Dict[str, Any]
    ) -> str:
        """
        Process a response from a tool call and send it back to Gemini.
        
        Args:
            tool_name: Name of the tool that was called
            tool_response: Response data from the tool execution
        
        Returns:
            Gemini's response after processing the tool result
        """
        if self.chat_session is None:
            raise ValueError("No active chat session. Call create_chat_session() first.")
        
        logger.info(f"Processing response from tool '{tool_name}'")
        
        try:
            # Create content with the tool response
            response_content = Content(
                parts=[
                    Part.from_function_response(
                        name=tool_name,
                        response=tool_response
                    )
                ]
            )
            
            # Send the tool response to Gemini
            gemini_response = self.chat_session.send_message(response_content)
            
            logger.info("Successfully processed tool response with Gemini")
            
            return gemini_response.text
            
        except Exception as e:
            logger.error(f"Error processing tool response with Gemini: {str(e)}")
            raise


# Example usage function
def example_usage():
    """Example of how to use the GeminiService class."""
    # Initialize the service
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    gemini_service = GeminiService(project_id=project_id)
    
    # Create a chat session
    gemini_service.create_chat_session()
    
    # Example prompt for client booking
    prompt = """
    O cliente João Silva deseja agendar uma consulta para a próxima semana, 
    preferencialmente na terça-feira pela manhã. Ele mencionou que é para uma 
    consulta inicial e seu email é joao.silva@example.com.
    
    Por favor, verifique a disponibilidade do profissional para terça-feira 
    da próxima semana pela manhã e sugira horários disponíveis.
    """
    
    # Context with professional information
    context = {
        "professional_id": "prof123",
        "professional_name": "Dra. Ana Oliveira",
        "sheet_id": "1abc123def456ghi789",
        "service_type": "Consulta Inicial",
        "duration_minutes": 60
    }
    
    # Send the message and get the response
    response_text, tool_calls = gemini_service.send_chat_message(prompt, context)
    
    print(f"Gemini Response: {response_text}")
    
    # Process tool calls if any
    if tool_calls:
        print(f"Tool calls made by Gemini: {json.dumps(tool_calls, indent=2)}")
        
        # Example of processing a tool call response
        # In a real application, you would execute the actual tool function
        # and get the real response data
        tool_name = tool_calls[0]['name']
        mock_tool_response = {
            "availableSlots": [
                {"start": "2025-05-24T09:00:00", "end": "2025-05-24T10:00:00"},
                {"start": "2025-05-24T10:30:00", "end": "2025-05-24T11:30:00"},
                {"start": "2025-05-24T11:30:00", "end": "2025-05-24T12:30:00"}
            ]
        }
        
        # Process the tool response
        final_response = gemini_service.process_tool_response(tool_name, mock_tool_response)
        print(f"Final response after tool execution: {final_response}")


if __name__ == "__main__":
    example_usage()
