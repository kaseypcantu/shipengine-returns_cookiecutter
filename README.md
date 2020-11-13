# ShipEngine Return Shipments Portal - Cookiecutter template

## Return Portal Base - Powered by _`ShipEngine API`_

### Features:
- Flask Server backend, that has endpoints to make server-side API/HTTP requests to ShipEngine at the clients request.
- The frontend is server-side rendered HTML and API/HTTP request data using Jinja2 templating native to Flask.
- Facilitate acceptance of customer returns allowing them to create return labels and optionally schedule a pickup.
- Docker Compose file includes Postgres, Redis, and PGAdmin, and is ready for use during development via `docker-compose up -d`.

## Prerequisites
You will need your `ShipEngine API Key` handy, and if you don't have one yet you can create a free ShipEngine account here -> [Create a free ShipEngine account](https://www.shipengine.com/signup/ "ShipEngine Sign Up")

## Usage:
This project is to be used with the [Cookiecutter](https://github.com/cookiecutter/cookiecutter "Cookiecutter Github Page") python package and you will need to download it first to make use of this cookiecutter template.
- You can download it via `pip` using the following command:
```bash
pip install --user cookiecutter
```

Once you have downloaded `cookiecutter` you will need to run cookiecutter against this repo:
- You can specify a direct github url in the command as shown below:
```bash
cookiecutter https://github.com/kaseypcantu/shipengine-returns_cookiecutter
```
- Running this command will run cookiecutter against this template, and in doing so you will be met with a few configuration questions at the command-line. It is **imperative** that you provide an answer to each prompt, this will ensure that your generate returns portal will work out of the box. 

- You now have a directory titled the name provided in configuration, that houses a working base to hit the ground running when it comes to building a Shipping Returns Portal powered by `ShipEngine`. 

## Run the server
You will need to `cd` (change directory) into the newly generated Returns Portal directory and run this command to start the flask server.
```bash
python run.py
```
- You can now visit the `frontend` at http://localhost:5000/

## Notes on usage and deployment
- You will be asked to enter your ShipEngine Sandbox and Production API key, and the server is configured to use the Sandbox API key by default. This means you will need to change the the `se_client.py` to use the Production API key env variable. 
- You will also need to adjust your carrier_id from a sandbox carrier_id to one of your connected carrier accounts carrier_ids for use in production.