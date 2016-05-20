from django.conf.urls import url, include
from artifact import views, api


urlpatterns = [

    url(r'^map_index$', views.map_index, name='map_index'),
    url(r'^location/(?P<map_id>\d+)$', views.location, name='location'),
    url(r'^docs/', include('rest_framework_swagger.urls')),

    url(r'^api/v1/maps/(?P<canvas_course_id>\d+)$', api.map_collection, name='maps'),
    url(r'^api/v1/markers/(?P<map_id>\d+)$', api.marker_collection, name='markers'),
    url(r'^api/v1/updatePoint/(?P<point_id>\d+)$', api.updatePoint, name='updatePoint'),
    url(r'^api/v1/location/(?P<map_id>\d+)$', api.map_location, name='map_location'),
    url(r'^api/v1/csvpoints/(?P<map_id>\d+)$', api.csv_points, name='csv_points'),    
    url(r'^api/v1/downloadcsv/(?P<map_id>\d+)$', api.download_csv, name='download_csv'),
]


