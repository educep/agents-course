FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy the entire project structure first
COPY . /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Add the app directory to Python path
ENV PYTHONPATH=/app

# Expose the port Gradio will run on
EXPOSE 7860

# Set the working directory
WORKDIR /app

# Command to run the application
CMD ["python", "src/first_agent/app.py"]

# Build command:
# docker build -t first-agent -f src/first_agent/Dockerfile .
# Run command with environment variables:
# docker run -p 7860:7860 --env-file .env first-agent
# http://localhost:7860/
