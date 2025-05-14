# Agents course

This course comes from the HuggingFace course: [course](https://huggingface.co/learn/agents-course/unit0/introduction)

## Features

- In process

## Project Setup Guide

## Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- Git

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/MacOS
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

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
│   └── settings.py     # Configuration management
├── .venv/              # Virtual environment (not in repo)
├── .env              # Environment variables (not in repo)
├── .gitignore       # Git ignore file
└── README.md        # This file
```

### Adding New Settings

To add new configuration settings:

1. Add the environment variable to your `.env` file
2. Add the corresponding field in `config/settings.py`
3. Update this README with the new variable details

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Submit a pull request

## Security Notes

- Never commit the `.env` file to version control
- Keep your API keys and secrets secure
- Use environment variables for sensitive information

## License

[Your License Here]

## Running the Application

To run the Streamlit app:

```bash
streamlit run streamlit_app.py
```

The application will open in your default web browser at `http://localhost:8501`.

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

- streamlit
- ipyvizzu
- pandas
- loguru
