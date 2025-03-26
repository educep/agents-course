FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gradio pytz pyyaml

# Copy the application code
COPY . /app/src/first_agent/

# Add the app directory to Python path
ENV PYTHONPATH=/app

# Expose the port Gradio will run on
EXPOSE 7860

# Set the working directory to where the app.py is located
WORKDIR /app/src/first_agent

# Command to run the application
CMD ["python", "app.py"]

# docker build -t first-agent -f src/first_agent/Dockerfile src/first_agent/
# docker run -p 7860:7860 first-agent
# http://localhost:7860/
