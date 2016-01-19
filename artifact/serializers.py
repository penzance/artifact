from rest_framework import serializers
from artifact.models import Map, Markers


class MarkersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Markers
        fields = ('title', 'map', 'latitude', 'longitude', 'description', 'external_url', 'created_by_id', 'created_by_full_name', 'modified_by_id',
        	'date_created', 'date_modified')


class MapSerializer(serializers.ModelSerializer):
    markers = MarkersSerializer(many=True, read_only=True)

    class Meta:
        model = Map
        fields = ('id', 'canvas_course_id', 'title', 'latitude', 'longitude', 'zoom', 'maptype', 'thumbnail', 'markers',
                  'date_created', 'date_modified', 'created_by_id', 'created_by_full_name', 'modified_by_id', 'description')



