# SimpleChatbot

A production-ready Python chatbot powered by Amazon Bedrock Anthropic models. Features both a CLI interface for quick testing and a Flask-based web GUI with a modern, responsive design.

## Features

- **Multiple Anthropic Models**: Choose between Claude Sonnet 4.6, Sonnet 4.5, Haiku 4.5, and Opus 4.5
- **CLI Interface**: Beautiful terminal-based chat using Rich library
- **Web GUI**: Modern Flask-based interface with real-time chat
- **AWS Integration**: Uses Amazon Bedrock Runtime with default AWS profile
- **Production-Ready**: Comprehensive error handling, type hints, and documentation

## Quick Start

### Prerequisites

- Python 3.11+
- AWS account with Bedrock access enabled
- AWS CLI configured with default profile (`aws configure`)

### Windows

```batch
scripts\run.bat
scripts\run_web.bat
```

### macOS/Linux

```bash
chmod +x scripts/run.sh
./scripts/run.sh
./scripts/run_web.sh
```

## Configuration

The chatbot uses the default AWS profile. Set the region to `us-east-1` (default) or update in `.env`.

## License

MIT License - see [LICENSE](LICENSE) for details.
