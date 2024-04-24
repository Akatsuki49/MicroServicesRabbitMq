# Use the official Python 3.11.9 image as the base image
FROM python:3.11.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

ENV PYTHONUNBUFFERED=1

# Install dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the Python script
CMD ["python", "order_processing_consumer.py"]
