# Use the official Python image as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP = main.py

# Copy the application code into the container
COPY . .

# Expose the port that the Flask app runs on
EXPOSE 8080

# Define the command to run the Flask application when the container starts
CMD ["python", "main.py"]
