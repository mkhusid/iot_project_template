# File: hub/Dockerfile
FROM python:3.10.0-slim-bullseye
# Upgrade system packages and pip
RUN apt-get update && apt-get install -y --no-install-recommends gcc \
    && pip install --upgrade pip
# Set the working directory
WORKDIR /app
# Copy requirements file first to leverage docker cache
COPY requirements.txt .
# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Copy the rest of the code
COPY . .
# Expose the port and set the command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]