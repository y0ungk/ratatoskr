from flask import current_app as app
import re, requests

BASE_URL = 'https://api.mailgun.net/v3'


def send(data):
    # mailgun endpoint needs to match the sending domain from sender email,
    # so we'll extract it from the email rather than using a configuration
    email_segments = re.split("@", data['from'])
    response = requests.post(
        BASE_URL + '/' + email_segments[1] + '/messages',
        auth=('api', app.config['MAILGUN_API_KEY']),
        data={
            'to': data['to_name'] + ' <' + data['to'] + '>',
            'from': data['from_name'] + ' <' + data['from'] + '>',
            'subject': data['subject'],
            'html': data['body'],
            'text': data['text']
        })

    return {'code':response.status_code, 'message':response.text}
