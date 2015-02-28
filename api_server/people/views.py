from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from oauth2_provider.decorators import protected_resource
from people.models import Directory
import simplejson as json

@protected_resource()
def full(request):
    result = Directory.objects.using('sdb').all()
    result = [{
        'username': entry.username,
        'firstname': entry.firstname,
        'lastname': entry.lastname,
        'title': entry.title,
        'room': entry.room,
        'year': str(entry.year),
    } for entry in result]
    return HttpResponse(json.dumps(result), content_type='text/javascript')
