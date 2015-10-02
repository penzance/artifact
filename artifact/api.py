import logging

from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponse

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from artifact.models import Map, Markers
from artifact.serializers import MapSerializer, MarkersSerializer

logger = logging.getLogger(__name__)


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
    if request.method == 'GET':
        maps = Markers.objects.filter(map_id=map_id)
        serializer = MarkersSerializer(maps, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        logged_in_user_id = request.LTI['lis_person_sourcedid']
        data = {'title': request.data.get('title'),
                'map': map_id,
                'latitude': request.data.get('latitude'),
                'longitude': request.data.get('longitude'),
                'description': request.data.get('description'),
                'external_url': request.data.get('external_url'),
                'date_modified': timezone.now(),
                'created_by': logged_in_user_id,
                'modified_by': logged_in_user_id,
                }
        serializer = MapSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
