import unittest, json
from mock import patch
from ratatoskr import ratatoskr


class RatatoskrTests(unittest.TestCase):
    def setUp(self):
        self.app = ratatoskr.app.test_client()
        ratatoskr.app.testing = True
        self.example = {
            'to': 'fake@example.com',
            'to_name': 'Mr. Fake',
            'from': 'noreply@mybrightwheel.com',
            'from_name': 'Brightwheel',
            'subject': 'A Message from Brightwheel',
            'body': '<h1>Your Bill</h1><p>$10</p>'
        }

    def test_valid_request(self):
        email_request = ratatoskr.parse(self.example)
        self.assertEqual(email_request['text'], b'# Your Bill\n\n$10\n\n')
        self.assertEqual(email_request['to'], 'fake@example.com')
        self.assertEqual(email_request['to_name'], 'Mr. Fake')
        self.assertEqual(email_request['from'], 'noreply@mybrightwheel.com')
        self.assertEqual(email_request['from_name'], 'Brightwheel')
        self.assertEqual(email_request['subject'], 'A Message from Brightwheel')
        self.assertEqual(email_request['body'], '<h1>Your Bill</h1><p>$10</p>')

    def test_missing_to_field_in_request(self):
        example = self.example
        del example['to']
        with self.assertRaises(ratatoskr.ValidationError) as cm:
            ratatoskr.parse(example)

        the_exception = cm.exception
        self.assertEqual(the_exception.message, "'to' is a required property")

    def test_missing_to_name_field_in_request(self):
        example = self.example
        del example['to_name']
        with self.assertRaises(ratatoskr.ValidationError) as cm:
            ratatoskr.parse(example)

        the_exception = cm.exception
        self.assertEqual(the_exception.message, "'to_name' is a required property")

    def test_missing_from_field_in_request(self):
        example = self.example
        del example['from']
        with self.assertRaises(ratatoskr.ValidationError) as cm:
            ratatoskr.parse(example)

        the_exception = cm.exception
        self.assertEqual(the_exception.message, "'from' is a required property")

    def test_missing_from_name_field_in_request(self):
        example = self.example
        del example['from_name']
        with self.assertRaises(ratatoskr.ValidationError) as cm:
            ratatoskr.parse(example)

        the_exception = cm.exception
        self.assertEqual(the_exception.message, "'from_name' is a required property")

    def test_missing_subject_field_in_request(self):
        example = self.example
        del example['subject']
        with self.assertRaises(ratatoskr.ValidationError) as cm:
            ratatoskr.parse(example)

        the_exception = cm.exception
        self.assertEqual(the_exception.message, "'subject' is a required property")

    def test_missing_body_field_in_request(self):
        example = self.example
        del example['body']
        with self.assertRaises(ratatoskr.ValidationError) as cm:
            ratatoskr.parse(example)

        the_exception = cm.exception
        self.assertEqual(the_exception.message, "'body' is a required property")

    def test_invalid_recipient_email_format(self):
        example = self.example
        example['to'] = 'fake'
        with self.assertRaises(ratatoskr.ValidationError) as cm:
            ratatoskr.parse(example)

        the_exception = cm.exception
        self.assertEqual(the_exception.message, "'fake' is not a 'email'")

    def test_invalid_sender_email_format(self):
        example = self.example
        example['from'] = 'noreply'
        with self.assertRaises(ratatoskr.ValidationError) as cm:
            ratatoskr.parse(example)

        the_exception = cm.exception
        self.assertEqual(the_exception.message, "'noreply' is not a 'email'")

    @patch('ratatoskr.adapters.mailgun.send')
    def test_mailgun_successful_send(self, test_patch):
        test_patch.return_value = {'code': 200, 'message': 'email queued for sending...'}
        ratatoskr.app.config['SELECTED_SERVICE'] = 'mailgun'
        result = self.app.post('/email', data=json.dumps(self.example), follow_redirects=True)
        self.assertEqual(result.data, 'email sent!')

    @patch('ratatoskr.adapters.mandrill.send')
    def test_mandrill_successful_send(self, test_patch):
        test_patch.return_value = {'code':200, 'message':'email queued for sending...'}
        ratatoskr.app.config['SELECTED_SERVICE'] = 'mandrill'
        result = self.app.post('/email', data=json.dumps(self.example), follow_redirects=True)
        self.assertEqual(result.data, 'email sent!')

    @patch('ratatoskr.adapters.mailgun.send')
    def test_mailgun_failed_send(self, mailgun_patch):
        mailgun_patch.return_value = {'code': 500, 'message': 'egads, mailgun down!'}
        ratatoskr.app.config['SELECTED_SERVICE'] = 'mailgun'
        result = self.app.post('/email', data=json.dumps(self.example), follow_redirects=True)
        self.assertEqual(result.data, 'there was an error: ' + 'egads, mailgun down!')

    @patch('ratatoskr.adapters.mandrill.send')
    def test_mandrill_failed_send(self, test_patch):
        test_patch.return_value = {'code': 500, 'message': 'egads, mandrill down!'}
        ratatoskr.app.config['SELECTED_SERVICE'] = 'mandrill'
        result = self.app.post('/email', data=json.dumps(self.example), follow_redirects=True)
        self.assertEqual(result.data, 'there was an error: ' + 'egads, mandrill down!')

if __name__ == '__main__':
    unittest.main()
