"""
Main Cloud Function for AgendAI

This is the main entry point for the Google Cloud Function that handles
webhook requests from Dialogflow CX, interacts with the Gemini API,
and orchestrates the scheduling workflow.

Author: Frederico Policarpo Martins Boaventura
Date: May 17, 2025
"""

import os
import json
import logging
import functions_framework
from flask import Request, jsonify
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple

# Import the Gemini service
from gemini_service import GeminiService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize the Gemini service
project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
gemini_service = GeminiService(project_id=project_id)

@functions_framework.http
def handle_dialogflow_webhook(request: Request) -> Dict[str, Any]:
    """
    Main entry point for the Cloud Function that handles Dialogflow CX webhook requests.
    
    Args:
        request: HTTP request from Dialogflow CX
        
    Returns:
        JSON response to be sent back to Dialogflow CX
    """
    try:
        # Parse the request JSON
        request_json = request.get_json(silent=True)
        
        if not request_json:
            logger.error("No JSON data received in request")
            return jsonify({"error": "No JSON data received"})
        
        logger.info(f"Received webhook request: {json.dumps(request_json, ensure_ascii=False)[:200]}...")
        
        # Extract the session ID
        session_id = request_json.get("sessionInfo", {}).get("session", "")
        
        # Extract the intent from the request
        intent = request_json.get("intentInfo", {}).get("displayName", "")
        
        # Extract parameters from the request
        parameters = request_json.get("sessionInfo", {}).get("parameters", {})
        
        # Get the language code (should be pt-BR)
        language_code = request_json.get("languageCode", "pt-br")
        
        # Process the request based on the intent
        response_data = process_intent(intent, parameters, session_id, language_code)
        
        # Return the response
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Error processing webhook request: {str(e)}", exc_info=True)
        
        # Return a generic error response
        return jsonify({
            "fulfillmentResponse": {
                "messages": [
                    {
                        "text": {
                            "text": [
                                "Desculpe, ocorreu um erro ao processar sua solicitação. Por favor, tente novamente mais tarde."
                            ]
                        }
                    }
                ]
            }
        })

def process_intent(
    intent: str, 
    parameters: Dict[str, Any], 
    session_id: str,
    language_code: str
) -> Dict[str, Any]:
    """
    Process the intent and generate a response using the Gemini API.
    
    Args:
        intent: The name of the intent from Dialogflow CX
        parameters: Parameters extracted from the user's request
        session_id: The session ID from Dialogflow CX
        language_code: The language code (e.g., pt-br)
        
    Returns:
        Response data to be sent back to Dialogflow CX
    """
    logger.info(f"Processing intent: {intent}")
    
    # Extract professional ID from session (in a real app, this would be stored in a database or session store)
    # For this example, we'll use a placeholder or extract from parameters if available
    professional_id = parameters.get("professional_id", "prof123")
    
    # Prepare the context for Gemini
    context = {
        "professional_id": professional_id,
        "intent": intent,
        "parameters": parameters,
        "session_id": session_id,
        "language_code": language_code,
        "timestamp": datetime.now().isoformat()
    }
    
    # Handle different intents
    if intent == "configurar_disponibilidade":
        return handle_availability_setup(parameters, context)
    elif intent == "configurar_politica_cancelamento":
        return handle_cancellation_policy_setup(parameters, context)
    elif intent == "solicitar_agendamento":
        return handle_booking_request(parameters, context)
    elif intent == "selecionar_horario_especifico":
        return handle_specific_time_selection(parameters, context)
    elif intent == "gerenciar_pedido_pendente":
        return handle_pending_request_management(parameters, context)
    elif intent == "consultar_agenda":
        return handle_agenda_query(parameters, context)
    elif intent == "solicitar_cancelamento":
        return handle_cancellation_request(parameters, context)
    else:
        # For unhandled intents, use Gemini to generate a generic response
        prompt = f"""
        O usuário acionou a intent "{intent}" com os seguintes parâmetros:
        {json.dumps(parameters, ensure_ascii=False, indent=2)}
        
        Por favor, gere uma resposta apropriada em português brasileiro (pt-BR).
        """
        
        # Create a new chat session for this interaction
        gemini_service.create_chat_session()
        
        # Send the prompt to Gemini
        response_text, tool_calls = gemini_service.send_chat_message(prompt, context)
        
        # Process any tool calls if needed
        if tool_calls:
            # In a real application, you would execute the actual tool functions
            # and process the responses
            logger.info(f"Gemini made {len(tool_calls)} tool calls")
            
            # For this example, we'll just log the tool calls
            for tool_call in tool_calls:
                logger.info(f"Tool call: {tool_call['name']} with args: {tool_call['args']}")
        
        # Return the response to Dialogflow
        return {
            "fulfillmentResponse": {
                "messages": [
                    {
                        "text": {
                            "text": [response_text]
                        }
                    }
                ]
            }
        }

