"""Core chatbot logic for SimpleChatbot."""

import json
import logging
from typing import Any

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from simplechatbot.config import ChatbotConfig

logger = logging.getLogger(__name__)


class SimpleChatbot:
    """A chatbot powered by Amazon Bedrock Anthropic models."""

    def __init__(self, config: ChatbotConfig | None = None) -> None:
        self.config = config or ChatbotConfig()
        self.conversation_history: list[dict[str, str]] = []
        self._client = self._create_client()

    def _create_client(self) -> Any:
        try:
            client = boto3.client("bedrock-runtime", region_name=self.config.aws_region)
            logger.info("Bedrock Runtime client created for region: %s", self.config.aws_region)
            return client
        except (BotoCoreError, ClientError) as e:
            raise RuntimeError(f"Failed to create Bedrock Runtime client: {e}") from e

    def get_response(self, user_message: str) -> str:
        self.conversation_history.append({"role": "user", "content": [{"text": user_message}]})
        self._trim_history()

        try:
            response = self._client.converse(
                modelId=self.config.model_id,
                messages=self.conversation_history,
                system=[{"text": self.config.system_prompt}],
                inferenceConfig={"maxTokens": self.config.max_tokens, "temperature": 0.7},
            )
            assistant_message = response["output"]["message"]
            assistant_text = assistant_message["content"][0]["text"]
            self.conversation_history.append({"role": "assistant", "content": [{"text": assistant_text}]})
            logger.info("Response received from model: %s", self.config.model_id)
            return assistant_text

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            error_message = e.response["Error"]["Message"]
            self.conversation_history.pop()
            if error_code == "ThrottlingException":
                raise RuntimeError("Request was throttled. Please wait and try again.") from e
            elif error_code == "AccessDeniedException":
                raise RuntimeError("Access denied. Ensure Bedrock permissions are configured.") from e
            else:
                raise RuntimeError(f"Bedrock API error ({error_code}): {error_message}") from e

        except BotoCoreError as e:
            self.conversation_history.pop()
            raise RuntimeError(f"AWS SDK error: {e}") from e

        except Exception as e:
            if self.conversation_history and self.conversation_history[-1]["role"] == "user":
                self.conversation_history.pop()
            raise RuntimeError(f"Unexpected error: {e}") from e

    def _trim_history(self) -> None:
        max_messages = self.config.conversation_history_limit * 2
        if len(self.conversation_history) > max_messages:
            self.conversation_history = self.conversation_history[-max_messages:]

    def clear_history(self) -> None:
        self.conversation_history = []
        logger.info("Conversation history cleared.")

    def set_model(self, model_key: str) -> None:
        self.config.set_model(model_key)
        logger.info("Model changed to: %s", self.config.model.display_name)

    @property
    def current_model_name(self) -> str:
        return self.config.model.display_name
