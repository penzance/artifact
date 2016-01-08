from django.test import TestCase

from django.test import RequestFactory
from mock import patch, Mock, ANY
from artifact.utils import create_json_200_response, create_context_error_response

class TestUtils(TestCase):

    longMessage = True

    def setUp(self):
        self.request = RequestFactory().post('/fake-path')
        self.request.user = Mock(name='user_mock')
        self.request.user.is_authenticated.return_value = True

    def test_create_json_200_response_ok(self):
        result = create_json_200_response()
        value = '{}'.format(result)
        self.assertEqual('Content-Type: application/json\r\n\r\n{"message": "success"}', value)

    @patch('artifact.utils.HttpResponse')
    def test_create_context_error_response_no_message_no_template(self, mock_http):
        result = create_context_error_response(self.request)
        #print mock_http.mock_calls
        mock_http.assert_called_with('<html><head></head><body>It looks like you have been working on multiple Canvas sites. </body></html>', content_type='text/html', status=400)

    @patch('artifact.utils.render')
    @patch('artifact.utils.HttpResponse')
    def test_create_context_error_response_no_message_with_template(self, mock_http, mock_render):
        result = create_context_error_response(self.request, template='test')
        mock_render.assert_called_with(ANY, 'test', {'message': 'It looks like you have been working on multiple Canvas sites. '})

