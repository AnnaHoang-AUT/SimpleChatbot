"""Configuration and settings for SimpleChatbot."""

import os
from dataclasses import dataclass, field
from typing import ClassVar

from dotenv import load_dotenv

load_dotenv()


@dataclass
class BedrockModel:
    """Represents an Amazon Bedrock Anthropic model configuration."""
    model_id: str
    display_name: str
    description: str


AVAILABLE_MODELS: dict[str, BedrockModel] = {
    "sonnet-4.6": BedrockModel(
        model_id="us.anthropic.claude-sonnet-4-6",
        display_name="Claude Sonnet 4.6",
        description="Latest and most capable balanced model - best for complex tasks",
    ),
    "sonnet-4.5": BedrockModel(
        model_id="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
        display_name="Claude Sonnet 4.5",
        description="High-performance model with strong reasoning capabilities",
    ),
    "haiku-4.5": BedrockModel(
        model_id="us.anthropic.claude-haiku-4-5-20251001-v1:0",
        display_name="Claude Haiku 4.5",
        description="Fast and cost-effective for simple tasks",
    ),
    "opus-4.5": BedrockModel(
        model_id="us.anthropic.claude-opus-4-5-20251101-v1:0",
        display_name="Claude Opus 4.5",
        description="Most powerful model for highly complex reasoning",
    ),
}

DEFAULT_MODEL_KEY: str = "sonnet-4.6"


@dataclass
class ChatbotConfig:
    """Configuration settings for the SimpleChatbot application."""

    aws_region: str = field(default_factory=lambda: os.getenv("AWS_DEFAULT_REGION", "us-east-1"))
    model_key: str = field(default_factory=lambda: DEFAULT_MODEL_KEY)
    max_tokens: int = field(default_factory=lambda: int(os.getenv("MAX_TOKENS", "4096")))
    conversation_history_limit: int = field(default_factory=lambda: int(os.getenv("CONVERSATION_HISTORY_LIMIT", "20")))
    system_prompt: str = field(default=(
        "You are a helpful, knowledgeable, and friendly AI assistant powered by "
        "Amazon Bedrock. You provide clear, accurate, and concise responses. "
        "When you don't know something, you say so honestly. You can help with "
        "a wide range of topics including programming, writing, analysis, math, "
        "and general knowledge. Always be respectful and professional."
    ))
    flask_host: str = field(default_factory=lambda: os.getenv("FLASK_HOST", "127.0.0.1"))
    flask_port: int = field(default_factory=lambda: int(os.getenv("FLASK_PORT", "5000")))
    flask_debug: bool = field(default_factory=lambda: os.getenv("FLASK_DEBUG", "false").lower() == "true")

    MODELS: ClassVar[dict[str, BedrockModel]] = AVAILABLE_MODELS

    @property
    def model(self) -> BedrockModel:
        return AVAILABLE_MODELS.get(self.model_key, AVAILABLE_MODELS[DEFAULT_MODEL_KEY])

    @property
    def model_id(self) -> str:
        return self.model.model_id

    def set_model(self, model_key: str) -> None:
        if model_key not in AVAILABLE_MODELS:
            valid_keys = ", ".join(AVAILABLE_MODELS.keys())
            raise ValueError(f"Invalid model key '{model_key}'. Available: {valid_keys}")
        self.model_key = model_key
