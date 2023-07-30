# Use the official Python image as the base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app
COPY /. /app/.
COPY requirements.txt .
RUN pip install -r requirements.txt