def handle_availability_setup(
    parameters: Dict[str, Any], 
    context: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Handle the availability setup intent.
    
    Args:
        parameters: Parameters from Dialogflow CX
        context: Context information
        
    Returns:
        Response for Dialogflow CX
    """
    # Extract availability parameters
    dias_semana = parameters.get("dias_semana", [])
    horario_inicio = parameters.get("horario_inicio", "")
    horario_fim = parameters.get("horario_fim", "")
    
    # Prepare the prompt for Gemini
    prompt = f"""
    O profissional deseja configurar sua disponibilidade com os seguintes parâmetros:
    - Dias da semana: {', '.join(dias_semana)}
    - Horário de início: {horario_inicio}
    - Horário de fim: {horario_fim}
    
    Por favor, configure esta disponibilidade no Google Calendar do profissional
    e atualize a configuração no Google Sheets. Em seguida, gere uma resposta
    de confirmação em português brasileiro (pt-BR).
    """
    
    # Create a new chat session for this interaction
    gemini_service.create_chat_session()
    
    # Send the prompt to Gemini
    response_text, tool_calls = gemini_service.send_chat_message(prompt, context)
    
    # Process tool calls if any
    final_response = process_tool_calls(tool_calls, response_text)
    
    # Return the response to Dialogflow
    return {
        "fulfillmentResponse": {
            "messages": [
                {
                    "text": {
                        "text": [final_response]
                    }
                }
            ]
        }
    }

def handle_cancellation_policy_setup(
    parameters: Dict[str, Any], 
    context: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Handle the cancellation policy setup intent.
    
    Args:
        parameters: Parameters from Dialogflow CX
        context: Context information
        
    Returns:
        Response for Dialogflow CX
    """
    # Extract cancellation policy parameters
    limite_cancelamento_horas = parameters.get("limite_cancelamento_horas", 0)
    taxa_cancelamento_valor = parameters.get("taxa_cancelamento_valor", 0)
    
    # Prepare the prompt for Gemini
    prompt = f"""
    O profissional deseja configurar sua política de cancelamento com os seguintes parâmetros:
    - Limite de horas para cancelamento gratuito: {limite_cancelamento_horas} horas
    - Taxa de cancelamento (se fora do prazo): R$ {taxa_cancelamento_valor}
    
    Por favor, atualize esta política de cancelamento no Google Sheets do profissional.
    Em seguida, gere uma resposta de confirmação em português brasileiro (pt-BR).
    """
    
    # Create a new chat session for this interaction
    gemini_service.create_chat_session()
    
    # Send the prompt to Gemini
    response_text, tool_calls = gemini_service.send_chat_message(prompt, context)
    
    # Process tool calls if any
    final_response = process_tool_calls(tool_calls, response_text)
    
    # Return the response to Dialogflow
    return {
        "fulfillmentResponse": {
            "messages": [
                {
                    "text": {
                        "text": [final_response]
                    }
                }
            ]
        }
    }

def handle_booking_request(
    parameters: Dict[str, Any], 
    context: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Handle the booking request intent from a client.
    
    Args:
        parameters: Parameters from Dialogflow CX
        context: Context information
        
    Returns:
        Response for Dialogflow CX
    """
    # Extract booking request parameters
    cliente_nome = parameters.get("cliente_nome", "")
    cliente_email = parameters.get("cliente_email", "")
    servico_tipo = parameters.get("servico_tipo", "")
    preferencia_data = parameters.get("preferencia_data", "")
    preferencia_periodo = parameters.get("preferencia_periodo", "")
    
    # Prepare the prompt for Gemini
    prompt = f"""
    Um cliente deseja agendar um serviço com os seguintes detalhes:
    - Nome do cliente: {cliente_nome}
    - Email do cliente: {cliente_email}
    - Tipo de serviço: {servico_tipo}
    - Preferência de data: {preferencia_data}
    - Preferência de período: {preferencia_periodo}
    
    Por favor, verifique a disponibilidade do profissional para esta preferência
    e sugira horários específicos disponíveis. A resposta deve ser em português
    brasileiro (pt-BR).
    """
    
    # Create a new chat session for this interaction
    gemini_service.create_chat_session()
    
    # Send the prompt to Gemini
    response_text, tool_calls = gemini_service.send_chat_message(prompt, context)
    
    # Process tool calls if any
    final_response = process_tool_calls(tool_calls, response_text)
    
    # Return the response to Dialogflow
    return {
        "fulfillmentResponse": {
            "messages": [
                {
                    "text": {
                        "text": [final_response]
                    }
                }
            ]
        }
    }

def handle_specific_time_selection(
    parameters: Dict[str, Any], 
    context: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Handle the specific time selection intent from a client.
    
    Args:
        parameters: Parameters from Dialogflow CX
        context: Context information
        
    Returns:
        Response for Dialogflow CX
    """
    # Extract time selection parameters
    horario_escolhido = parameters.get("horario_escolhido", "")
    data_escolhida = parameters.get("data_escolhida", "")
    cliente_nome = parameters.get("cliente_nome", "")
    cliente_email = parameters.get("cliente_email", "")
    servico_tipo = parameters.get("servico_tipo", "")
    
    # Prepare the prompt for Gemini
    prompt = f"""
    O cliente selecionou um horário específico para agendamento:
    - Nome do cliente: {cliente_nome}
    - Email do cliente: {cliente_email}
    - Tipo de serviço: {servico_tipo}
    - Data escolhida: {data_escolhida}
    - Horário escolhido: {horario_escolhido}
    
    Por favor, crie um evento pendente no Google Calendar do profissional com
    status "Pendente" e cor laranja (color_id=6). Também registre este pré-agendamento
    no Google Sheets. Em seguida, gere uma mensagem de confirmação do pré-agendamento
    para o cliente em português brasileiro (pt-BR), informando que o profissional
    precisa confirmar o agendamento.
    """
    
    # Create a new chat session for this interaction
    gemini_service.create_chat_session()
    
    # Send the prompt to Gemini
    response_text, tool_calls = gemini_service.send_chat_message(prompt, context)
    
    # Process tool calls if any
    final_response = process_tool_calls(tool_calls, response_text)
    
    # Return the response to Dialogflow
    return {
        "fulfillmentResponse": {
            "messages": [
                {
                    "text": {
                        "text": [final_response]
                    }
                }
            ]
        }
    }

def handle_pending_request_management(
    parameters: Dict[str, Any], 
    context: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Handle the pending request management intent from a professional.
    
    Args:
        parameters: Parameters from Dialogflow CX
        context: Context information
        
    Returns:
        Response for Dialogflow CX
    """
    # Extract management parameters
    event_id = parameters.get("event_id", "")
    action = parameters.get("action", "")  # 'confirm' or 'reject'
    
    # Prepare the prompt for Gemini
    prompt = f"""
    O profissional deseja {action} (confirmar ou rejeitar) o agendamento pendente com ID {event_id}.
    
    Se a ação for 'confirm':
    - Atualize o evento no Google Calendar para status "Confirmado" e cor verde (color_id=10)
    - Atualize o registro no Google Sheets
    - Gere uma mensagem de notificação para o cliente em português brasileiro (pt-BR)
    
    Se a ação for 'reject':
    - Exclua o evento do Google Calendar
    - Atualize o registro no Google Sheets como "Rejeitado"
    - Gere uma mensagem de notificação para o cliente em português brasileiro (pt-BR)
    """
    
    # Create a new chat session for this interaction
    gemini_service.create_chat_session()
    
    # Send the prompt to Gemini
    response_text, tool_calls = gemini_service.send_chat_message(prompt, context)
    
    # Process tool calls if any
    final_response = process_tool_calls(tool_calls, response_text)
    
    # Return the response to Dialogflow
    return {
        "fulfillmentResponse": {
            "messages": [
                {
                    "text": {
                        "text": [final_response]
                    }
                }
            ]
        }
    }

def handle_agenda_query(
    parameters: Dict[str, Any], 
    context: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Handle the agenda query intent from a professional.
    
    Args:
        parameters: Parameters from Dialogflow CX
        context: Context information
        
    Returns:
        Response for Dialogflow CX
    """
    # Extract query parameters
    data_consulta = parameters.get("data_consulta", "")
    
    # If no specific date is provided, default to today
    if not data_consulta:
        data_consulta = datetime.now().strftime("%Y-%m-%d")
    
    # Prepare the prompt for Gemini
    prompt = f"""
    O profissional deseja consultar sua agenda para a data: {data_consulta}.
    
    Por favor, liste todos os compromissos (confirmados e pendentes) para esta data,
    obtendo as informações do Google Calendar. A resposta deve ser em português
    brasileiro (pt-BR) e deve incluir o horário, status (confirmado/pendente) e
    nome do cliente para cada compromisso.
    """
    
    # Create a new chat session for this interaction
    gemini_service.create_chat_session()
    
    # Send the prompt to Gemini
    response_text, tool_calls = gemini_service.send_chat_message(prompt, context)
    
    # Process tool calls if any
    final_response = process_tool_calls(tool_calls, response_text)
    
    # Return the response to Dialogflow
    return {
        "fulfillmentResponse": {
            "messages": [
                {
                    "text": {
                        "text": [final_response]
                    }
                }
            ]
        }
    }

def handle_cancellation_request(
    parameters: Dict[str, Any], 
    context: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Handle the cancellation request intent from a client.
    
    Args:
        parameters: Parameters from Dialogflow CX
        context: Context information
        
    Returns:
        Response for Dialogflow CX
    """
    # Extract cancellation parameters
    event_id = parameters.get("event_id", "")
    cliente_nome = parameters.get("cliente_nome", "")
    
    # Prepare the prompt for Gemini
    prompt = f"""
    O cliente {cliente_nome} deseja cancelar o agendamento com ID {event_id}.
    
    Por favor, verifique a política de cancelamento do profissional e determine
    se há alguma taxa aplicável com base no tempo restante até o agendamento.
    
    Em seguida, informe ao cliente sobre a política e pergunte se deseja prosseguir
    com o cancelamento. A resposta deve ser em português brasileiro (pt-BR).
    """
    
    # Create a new chat session for this interaction
    gemini_service.create_chat_session()
    
    # Send the prompt to Gemini
    response_text, tool_calls = gemini_service.send_chat_message(prompt, context)
    
    # Process tool calls if any
    final_response = process_tool_calls(tool_calls, response_text)
    
    # Return the response to Dialogflow
    return {
        "fulfillmentResponse": {
            "messages": [
                {
                    "text": {
                        "text": [final_response]
                    }
                }
            ]
        }
    }

def process_tool_calls(
    tool_calls: List[Dict[str, Any]], 
    default_response: str
) -> str:
    """
    Process tool calls made by Gemini.
    
    In a real application, this would execute the actual tool functions
    and process the responses. For this example, we'll simulate the process.
    
    Args:
        tool_calls: List of tool calls made by Gemini
        default_response: Default response to use if no tool calls were made
        
    Returns:
        Final response text after processing tool calls
    """
    if not tool_calls:
        return default_response
    
    logger.info(f"Processing {len(tool_calls)} tool calls")
    
    # For this example, we'll simulate tool execution
    # In a real application, you would execute the actual tool functions
    
    # Process each tool call
    for i, tool_call in enumerate(tool_calls):
        tool_name = tool_call.get("name", "")
        tool_args = tool_call.get("args", {})
        
        logger.info(f"Processing tool call {i+1}/{len(tool_calls)}: {tool_name}")
        
        # Simulate tool execution and response
        # In a real application, you would call the actual API
        mock_response = simulate_tool_execution(tool_name, tool_args)
        
        # Send the tool response back to Gemini
        if i == len(tool_calls) - 1:  # If this is the last tool call
            # Process the final tool response
            final_response = gemini_service.process_tool_response(tool_name, mock_response)
            return final_response
        else:
            # Process intermediate tool response
            gemini_service.process_tool_response(tool_name, mock_response)
    
    # If we reach here, something went wrong
    return default_response

def simulate_tool_execution(
    tool_name: str, 
    tool_args: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Simulate the execution of a tool function.
    
    In a real application, this would call the actual API (Google Calendar, Google Sheets).
    For this example, we'll return mock responses.
    
    Args:
        tool_name: Name of the tool function
        tool_args: Arguments for the tool function
        
    Returns:
        Mock response from the tool
    """
    logger.info(f"Simulating execution of tool: {tool_name} with args: {tool_args}")
    
    # Mock responses for different tool functions
    if tool_name == "list_calendar_events":
        # Mock response for listing calendar events
        return {
            "events": [
                {
                    "id": "event123",
                    "summary": "[Confirmado] - Consulta Inicial",
                    "start": "2025-05-24T09:00:00",
                    "end": "2025-05-24T10:00:00",
                    "status": "confirmed",
                    "attendees": [{"email": "cliente@example.com", "displayName": "Cliente A"}]
                },
                {
                    "id": "event456",
                    "summary": "[Pendente] - Reunião",
                    "start": "2025-05-24T14:00:00",
                    "end": "2025-05-24T15:00:00",
                    "status": "tentative",
                    "attendees": [{"email": "cliente@example.com", "displayName": "Cliente B"}]
                }
            ]
        }
    elif tool_name == "get_calendar_free_busy":
        # Mock response for free/busy information
        return {
            "timeMin": "2025-05-24T00:00:00",
            "timeMax": "2025-05-24T23:59:59",
            "busy": [
                {"start": "2025-05-24T09:00:00", "end": "2025-05-24T10:00:00"},
                {"start": "2025-05-24T14:00:00", "end": "2025-05-24T15:00:00"}
            ],
            "free": [
                {"start": "2025-05-24T10:30:00", "end": "2025-05-24T12:30:00"},
                {"start": "2025-05-24T15:30:00", "end": "2025-05-24T17:30:00"}
            ]
        }
    elif tool_name == "create_calendar_event":
        # Mock response for creating a calendar event
        return {
            "id": "new_event_789",
            "summary": tool_args.get("summary", ""),
            "start": tool_args.get("start_datetime", ""),
            "end": tool_args.get("end_datetime", ""),
            "status": tool_args.get("status", ""),
            "created": datetime.now().isoformat()
        }
    elif tool_name == "update_calendar_event":
        # Mock response for updating a calendar event
        return {
            "id": tool_args.get("event_id", ""),
            "summary": tool_args.get("summary", ""),
            "status": tool_args.get("status", ""),
            "updated": datetime.now().isoformat()
        }
    elif tool_name == "delete_calendar_event":
        # Mock response for deleting a calendar event
        return {
            "id": tool_args.get("event_id", ""),
            "deleted": True
        }
    elif tool_name == "read_sheet_config":
        # Mock response for reading sheet configuration
        config_type = tool_args.get("config_type", "")
        
        if config_type == "availability":
            return {
                "availability": [
                    {"day": "Monday", "start": "09:00", "end": "17:00"},
                    {"day": "Tuesday", "start": "09:00", "end": "17:00"},
                    {"day": "Wednesday", "start": "09:00", "end": "17:00"},
                    {"day": "Thursday", "start": "09:00", "end": "17:00"},
                    {"day": "Friday", "start": "09:00", "end": "17:00"}
                ]
            }
        elif config_type == "cancellation_policy":
            return {
                "cancellation_policy": {
                    "free_cancellation_hours": 24,
                    "cancellation_fee": 50.0
                }
            }
        elif config_type == "service_types":
            return {
                "service_types": [
                    {"name": "Consulta Inicial", "duration": 60, "price": 200.0},
                    {"name": "Consulta de Retorno", "duration": 30, "price": 150.0},
                    {"name": "Reunião", "duration": 60, "price": 180.0}
                ]
            }
    elif tool_name == "update_sheet_config":
        # Mock response for updating sheet configuration
        return {
            "updated": True,
            "config_type": tool_args.get("config_type", ""),
            "timestamp": datetime.now().isoformat()
        }
    elif tool_name == "log_booking_action":
        # Mock response for logging a booking action
        return {
            "logged": True,
            "action": tool_args.get("action", ""),
            "timestamp": datetime.now().isoformat()
        }
    elif tool_name == "get_booking_stats":
        # Mock response for getting booking statistics
        stat_type = tool_args.get("stat_type", "")
        
        if stat_type == "confirmed_count":
            return {"count": 15}
        elif stat_type == "cancellation_rate":
            return {"rate": 0.12}
        elif stat_type == "no_show_rate":
            return {"rate": 0.05}
        elif stat_type == "cancellation_fees":
            return {"total_fees": 150.0}
    
    # Default response for unknown tools
    return {"error": "Unknown tool", "tool_name": tool_name}

if __name__ == "__main__":
    # This is used when running locally only
    # When deployed to Google Cloud Functions, the function will be triggered by HTTP requests
    pass
