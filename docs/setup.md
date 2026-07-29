# Setup Instructions

## Prerequisites

- Python 3.11+
- AWS account with Amazon Bedrock access enabled
- AWS CLI configured with default profile

## Quick Start

```bash
# Windows
scripts\run.bat        # CLI
scripts\run_web.bat    # Web GUI

# macOS/Linux
./scripts/run.sh       # CLI
./scripts/run_web.sh   # Web GUI
```

## Manual Installation

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -e .
python -m simplechatbot.cli
python -m simplechatbot.web.app
```
