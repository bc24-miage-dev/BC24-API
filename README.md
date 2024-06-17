# BC24-API

This is the API for the BC24 Traceability project.

## Local Development

Follow these steps to launch the API locally:

1. Ensure you have Python 3.11 installed. You can download it from [here](https://www.python.org/downloads/).

2. Make sure poetry is installed

   ```bash
   pip install poetry
   ```

3. Install the required dependencies. If you're using Poetry, you can do this by running:

   ```bash
   poetry install
   ```

4. Start the Uvicorn server with reload enabled:

   ```bash
   uvicorn main:app --reload
   ```

The server will start on `http://localhost:8000`. You can view the API documentation at `http://localhost:8000/docs`.

### Running with Docker

If you prefer to use Docker for development or deployment, follow these steps to build and run your application inside a Docker container.

1. Build the Docker image:

   ```bash
   docker build -t bc24-api .
   ```

   This command builds a Docker image named `bc24-api` from the Dockerfile in the current directory.

2. Run the Docker container:

   ```bash
   docker run -d --name bc24-api-container -p 8000:8000 bc24-api
   ```

   This command runs the `bc24-api` image in a container named `bc24-api-container`. It also maps port 8000 of the container to port 8000 on the host, allowing you to access the API at `http://localhost:8000`.

You can now access the API and its documentation in the same way as running it locally without Docker.

# Stress Tests

MAKE SURE YOU KNOW WHAT YOU ARE DOING. THIS WILL LAUNCH THE TESTS ON THE CURRENT CONTRACT MENTIONED IN .ENV FILE AND WILL POTENTIALLY MESS UP THE CURRENT STATE OF THE BLOCKCHAIN! 

YOU HAVE BEEN WARNED.

```
 locust -f .\tests\stressTest.py
```

Navigate to the localhost site and start the tests with appropriate arguments.
