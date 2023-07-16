# Use the official Python base image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR  /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY . .

# Expose the desired port for the Flask application
EXPOSE 5000

# Set the entrypoint command to run the Flask application
CMD ["python", "app.py"]

