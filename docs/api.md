# API Documentation

## POST /api/chat
Send a message. Body: `{"message": "text", "model": "sonnet-4.6"}`
Response: `{"response": "text", "model": "Claude Sonnet 4.6"}`

## POST /api/clear
Clear conversation history. Response: `{"status": "ok"}`

## POST /api/model
Change model. Body: `{"model": "haiku-4.5"}`
Response: `{"status": "ok", "model": "Claude Haiku 4.5"}`

## GET /api/health
Health check. Response: `{"status": "healthy", "model": "...", "region": "us-east-1"}`

## Available Models

| Key | Model ID | Display Name |
|-----|----------|-------------|
| sonnet-4.6 | us.anthropic.claude-sonnet-4-6-20250514 | Claude Sonnet 4.6 |
| sonnet-4.5 | us.anthropic.claude-sonnet-4-5-20250514 | Claude Sonnet 4.5 |
| haiku-4.5 | us.anthropic.claude-haiku-4-5-20250514 | Claude Haiku 4.5 |
| opus-4.5 | us.anthropic.claude-opus-4-5-20250514 | Claude Opus 4.5 |
