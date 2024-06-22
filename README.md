# BC24-API

This is the API for the BC24 Traceability project.

## Development

### env variables
Copy the `.env-template` and rename it to `.env`
Provide a validator url as well as the address of the deployed contract. 

Additionally provide wallet addresses and private keys of the users that will be using the api

### Run 
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


## Load Testing
We use locust to do stress and load testing for the API and respectively for the underlying BC. 

1. Make sure the api is running at `http://localhost:8000`
2. Run the locust service
   ```bash
      locust -f .\tests\stressTest.py
   ``` 
3. Navigate to `http://localhost:8089` 
4. Select a number of users, the time it takes to add a new user and provide the host (`http://localhost:8000`)
5. Run the tests and observe the results

