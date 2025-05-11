# Use the official Python image as the base image
FROM python:3.11
# Set the working directory inside the container
RUN apt-get update && apt-get install -y --no-install-recommends gcc \
    && pip install --upgrade pip
WORKDIR /app
# Copy the requirements.txt file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Copy the entire application into the container
COPY . .
# Run the main.py script inside the container when it starts
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]