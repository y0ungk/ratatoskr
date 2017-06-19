ratatoskr
=========

A flask microservice as a façade of external email services to allow failover

## Requirements

* virtualenv

## Usage

Create a virtualenv from the root of the project directory

```bash
virtualenv venv
. venv/bin/activate
```

Now, install the app

```bash
pip install --editable .
```

For local development edit configuration in the ratatoskr.py file. For stage/production export an RATATOSKR_CFG 
environment variable pointing to a configuration file. For example:

```bash
export RATATOSKR_CFG=/path/to/settings.cfg
```

This will allow configuration to be changed separately from a code push as long the configs are kept separately.  

Next, set flask to use ratatoskr and then run:

```bash
export FLASK_APP=ratatoskr
flask run
```

Congrats, you are now running ratatoskr!  The app can now be reached at http://localhost:5000/

If you need to modify dependencies, make changes in `setup.py`.

## Run tests

To run all tests (recommend running inside virtualenv also):

```bash
python setup.py test
```

## Architecture

We've chosen flask and therefore python for it's simplicity and fantastic package support.

Packages we're using in addition to flask:
* json_schema - schema validation for json inputs
* html2text - html to plain text conversion (RIP Aaron Swartz)
* requests - http library
 
Supported Adapters
* mailgun
* mandrill (mailchimp)

## Future improvements

* Production setup: While lightweight and easy to use, Flask’s built-in server is not suitable for production as it does 
not scale well and by default serves only one request at a time. Probably would avoid mod_wsgi and leverage either uWSGI 
or gunicorn depending on infrastructure demands. Would require more research.
* Monitoring/logging: Monitoring and better logging is a must for production use
* Realtime failover: Instead of using a configuration change, we can fail over in realtime when a service provider goes 
down
* Better exception/error handling: Very rudimentary handling so far.  We can be more robust in the codes and messages we
return back.
* Documentation/tests: Missing API documentation with endpoints and examples. Generally just testing logic in the main
controller.

## Fun Fact
Per Wikipedia, in Norse mythology, Ratatoskr is a squirrel who runs up and down the world tree Yggdrasil to carry 
messages between the Veðrfölnir, perched atop Yggdrasil, and the wyrm Níðhöggr, who dwells beneath one of the three 
roots of the tree. 

This concept of ferrying messages from one world to another made the name fit well with the purpose of this project. ^^v 