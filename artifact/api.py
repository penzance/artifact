from artifact.serializers import MapSerializer, MarkersSerializer
from artifact.models import Map, Markers

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.utils import timezone

from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status

import urlparse
import urllib2
import logging
import urllib
import json
import csv

logger = logging.getLogger(__name__)

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


# Loads/saves map views from the landing page
@login_required
@api_view(['GET', 'POST'])
def map_collection(request, canvas_course_id):

    if request.method == 'GET':

        maps = Map.objects.filter(canvas_course_id=canvas_course_id)
        serializer = MapSerializer(maps, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        logged_in_user_id = request.LTI['lis_person_sourcedid']
        data = { 'canvas_course_id': canvas_course_id,
                 'title': request.data.get('title'),
                 'description': request.data.get('description'),
                 'latitude': request.data.get('latitude'),
                 'longitude': request.data.get('longitude'),
                 'zoom': int(request.data.get('zoom')),
                 'maptype': int(request.data.get('maptype')),
                 'date_modified': timezone.now(),
                 'created_by': logged_in_user_id,
                 'modified_by': logged_in_user_id,
                 }

        serializer = MapSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Get the map that is selected
@login_required
@api_view(['GET'])
def map_location(request, map_id):
    try:
        map = Map.objects.get(pk=map_id)
    except Map.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MapSerializer(map)
        return Response(serializer.data)

# Get the map that is selected
@login_required
@api_view(['GET'])
def download_csv(request, map_id):
    try:
        map = Map.objects.get(pk=map_id)
    except Map.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MapSerializer(map)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="downloaded_points.csv"'
        fieldnames = ['title', 'map', 'latitude', 'longitude', 'description', 'external_url', 
            'created_by', 'modified_by', 'date_created', 'date_modified']
        writer = csv.DictWriter(response, fieldnames=fieldnames)
        writer.writeheader()
        for dictionary in serializer.data['markers']:
            writer.writerow(dictionary)
        return response

# Generate the points for the selected map and process single point upload
@login_required
@api_view(['GET', 'POST'])
def marker_collection(request, map_id):

    if request.method == 'GET':

        maps = Markers.objects.filter(map_id=map_id)
        serializer = MarkersSerializer(maps, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        logged_in_user_id = request.user.username
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        address = request.data.get('address')

        # lat/long points take precedence over addresses
        if latitude is not None and longitude is not None:
            data = {'title': request.data.get('title'),
                    'map': map_id,
                    'latitude': request.data.get('latitude'),
                    'longitude': request.data.get('longitude'),
                    'description': request.data.get('description'),
                    'external_url': request.data.get('externalurl'),
                    'fileupload': request.data.get('fileupload'),
                    'created_by': logged_in_user_id,
                    'modified_by': logged_in_user_id,
                    'date_created': timezone.now(),
                    'date_modified': timezone.now(),
                    }

            serializer = MarkersSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif address:
            address = urllib.quote(address.encode("utf-8"))
            url = 'http://maps.googleapis.com/maps/api/geocode/json?address='+address+'&sensor=true'
            data = urllib2.urlopen(url).read()
            json_data = json.loads(data)
            stat = json_data.get('status')

            if stat in 'OK':
                result = json_data['results'][0]         
                latitude = result['geometry']['location']['lat']
                longitude = result['geometry']['location']['lng']
                
                data = {'title': request.data.get('title'),
                        'map': map_id,
                        'latitude': latitude,
                        'longitude': longitude,
                        'description': request.data.get('description'),
                        'external_url': request.data.get('externalurl'),
                        'fileupload': request.data.get('fileupload'),
                        'created_by': logged_in_user_id,
                        'modified_by': logged_in_user_id,
                        'date_created': timezone.now(),
                        'date_modified': timezone.now(),
                        }

                serializer = MarkersSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'latitude': latitude, 'longitude': longitude}, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            else:
                errors = ['Address not found!']
                return JSONResponse(errors, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            errors = ['You did not enter either an address or lat/long. Try again.']
            return JSONResponse(errors, status=status.HTTP_400_BAD_REQUEST)


# Uploading multiple points via CSV file
@login_required
@api_view(['POST'])
def csv_points(request, map_id):
    if request.method == 'POST':
        logged_in_user_id = request.user.username
        datatouse = request.data.dict().keys()[0]
        datatouse = json.loads(datatouse)
        errors = []
        for item in datatouse:
            data = {'title': item[u'title'],
                    'map': map_id,
                    'latitude': item[u'latitude'],
                    'longitude': item[u'longitude'],
                    'description': item[u'description'],
                    'external_url': item[u'externalurl'],
                    'created_by': logged_in_user_id,
                    'modified_by': logged_in_user_id,
                    'date_created': timezone.now(),
                    'date_modified': timezone.now(),
                    }

            serializer = MarkersSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            else:
                errors.append(serializer.errors)
        if len(errors) != 0:
            return JSONResponse(errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.data, status=status.HTTP_201_CREATED)