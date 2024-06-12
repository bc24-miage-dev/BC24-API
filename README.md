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

## Deployment to Raspberry Pin (not yet working, Architecture problems)

To deploy the Docker image to a Raspberry Pi, follow these steps:

1. **Save the Docker Image**: First, save your Docker image to a tar file on your local machine.

   ```bash
   ddocker save bc24-api -o bc24-api.tar
   ```

2. **Transfer the Image to Raspberry Pi**: Use `scp` to securely transfer the image file to your Raspberry Pi. Replace `raspberry_pi_username` with your actual Raspberry Pi's username and `raspberry_pi_ip` with its IP address.

   ```bash
   scp bc24-api.tar pi@45.80.25.84:~/Documents
   ```

3. **Load the Image on Raspberry Pi**: SSH into your Raspberry Pi, navigate to the directory where you transferred the tar file, and load the image into Docker.

   ```bash
   ssh pi@45.80.25.84
   cd ~/Documents
   (rm -rf bc24-api.tar) # if the image is already present
   docker load -i bc24-api.tar
   ```

4. **Run the Docker Container on Raspberry Pi**: Finally, run the Docker container on your Raspberry Pi.  

   ```bash
   docker run -d --name bc24-api-container -p 8000:8000 bc24-api
   ```
   **Adjust the port if needed or already in use!**

   This command runs the `bc24-api` image in a container named `bc24-api-container` on your Raspberry Pi. It also maps port 8000 of the container to port 8000 on the Raspberry Pi, allowing you to access the API at `http://raspberry_pi_ip:8000`.

Now, your API is running on a Raspberry Pi, and you can access it using the Raspberry Pi's IP address.
