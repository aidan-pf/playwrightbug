FROM mcr.microsoft.com/playwright/python:v1.34.0-jammy

RUN apt update

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc g++ python3-dev libxml2-dev libxslt-dev wget libxtst6

# Install the required packages
RUN pip install --upgrade pip
RUN pip install psutil

# Copy the requirements file to the container
COPY requirements.txt ./

# Install the remaining required packages
RUN pip install -r requirements.txt

# Install Playwright and its browser dependencies
RUN playwright install-deps firefox
RUN playwright install firefox

# Copy the script to the container
COPY . ./

# Set the environment variable for the port number
ENV PORT 8080

# Expose the port for incoming traffic
EXPOSE 8080

# Set the entrypoint to run the script
CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT} --workers 1