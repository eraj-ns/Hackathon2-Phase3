"""AI Chat Agent for the AI Chat Agent & Conversation System."""

import os
from typing import Dict, Any, List, Optional
from uuid import UUID

from openai import OpenAI

from ..models.intent import Intent, IntentType, IntentRecognitionResult
from ..models.message import Message


class AIChatAgent:
    """AI agent that processes natural language input and generates responses."""

    def __init__(self):
        """Initialize the AI Chat Agent with OpenAI client."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")

        # Initialize the OpenAI client
        # Handle potential proxy-related initialization issues in newer OpenAI versions
        # Unset proxy-related environment variables that might interfere with OpenAI client
        original_http_proxy = os.environ.pop('HTTP_PROXY', None)
        original_https_proxy = os.environ.pop('HTTPS_PROXY', None)

        try:
            self.client = OpenAI(api_key=api_key)
        except TypeError as e:
            if "'proxies'" in str(e):
                # If there's a proxies-related error, initialize without problematic parameters
                self.client = OpenAI(api_key=api_key)
            else:
                raise
        finally:
            # Restore original proxy settings if they existed
            if original_http_proxy is not None:
                os.environ['HTTP_PROXY'] = original_http_proxy
            if original_https_proxy is not None:
                os.environ['HTTPS_PROXY'] = original_https_proxy

        # System prompt that guides the AI's behavior
        self.system_prompt = """
        You are an AI assistant that helps users manage their tasks through natural language.
        Your job is to understand the user's intent from their message and respond appropriately.
        You should:
        1. Identify if the user wants to create, view, update, delete, or mark tasks as complete/incomplete
        2. Extract relevant information like task titles, dates, priorities, etc.
        3. Respond with helpful and clear messages
        4. Remember that you cannot directly access the database - you must communicate intent to the system

        Common intents:
        - create_task: When user wants to add a new task
        - view_tasks: When user wants to see their tasks
        - update_task: When user wants to modify a task
        - delete_task: When user wants to remove a task
        - mark_complete: When user wants to mark a task as complete
        - mark_incomplete: When user wants to mark a task as incomplete
        """

    def process_user_message(
        self,
        user_message: str,
        conversation_history: Optional[List[Message]] = None
    ) -> Dict[str, Any]:
        """
        Process a user message and return an AI response along with intent information.

        Args:
            user_message: The natural language message from the user
            conversation_history: Previous messages in the conversation (for context)

        Returns:
            Dictionary containing the AI response, intent, and confidence
        """
        # Prepare the messages for the OpenAI API
        messages = [{"role": "system", "content": self.system_prompt}]

        # Add conversation history if available
        if conversation_history:
            for msg in conversation_history:
                role = msg.role
                if role == "user":
                    messages.append({"role": "user", "content": msg.content})
                elif role == "assistant":
                    messages.append({"role": "assistant", "content": msg.content})
                # We don't include tool messages in the conversation context for the AI

        # Add the current user message
        messages.append({"role": "user", "content": user_message})

        try:
            # Call the OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )

            # Extract the AI response
            ai_response = response.choices[0].message.content

            # Identify the intent from the user's message
            intent_result = self._identify_intent(user_message)

            return {
                "response": ai_response,
                "intent": intent_result,
                "success": True
            }

        except Exception as e:
            # Handle any errors from the OpenAI API
            import logging
            logging.error(f"Error in AIChatAgent.process_user_message: {str(e)}")
            return {
                "response": "I'm sorry, I encountered an error processing your request. Please try again.",
                "intent": Intent(
                    type=IntentType.UNKNOWN,
                    confidence=0.0,
                    parameters={},
                    extracted_entities=[]
                ),
                "success": False,
                "error": str(e)
            }

    def _identify_intent(self, user_message: str) -> IntentRecognitionResult:
        """
        Identify the intent from a user message using simple keyword matching.
        In a real implementation, this would use more sophisticated NLP techniques
        or leverage the OpenAI API to classify intent.
        """
        message_lower = user_message.lower()

        # Simple keyword-based intent detection with confidence scores
        confidence = 0.3  # Default low confidence
        intent_type = IntentType.UNKNOWN

        # Calculate confidence based on keyword matches
        keyword_matches = []

        if any(keyword in message_lower for keyword in ["add", "create", "new", "make", "task to"]):
            intent_type = IntentType.CREATE_TASK
            keyword_matches.extend(["add", "create", "new", "make", "task to"])
            confidence = 0.8

        if any(keyword in message_lower for keyword in ["view", "show", "see", "list", "display", "my tasks"]):
            intent_type = IntentType.VIEW_TASKS
            keyword_matches.extend(["view", "show", "see", "list", "display", "my tasks"])
            confidence = max(confidence, 0.8)

        if any(keyword in message_lower for keyword in ["update", "change", "modify", "edit"]):
            intent_type = IntentType.UPDATE_TASK
            keyword_matches.extend(["update", "change", "modify", "edit"])
            confidence = max(confidence, 0.8)

        if any(keyword in message_lower for keyword in ["delete", "remove", "cancel"]):
            intent_type = IntentType.DELETE_TASK
            keyword_matches.extend(["delete", "remove", "cancel"])
            confidence = max(confidence, 0.8)

        if any(keyword in message_lower for keyword in ["complete", "done", "finish", "completed"]):
            intent_type = IntentType.MARK_COMPLETE
            keyword_matches.extend(["complete", "done", "finish", "completed"])
            confidence = max(confidence, 0.8)

        if any(keyword in message_lower for keyword in ["incomplete", "not done", "undo", "reopen"]):
            intent_type = IntentType.MARK_INCOMPLETE
            keyword_matches.extend(["incomplete", "not done", "undo", "reopen"])
            confidence = max(confidence, 0.8)

        # If still unknown, check for general conversation patterns
        if intent_type == IntentType.UNKNOWN:
            if any(keyword in message_lower for keyword in ["hello", "hi", "hey", "greetings", "help"]):
                confidence = 0.6  # Medium confidence for greeting/help intent (mapped to unknown for now)
            elif "?" in user_message or any(keyword in message_lower for keyword in ["what", "how", "when", "where", "why"]):
                confidence = 0.5  # Medium confidence for question intent (mapped to unknown for now)
            else:
                confidence = 0.3  # Low confidence for unrecognized intent

        # Extract entities (simple implementation)
        entities = self._extract_entities(user_message)

        intent = Intent(
            type=intent_type,
            confidence=confidence,
            parameters={},  # Will be populated by MCP tools based on the intent
            extracted_entities=entities
        )

        return IntentRecognitionResult(
            intent=intent,
            raw_text=user_message,
            confidence=confidence
        )

    def _extract_entities(self, message: str) -> List[str]:
        """
        Extract entities from a message.
        In a real implementation, this would use NLP techniques.
        """
        # This is a simplified entity extraction
        # In a real implementation, we'd use more sophisticated NLP
        entities = []

        # Look for potential task descriptions (words that might be task titles)
        words = message.split()
        for word in words:
            # Simple heuristic: if the word is longer than 2 characters and doesn't look like a stop word
            if len(word) > 2 and word.lower() not in ["the", "and", "or", "but", "in", "on", "at", "to"]:
                # Remove punctuation
                clean_word = ''.join(c for c in word if c.isalnum() or c in [' ', '-', '_'])
                if clean_word and clean_word not in entities:
                    entities.append(clean_word)

        return entities

    def generate_response_for_intent(
        self,
        intent: Intent,
        user_message: str,
        additional_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate a contextual response based on the identified intent.
        """
        if intent.type == IntentType.CREATE_TASK:
            return f"I understand you want to create a task. I'll help you with that. You mentioned: '{user_message}'."
        elif intent.type == IntentType.VIEW_TASKS:
            return f"You'd like to view your tasks. I'll retrieve them for you."
        elif intent.type == IntentType.UPDATE_TASK:
            return f"I'll help you update your task based on your request: '{user_message}'."
        elif intent.type == IntentType.DELETE_TASK:
            return f"You want to delete a task. Could you please specify which task you'd like to remove?"
        elif intent.type == IntentType.MARK_COMPLETE:
            return f"I'll mark the appropriate task as complete based on your request: '{user_message}'."
        elif intent.type == IntentType.MARK_INCOMPLETE:
            return f"I'll mark the appropriate task as incomplete based on your request: '{user_message}'."
        else:
            return f"I received your message: '{user_message}'. How can I help you with your tasks?"