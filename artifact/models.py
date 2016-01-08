from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core import files


class Map(models.Model):

    SATELLITE = 1
    ROADMAP = 2
    HYBRID = 3
    TERRAIN = 4

    MAP_TYPE_CHOICES = (
        (SATELLITE, 'SATELLITE'),
        (ROADMAP, 'ROADMAP'),
        (HYBRID, 'HYBRID'),
        (TERRAIN, 'TERRAIN'),
    )

    canvas_course_id = models.IntegerField()
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=500)
    latitude = models.CharField(max_length=32)
    longitude = models.CharField(max_length=32)
    zoom = models.IntegerField()
    maptype = models.IntegerField(choices=MAP_TYPE_CHOICES, default=ROADMAP)
    created_by_id = models.CharField(max_length=32)
    modified_by_id = models.CharField(max_length=32)
    created_by_full_name = models.CharField(max_length=32)
    date_created = models.DateTimeField(blank=True, default=timezone.now)
    date_modified = models.DateTimeField(blank=True, default=timezone.now)

    class Meta:
        db_table = 'mp_maps'

    def __unicode__(self):
        return u'{}'.format(
            self.title
        )

    @property
    def thumbnail(self):
        if self.maptype == 1:
            map_type = 'satellite'
        elif self.maptype == 2:
            map_type = 'roadmap'
        elif self.maptype == 3:
            map_type = 'hybrid'
        elif self.maptype == 4:
            map_type = 'terrain'
        return settings.MAP_THUMBNAIL_URL.format(latitude=self.latitude, longitude=self.longitude,
                                                 zoom=self.zoom, maptype=map_type)


class Markers(models.Model):
    title = models.CharField(max_length=250)
    map = models.ForeignKey(Map, related_name='markers')
    latitude = models.CharField(max_length=32)
    longitude = models.CharField(max_length=32)
    description = models.CharField(max_length=2000)
    external_url = models.CharField(max_length=250, default="")
    created_by_id = models.CharField(max_length=32)
    modified_by_id = models.CharField(max_length=32)
    created_by_full_name = models.CharField(max_length=32)
    date_created = models.DateTimeField(blank=True, default=timezone.now)
    date_modified = models.DateTimeField(blank=True, default=timezone.now)

    class Meta:
        db_table = 'mp_markers'

    def __unicode__(self):
        return u'{}'.format(
            self.title
        )