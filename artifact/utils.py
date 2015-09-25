import json

from django.http import HttpResponse
from django.shortcuts import render
from django.utils.safestring import mark_safe


def create_json_200_response(data={'message': 'success'}):
    return HttpResponse(
        json.dumps(data),
        status=200,
        content_type='application/json'
    )


def create_json_500_response(message):
    return HttpResponse(
        json.dumps({'error': message}),
        status=500,
        content_type='application/json'
    )


def create_context_error_response(request, message='', template=None):
    """
    This method helps in error handling and is used by the validation
    methods. It returns an HttpResponse if the request is via AJAX otherwise
    renders the given error template.
    """
    message = "It looks like you have been working on multiple Canvas sites. %s" % message
    if request.is_ajax():
        return HttpResponse(json.dumps({'error': message}), content_type="application/json", status=400)
    else:
        if template:
            return render(request, template, {'message': mark_safe(message)})
        else:
            return HttpResponse(
                "<html><head></head><body>%s</body></html>" % message,
                content_type="text/html",
                status=400
            )

