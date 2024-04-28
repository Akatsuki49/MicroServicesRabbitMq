# Use an official Python runtime as a base image
FROM python:3.9.11

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose any ports the app is expecting
EXPOSE 5000

ENV PYTHONUNBUFFERED=1

# Define environment variables
ENV RABBITMQ_HOST=rabbitmq
ENV MONGO_HOST=mongodb

# Command to run the application
CMD ["python", "server.py"]
