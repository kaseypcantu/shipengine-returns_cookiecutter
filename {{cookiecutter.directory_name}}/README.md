# _{{ cookiecutter.project_name }}_

## Barebones Return Portal Starter - Powered by ShipEngine API

### Features:
- Flask Server backend, that has endpoints to make server-side API/HTTP requests to ShipEngine at the clients request.
- The frontend is server-side rendered HTML and API/HTTP request data using Jinja2 templating native to Flask.
- Facilitate acceptance of customer returns allowing them to create return labels and optionally schedule a pickup, powered by `ShipEngine API`.

## Install the project dependencies


## Run the server & Install dependencies
You will need to `cd` (change directory) into the newly generated Returns Portal directory and this command will install all dependencies used in this project.
```bash
pip install -r requirements.txt
```
- Next run this command to start the flask server.
```bash
python run.py
```
- You can now visit the `frontend` at http://localhost:5000/

## Notes on usage and deployment
- The server is configured to use the Sandbox API key by default. This means you will need to change [.env](./.env) on **line 8** variable `SHIPENGINE_CARRIER_ID` that the the [se_client.py](./{{ cookiecutter.module_name }}/se_client.py) uses on **line 47**, to the ShipEngine Production API Key. 
- You will also need to adjust your `carrier_id` from a `sandbox carrier_id` to one of `your connected carrier accounts` carrier_ids for use in `production`.