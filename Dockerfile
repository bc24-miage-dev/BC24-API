# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install poetry
RUN pip install poetry

# Disable virtualenv creation to ensure dependencies are installed in the container
RUN poetry config virtualenvs.create false

# Install project dependencies
RUN poetry install --no-dev

# Expose port 8000 for the API
EXPOSE 8000

# Define the command to start the server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]