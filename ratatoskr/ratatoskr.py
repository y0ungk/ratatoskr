import sys, logging
from flask import Flask, request
from jsonschema import validate, ValidationError, FormatChecker
from html2text import html2text
from .adapters import mailgun, mandrill

app = Flask(__name__)
app.config.from_object(__name__)  # load config from this file , ratatoskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    MAILGUN_API_KEY='__MAILGUN_API_KEY__',
    MANDRILL_API_KEY='__MANDRILL_API_KEY__',
    SELECTED_SERVICE='mailgun'
))
app.config.from_envvar('RATATOSKR_CFG', silent=True)
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


@app.route('/status')
def status():
    return 'Hello World!'  # simple health check for an ELB


def parse(email_request):
    schema = {
        'title': 'email_request',
        'type': 'object',
        'properties': {
            'to': {'type': 'string', 'format': 'email'},
            'to_name': {'type': 'string'},
            'from': {'type': 'string', 'format': 'email'},
            'from_name': {'type': 'string'},
            'subject': {'type': 'string'},
            'body': {'type': 'string'},
        },
        'required': ['to', 'to_name', 'from', 'from_name', 'subject', 'body']
    }
    result = email_request
    validate(email_request, schema, format_checker=FormatChecker())
    result['text'] = html2text(result['body'])
    return result


@app.route('/email', methods=['POST'])
def email():
    try:
        email_request = parse(request.get_json(True))
    except ValidationError as e:
        return e.message

    logging.debug("request: %r", email_request)

    if app.config['SELECTED_SERVICE'] is 'mailgun':
        response = mailgun.send(email_request)
    elif app.config['SELECTED_SERVICE'] is 'mailgun':
        response = mandrill.send(email_request)
    else:
        response = {'code':404, 'message':'no service configured'}

    result = 'email sent!'
    if response['code'] is not 200:
        result = 'there was an error: ' + response['message']

    logging.debug("response: %r", response)

    return result


if __name__ == '__main__':
    app.run()
