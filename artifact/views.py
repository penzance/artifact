import logging

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import render

logger = logging.getLogger(__name__)


@login_required
@require_http_methods(['GET'])
def map_index(request):
    logger.debug('******** MapList ********')
    for k,v in request.LTI.items():
        logger.debug('%s : %s' % (k,v))
    logger.debug('******** EndMapList ********')
    canvas_course_id = request.LTI.get('custom_canvas_course_id')
    return render(request, 'artifact/map_index.html', {'canvas_course_id': canvas_course_id})


@login_required
@require_http_methods(['GET'])
def location(request, map_id):
    logger.debug('******** Location ********')
    for k,v in request.LTI.items():
        logger.debug('%s : %s' % (k,v))
    logger.debug('******** EndLocation ********')
    return render(request, 'artifact/location.html', {'map_id': map_id})



