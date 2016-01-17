import json

from django.test import TestCase
from django.test import RequestFactory
from mock import patch, Mock, ANY

from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import APITestCase

from artifact.models import Map, Markers
from artifact.utils import create_json_200_response, create_context_error_response
from artifact.views import map_index, location
from artifact.api import map_collection, map_location, download_csv, marker_collection, csv_points


class SerializerStub(object):

    def __init__(self, arg):
        super(SerializerStub, self).__init__()
        self.data = arg
        self.map = arg

# utils.py


class TestUtils(TestCase):

    longMessage = True

    def setUp(self):
        self.request = RequestFactory().post('/fake-path')
        self.request.user = Mock(name='user_mock')
        self.request.user.is_authenticated.return_value = True

    def test_create_json_200_response_ok(self):
        result = create_json_200_response()
        value = '{}'.format(result)
        self.assertEqual(
            'Content-Type: application/json\r\n\r\n{"message": "success"}', value)

    @patch('artifact.utils.HttpResponse')
    def test_create_context_error_response_no_message_no_template(self, mock_http):
        result = create_context_error_response(self.request)
        mock_http.assert_called_with(
            '<html><head></head><body>It looks like you have been working on multiple Canvas sites. </body></html>', content_type='text/html', status=400)

    @patch('artifact.utils.render')
    @patch('artifact.utils.HttpResponse')
    def test_create_context_error_response_no_message_with_template(self, mock_http, mock_render):
        result = create_context_error_response(self.request, template='test')
        mock_render.assert_called_with(ANY, 'test', {
                                       'message': 'It looks like you have been working on multiple Canvas sites. '})


# views.py
class TestViews(TestCase):

    longMessage = True

    def setUp(self):
        self.request = RequestFactory().get('/fake-path')
        self.request.user = Mock(name='user_mock')
        self.request.user.is_authenticated.return_value = True
        self.request.LTI = {"custom_canvas_course_id": 73}

    @patch('artifact.views.render')
    def test_map_index(self, mock_render):
        canvas_course_id = self.request.LTI["custom_canvas_course_id"]
        map_index(self.request)
        mock_render.assert_called_with(
            self.request, 'artifact/map_index.html', {'canvas_course_id': canvas_course_id})

    @patch('artifact.views.render')
    def test_location(self, mock_render):
        map_id = 1
        result = location(self.request, map_id)
        mock_render.assert_called_with(
            self.request, 'artifact/location.html', {'map_id': map_id})

# api.py


