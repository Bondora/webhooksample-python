# webhooksample-python

This is a simple Python 3 Flask app that can receive Bondora API's webhook calls.

## Installation

The app uses a Python `venv`, you can set it up after cloning the code with these commands:

```
$ python3 -m venv venv
```

Then to activate the environment:

```
$ . venv/bin/activate
```

On Windows, the process is like this in Powershell:

```
PS> C:\Python37\python.exe -m venv venv
PS> . venv\Scripts\Activate.ps1
```

Or similar, depending on where Python is installed.

Then install the `pip` dependencies:

```
(venv) $ pip install -r requirements.txt
```

## Config

Copy `app.default.cfg` to `app.cfg` and make changes inside.
Most importantly the HTTP signing keys that are registered on the webhook.
Also, recommended to configure the hostname.

## Running

You need to have the environment active (there will be a `(venv)` on the prompt).
Next run [Flask](https://palletsprojects.com/p/flask/):

```
(venv) $ flask run
```

It will run the app at http://localhost:5000/ but if this is not desired you can use:

```
(venv) $ flask run --host 0.0.0.0 --port 8080
```

To bind to IP 0.0.0.0 (accepting requests from everywhere) and port 8080 for example.

## Data

The webhook saves the received payload JSON objects to the configured data directory.