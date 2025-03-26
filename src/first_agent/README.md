---
title: First Agent Template
emoji: ⚡
colorFrom: pink
colorTo: yellow
sdk: gradio
sdk_version: 5.15.0
app_file: app.py
pinned: false
tags:
- smolagents
- agent
- smolagent
- tool
- agent-course
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

# First Agent - AI Assistant with Gradio UI

This is an AI assistant agent built using the `smolagents` framework, featuring a Gradio web interface and Docker support. The agent can perform various tasks including time queries, web searches, and custom operations.

## Features

- 🤖 AI-powered assistant using Qwen2.5-Coder model
- 🌐 Web-based Gradio interface
- 🐳 Docker support for easy deployment
- 🔍 Built-in tools:
  - Time zone queries
  - DuckDuckGo web search
  - Custom tool support
  - Final answer formatting

## Prerequisites

- Python 3.9+
- Docker (optional, for containerized deployment)
- Required Python packages (see `requirements.txt`)

## Installation

### Local Installation

1. Install the required packages:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

### Docker Installation

1. Build the Docker image:
```bash
docker build -t first-agent -f src/first_agent/Dockerfile src/first_agent/
```

2. Run the container:
```bash
docker run --rm -p 7860:7860 first-agent
```

## Available Tools

### 1. Time Zone Tool
- Get current time in any timezone
- Example: "What time is it in New York?"

### 2. Custom Tool
- A template for custom functionality
- Easily extensible for specific use cases

### 3. DuckDuckGo Search
- Web search capabilities
- Real-time information retrieval

### 4. Final Answer Tool
- Formats and presents final responses
- Ensures consistent output formatting

## Configuration

### Model Settings
- Model: Qwen2.5-Coder
- Max Tokens: 2096
- Temperature: 0.5

### Agent Configuration
- Max Steps: 6
- Verbosity Level: 2
- Planning Interval: None

## Usage

1. Access the web interface at `http://localhost:7860`
2. Type your query in the chat interface
3. The agent will:
   - Process your request
   - Use appropriate tools
   - Provide a formatted response

## Development

### Adding New Tools

1. Use the `@tool` decorator
2. Define input/output types
3. Add to the agent's tool list in `app.py`

Example:
```python
@tool
def my_new_tool(arg1: str) -> str:
    """Tool description
    Args:
        arg1: argument description
    """
    return "result"
```

### Customizing the UI

The Gradio interface can be customized in `Gradio_UI.py`:
- Chat appearance
- File upload support
- Response formatting

## Troubleshooting

### Common Issues

1. Port 7860 in use:
```powershell
# PowerShell command to free the port
Get-Process python* | Where-Object {$_.MainWindowTitle -eq ""} | Stop-Process -Force
```

2. Docker issues:
```bash
# Check Docker logs
docker logs <container_id>
```

### Model Connection

If the model doesn't respond:
1. Check the alternative endpoint in `app.py`
2. Verify network connectivity
3. Monitor the debug output

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

[Your License Here]

## Acknowledgments

- Built with [smolagents](https://github.com/smol-ai/agents)
- UI powered by [Gradio](https://gradio.app/)