class TestAPI_GET(APITestCase):

    longMessage = True

    def setUp(self):
        self.request = APIRequestFactory().get('/fake-path')
        self.request.user = Mock(name='user_mock')
        self.request.user.is_authenticated.return_value = True
        self.request.LTI = {}
        Map.objects.create(id=1,
                           canvas_course_id=73,
                           title="title",
                           description="description",
                           latitude="43",
                           longitude="72",
                           zoom=4,
                           maptype=1,
                           created_by_id="huid",
                           modified_by_id="huid",
                           created_by_full_name="name",
                           date_created="2015-09-12 03:26:23.222+00",
                           date_modified="2015-09-12 03:26:23.222+00")
        Markers.objects.create(id=1,
                               title="title",
                               latitude="24",
                               longitude="25",
                               description="description",
                               external_url="blank",
                               created_by_id="huid",
                               modified_by_id="huid",
                               date_created="2015-09-12 03:26:23.222+00",
                               date_modified="2015-09-12 03:26:23.222+00",
                               map_id=1,
                               created_by_full_name="name")

    @patch('artifact.api.MapSerializer')
    def test_map_collection_GET(self, mock_serializer):
        canvas_course_id = 73
        mockvalue = [{"id": 1,
                      "canvas_course_id": 73,
                      "title": "title",
                      "latitude": "43",
                      "longitude": "72",
                      "zoom": 4,
                      "maptype": 1,
                      "thumbnail": "https://maps.googleapis.com/maps/api/staticmap?center=43,72&zoom=4&size=200x150&maptype=satellite",
                      "markers": [{"title": "title",
                                   "map": 1,
                                   "latitude": "24",
                                   "longitude": "25",
                                   "description": "description",
                                   "external_url": "blank",
                                   "created_by_id": "huid",
                                   "created_by_full_name": "name",
                                   "modified_by_id": "huid",
                                   "date_created": "2015-09-12T03:26:23.222000Z",
                                   "date_modified": "2015-09-12T03:26:23.222000Z"}],
                      "date_created": "2015-09-12T03:26:23.222000Z",
                      "date_modified": "2015-09-12T03:26:23.222000Z",
                      "created_by_id": "huid",
                      "created_by_full_name": "name",
                      "modified_by_id": "huid",
                      "description": "description"}]
        mock_serializer.return_value = SerializerStub(mockvalue)
        result = map_collection(self.request, canvas_course_id)
        self.assertTrue(status.is_success(result.status_code))
        self.assertEqual(json.loads(result.render().content), mockvalue)

    @patch('artifact.api.MapSerializer')
    def test_map_location_Key_Exists(self, mock_serializer):
        map_id = 1
        returnvalue = {"id": 1,
                       "canvas_course_id": 73,
                       "title": "title",
                       "latitude": "43",
                       "longitude": "72",
                       "zoom": 4,
                       "maptype": 1,
                       "thumbnail": "https://maps.googleapis.com/maps/api/staticmap?center=43,72&zoom=4&size=200x150&maptype=satellite",
                       "markers": [{"title": "title",
                                    "map": 1,
                                    "latitude": "24",
                                    "longitude": "25",
                                    "description": "description",
                                    "external_url": "blank",
                                    "created_by_id": "huid",
                                    "created_by_full_name": "name",
                                    "modified_by_id": "huid",
                                    "date_created": "2015-09-12T03:26:23.222000Z",
                                    "date_modified": "2015-09-12T03:26:23.222000Z"}],
                       "date_created": "2015-09-12T03:26:23.222000Z",
                       "date_modified": "2015-09-12T03:26:23.222000Z",
                       "created_by_id": "huid",
                       "created_by_full_name": "name",
                       "modified_by_id": "huid",
                       "description": "description"}
        mock_serializer.return_value = SerializerStub(returnvalue)
        result = map_location(self.request, map_id)
        self.assertTrue(status.is_success(result.status_code))
        self.assertEqual(json.loads(result.render().content), returnvalue)

    def test_map_location_Key_DoesnotExist(self):
        map_id = 5
        result = map_location(self.request, map_id)
        self.assertTrue(status.is_client_error(result.status_code))

    def test_download_csv_Key_DoesnotExist(self):
        map_id = 5
        result = download_csv(self.request, map_id)
        self.assertTrue(status.is_client_error(result.status_code))

    # @patch('artifact.api.MapSerializer')
    # @patch('artifact.api.HttpResponse')
    # def test_download_csv(self, mock_map, mock_http, mock_serializer):
    def test_download_csv(self):
        map_id = 1
        # stuff = {"id": 1,
        #                "canvas_course_id": 73,
        #                "title": "title",
        #                "latitude": "43",
        #                "longitude": "72",
        #                "zoom": 4,
        #                "maptype": 1,
        #                "thumbnail": "https://maps.googleapis.com/maps/api/staticmap?center=43,72&zoom=4&size=200x150&maptype=satellite",
        #                "markers": [{"title": "title",
        #                             "map": 1,
        #                             "latitude": "24",
        #                             "longitude": "25",
        #                             "description": "description",
        #                             "external_url": "blank",
        #                             "created_by_id": "huid",
        #                             "created_by_full_name": "name",
        #                             "modified_by_id": "huid",
        #                             "date_created": "2015-09-12T03:26:23.222000Z",
        #                             "date_modified": "2015-09-12T03:26:23.222000Z"}],
        #                "date_created": "2015-09-12T03:26:23.222000Z",
        #                "date_modified": "2015-09-12T03:26:23.222000Z",
        #                "created_by_id": "huid",
        #                "created_by_full_name": "name",
        #                "modified_by_id": "huid",
        #                "description": "description"}
        # mock_map.objects.get.return_value = stuff
        mockvalue = "title,map,latitude,longitude,description,external_url,created_by_full_name,date_created,date_modified\r\ntitle,1,24,25,description,blank,name,2015-09-12T03:26:23.222000Z,2015-09-12T03:26:23.222000Z\r\n"
        # mock_serializer = SerializerStub(stuff).map
        # print SerializerStub(stuff).map
        result = download_csv(self.request, map_id)
        # print "\n\n\n\n\n\n\n\n"
        # print result.status_code()
        self.assertTrue(status.is_success(result.status_code))
        self.assertEqual(result.content, mockvalue)

    @patch('artifact.api.MapSerializer')
    def test_marker_collection(self, mock_serializer):
        map_id = 1
        returnvalue = {"id": 1,
                       "canvas_course_id": 73,
                       "title": "title",
                       "latitude": "43",
                       "longitude": "72",
                       "zoom": 4,
                       "maptype": 1,
                       "thumbnail": "https://maps.googleapis.com/maps/api/staticmap?center=43,72&zoom=4&size=200x150&maptype=satellite",
                       "markers": [{"title": "title",
                                    "map": 1,
                                    "latitude": "24",
                                    "longitude": "25",
                                    "description": "description",
                                    "external_url": "blank",
                                    "created_by_id": "huid",
                                    "created_by_full_name": "name",
                                    "modified_by_id": "huid",
                                    "date_created": "2015-09-12T03:26:23.222000Z",
                                    "date_modified": "2015-09-12T03:26:23.222000Z"}],
                       "date_created": "2015-09-12T03:26:23.222000Z",
                       "date_modified": "2015-09-12T03:26:23.222000Z",
                       "created_by_id": "huid",
                       "created_by_full_name": "name",
                       "modified_by_id": "huid",
                       "description": "description"}
        mock_serializer.return_value = SerializerStub(returnvalue)
        result = map_location(self.request, map_id)
        self.assertTrue(status.is_success(result.status_code))
        self.assertEqual(json.loads(result.render().content), returnvalue)


class TestAPI_POST(APITestCase):

    longMessage = True

    def setUp(self):
        self.request = APIRequestFactory().post('/fake-path')
        self.request.user = Mock(name='user_mock')
        self.request.user.is_authenticated.return_value = True
        self.request.LTI = {}
        # Map.objects.create(id=1,
        #                    canvas_course_id=73,
        #                    title="title",
        #                    description="description",
        #                    latitude="43",
        #                    longitude="72",
        #                    zoom=4,
        #                    maptype=1,
        #                    created_by_id="huid",
        #                    modified_by_id="huid",
        #                    created_by_full_name="name",
        #                    date_created="2015-09-12 03:26:23.222+00",
        #                    date_modified="2015-09-12 03:26:23.222+00")
        # Markers.objects.create(id=1,
        #                        title="title",
        #                        latitude="24",
        #                        longitude="25",
        #                        description="description",
        #                        external_url="blank",
        #                        created_by_id="huid",
        #                        modified_by_id="huid",
        #                        date_created="2015-09-12 03:26:23.222+00",
        #                        date_modified="2015-09-12 03:26:23.222+00",
        #                        map_id=1,
        #                        created_by_full_name="name")

        # @patch('artifact.api.MapSerializer')
        # def test_map_collection_not_valid(self, mock_serializer):
        #     mock_serializer.return_value =
