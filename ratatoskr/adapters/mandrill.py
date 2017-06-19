from flask import current_app as app
import requests, json

BASE_URL = 'https://mandrillapp.com/api/1.0'


def send(data):
    response = requests.post(
        BASE_URL + '/messages/send.json',
        data=json.dumps({
            'key': app.config['MANDRILL_API_KEY'],
            'message': {
                'to': [{
                    'name': data['to_name'],
                    'email': data['to'],
                    'type': 'to'
                }],
                'from_email': data['from'],
                'from_name': data['from_name'],
                'subject': data['subject'],
                'html': data['body'],
                'text': data['text'],
                'attachments': [
                    {
                        'type': 'text/plain',
                        'name': 'myfile.txt',
                        'content': 'ZXhhbXBsZSBmaWxl'
                    }
                ]
            }}))

    return {'code':response.status_code, 'message':response.text}
