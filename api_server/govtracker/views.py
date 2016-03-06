from django.core import serializers
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.shortcuts import render
from oauth2_provider.decorators import protected_resource
from people.models import Directory
import simplejson as json
from oauth2_provider.views import ProtectedResourceView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@protected_resource()
def housemeetings(request):
    raise Exception(str(request.user.is_authenticated()))

