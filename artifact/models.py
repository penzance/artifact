from django.db import models
from django.utils import timezone
from django.conf import settings


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
    latitude = models.CharField(max_length=32)
    longitude = models.CharField(max_length=32)
    zoom = models.IntegerField()
    maptype = models.IntegerField(choices=MAP_TYPE_CHOICES, default=ROADMAP)
    created_by = models.CharField(max_length=32)
    modified_by = models.CharField(max_length=32)
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
        return settings.MAP_THUMBNAIL_URL.format(latitude=self.latitude, longitude=self.longitude,
                                                 zoom=self.zoom, maptype=self.maptype)


class Markers(models.Model):

    title = models.CharField(max_length=250)
    map = models.ForeignKey(Map, related_name='markers')
    latitude = models.CharField(max_length=32)
    longitude = models.CharField(max_length=32)
    description = models.CharField(max_length=2000)
    external_url = models.CharField(max_length=250)
    created_by = models.CharField(max_length=32)
    modified_by = models.CharField(max_length=32)
    date_created = models.DateTimeField(blank=True, default=timezone.now)
    date_modified = models.DateTimeField(blank=True, default=timezone.now)

    class Meta:
        db_table = 'mp_markers'

    def __unicode__(self):
        return u'{}'.format(
            self.title
        )