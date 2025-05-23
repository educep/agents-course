# Agents Course

This course comes from the HuggingFace course: [course](https://huggingface.co/learn/agents-course/unit0/introduction)

## Features

- In process

## Project Setup Guide

This project uses **uv** as the package manager for faster and more reliable dependency management, and includes a **Makefile** for streamlined development workflows.

## Prerequisites

- Python 3.9 or higher
- Git
- **uv** package manager (will be installed automatically via Makefile)

## Quick Start

### 1. Install uv (if not already installed)
```bash
make install_uv
```

### 2. Create Virtual Environment
```bash
make venv
```

### 3. Activate Virtual Environment

**Windows:**
```powershell
.\activate.ps1
```

**Linux/MacOS:**
```bash
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
make install
```

This will install all required packages using **uv** for faster dependency resolution and installation.

## Available Make Commands

The project includes a comprehensive Makefile with the following commands:

| Command | Description |
|---------|-------------|
| `make install_uv` | Install uv package manager |
| `make venv` | Create virtual environment |
| `make install` | Install dependencies using uv |
| `make test` | Run tests with pytest |
| `make format` | Format code with black and isort |
| `make lint` | Run linting tools (format, flake8, pyupgrade) |
| `make check-all` | Run all checks and tests |
| `make clean` | Clean up environment |
| `make build` | Build Docker image |
| `make run` | Run Docker container |
| `make help` | Display all available commands |

## Running Applications

### Streamlit App
To run the Streamlit application, simply execute the provided PowerShell script from the root directory:

```powershell
.\run_st_fapp.ps1
```

This will start the Streamlit app located at `src/first_agent/st_app.py`.

### Gradio App (Dockerized)
The Gradio app in `src/first_agent/` should be run in a Docker container due to security issues with current library versions that are mitigated in a containerized environment.

To dockerize and run the Gradio app: see README.md in `src/first_agent/`.


## Environment Configuration

1. Create a `.env` file in the root directory:
```bash
touch .env  # For Linux/MacOS
# or manually create .env file in Windows
```

2. Add the following environment variables to your `.env` file:
```env
# Required Settings
DEEPSEEK_API_KEY="your-deepseek-api-key"

# Optional Settings (with defaults)
MYAPP_DEBUG=false
MYAPP_ENVIRONMENT=dev  # Options: dev, prod, staging
MYAPP_APP_NAME="MyApp"
```

### Environment Variables Description

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| DEEPSEEK_API_KEY | Yes | - | API key for DEEPSEEK platform |
| MYAPP_DEBUG | No | false | Enable/disable debug mode |
| MYAPP_ENVIRONMENT | No | dev | Application environment (dev/prod/staging) |
| MYAPP_APP_NAME | No | MyApp | Name of the application |

## Usage

The application uses Pydantic settings for configuration management. You can import and use the settings in your code like this:

```python
from config.settings import settings

# Access configuration values
api_key = settings.deepseek_api_key
debug_mode = settings.debug
current_env = settings.environment
```

## Development

### Project Structure

```
├── config/
│   └── settings.py         # Configuration management
├── src/
│   └── first_agent/        # Main agent application
│       ├── app.py          # Main application
│       ├── st_app.py       # Streamlit app
│       ├── Gradio_UI.py    # Gradio interface
│       ├── Streamlit_UI.py # Streamlit interface
│       └── Dockerfile      # Docker configuration for Gradio app
├── Makefile               # Development commands
├── run_st_fapp.ps1       # Script to run Streamlit app
├── activate.ps1          # Windows activation script
├── .venv/                # Virtual environment (not in repo)
├── .env                  # Environment variables (not in repo)
├── .gitignore           # Git ignore file
└── README.md           # This file
```

### Development Workflow

1. **Setup**: Use `make venv` and `make install` for initial setup
2. **Code Quality**: Use `make format` and `make lint` before committing
3. **Testing**: Run `make test` to ensure all tests pass
4. **All Checks**: Use `make check-all` for comprehensive validation

### Adding New Settings

To add new configuration settings:

1. Add the environment variable to your `.env` file
2. Add the corresponding field in `config/settings.py`
3. Update this README with the new variable details

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Run `make check-all` to ensure code quality
4. Submit a pull request

## Security Notes

- Never commit the `.env` file to version control
- Keep your API keys and secrets secure
- Use environment variables for sensitive information
- **Important**: Use the dockerized Gradio app to avoid security vulnerabilities in current library versions

## License

[Your License Here]

## Data Structure

The dashboard uses synthetic data generated with the following structure:

### Product Nomenclature
- product_id: Unique identifier for each product
- product_type: Category (MEUBLE or DECO)
- product_name: Name of the product

### Transactions
- transaction_id: Unique identifier for each transaction
- date: Transaction date
- order_id: Order identifier
- client_id: Customer identifier
- prod_id: Product identifier
- prod_price: Product price
- prod_qty: Quantity sold

## Usage

1. The main chart shows product sales distribution
2. Use the animation controls to switch between different views
3. View summary statistics in the metrics section
4. Toggle the "Show Raw Data" checkbox to see the complete dataset

## Dependencies

Dependencies are managed using **uv** for faster installation and resolution. Main dependencies include:

- streamlit
- ipyvizzu
- pandas
- loguru

To see the complete list of dependencies, check the `requirements.txt` file.
