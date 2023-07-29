# Use the official Python image as the base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app
COPY pyproject.toml .
COPY /. /app/.
RUN pip install poetry==1.5.1
RUN poetry install

# Expose the port that FastAPI is running on
EXPOSE 8000
