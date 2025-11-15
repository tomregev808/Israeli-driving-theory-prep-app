# Use an official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create a directory for instance and db
RUN mkdir -p /app/instance

# Expose the port Fly.io expects
EXPOSE 8080

# Tell Gunicorn to listen on all interfaces and port 8080
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:create_app()"]
