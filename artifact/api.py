import logging

from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from artifact.models import Map, Markers
from artifact.serializers import MapSerializer, MarkersSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer
import csv
import urllib
import urllib2
import urlparse
import json

logger = logging.getLogger(__name__)

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)




@login_required
@api_view(['GET', 'POST'])
def map_collection(request, canvas_course_id):
    logger.debug('here')
    if request.method == 'GET':
        maps = Map.objects.filter(canvas_course_id=canvas_course_id)
        serializer = MapSerializer(maps, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        logged_in_user_id = request.LTI['lis_person_sourcedid']
        data = { 'canvas_course_id': canvas_course_id,
                 'title': request.data.get('title'),
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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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


@login_required
@api_view(['GET', 'POST'])
def marker_collection(request, map_id):
    logger.debug('HERE')
    if request.method == 'GET':
        maps = Markers.objects.filter(map_id=map_id)
        serializer = MarkersSerializer(maps, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        logger.debug("ASDFJKL")
        logger.debug('%s' % request.data);
        # logged_in_user_id = request.LTI['lis_person_sourcedid']
        logged_in_user_id = request.user.username
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        address = request.data.get('address')
        logger.debug(address)
        logger.debug(latitude)
        logger.debug(longitude)
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
            logger.debug("PRINT DATA")
            logger.debug(data)
            serializer = MarkersSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                logger.debug(serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif address:
            logger.debug("WENTINTOADDRESS")
            address = urllib.quote(address.encode("utf-8"))
            logger.debug(address)
            url = 'http://maps.googleapis.com/maps/api/geocode/json?address='+address+'&sensor=true'
            data = urllib2.urlopen(url).read()
            json_data = json.loads(data)
            stat = json_data.get('status')
            print
            print
            logger.debug(json_data)
            print
            print
            print '{}'.format(stat)
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
                logger.debug("PRINT DATA")
                logger.debug(data)
                serializer = MarkersSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    print '{}'.format(json.dumps({'latitude': latitude, 'longitude': longitude}))
                    return Response({'latitude': latitude, 'longitude': longitude}, status=status.HTTP_201_CREATED)
                else:
                    logger.debug(serializer.errors)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                errors = ['Address not found!']
                return JSONResponse(errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            errors = ['You did not enter either an address or lat/long. Try again.']
            return JSONResponse(errors, status=status.HTTP_400_BAD_REQUEST)


@login_required
@api_view(['GET','POST'])
def csv_points(request, map_id):
    logged_in_user_id = request.user.username
    # for i in request.data.dict().keys():
    #     logger.debug(i)
    datatouse = request.data.dict().keys()[0]
    datatouse = json.loads(datatouse)
    errors = []
    for item in datatouse:
        logger.debug(type(item))
        logger.debug(item)
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
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            #logger.debug(serializer.errors)
            #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            errors.append(serializer.errors)
    if len(errors) != 0:
        logger.debug (errors)
        return JSONResponse(errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.data, status=status.HTTP_201_CREATED)

















    # # logged_in_user_id = request.LTI['lis_person_sourcedid']
    # logged_in_user_id = request.user.username
    # data = {'title': request.data.get('title'),
    #         'map': map_id,
    #         'latitude': request.data.get('latitude'),
    #         'longitude': request.data.get('longitude'),
    #         'description': request.data.get('description'),
    #         'external_url': request.data.get('externalurl'),
    #         'fileupload': request.data.get('fileupload'),
    #         'created_by': logged_in_user_id,
    #         'modified_by': logged_in_user_id,
    #         'date_created': timezone.now(),
    #         'date_modified': timezone.now(),
    #         }
    # logger.debug("PRINT DATA")
    # logger.debug(data)
    # serializer = MarkersSerializer(data=data)
    # if serializer.is_valid():
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    # else:
    #     logger.debug(serializer.errors)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

