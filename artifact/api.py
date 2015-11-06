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

@login_required
@api_view(['GET','POST'])
def csv_points(request, map_id):
    requeststring = request.data[u' filename'].splitlines()
    logged_in_user_id = request.user.username
    errors = []
    for row in requeststring[4:-1]:
        items = row.split(",")
        data = {'title': items[0],
                'map': map_id,
                'latitude': items[2],
                'longitude': items[3],
                'description': items[1],
                'external_url': items[4],
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

