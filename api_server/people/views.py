from django.core import serializers
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.shortcuts import render
from oauth2_provider.decorators import protected_resource
from people.models import Directory, Medlink
from lounges.models import Lounge
import simplejson as json
from oauth2_provider.views import ProtectedResourceView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@protected_resource()
def full(request):
    result = Directory.objects.all()
    result = [{
        'username': entry.username,
        'firstname': entry.firstname,
        'lastname': entry.lastname,
        'title': entry.title,
        'room': entry.room,
        'year': str(entry.year),
        'type': entry.get_type_display(),
        'lounge': entry.lounge.description if entry.lounge else None,
    } for entry in result]
    return JsonResponse(result, safe=False)

@protected_resource()
def get_fifteen_seconds_of_frame(request):
    result = Directory.random()
    result = {
        'username': result.username,
        'firstname': result.firstname,
        'lastname': result.lastname,
        'title': result.title,
        'year': str(result.year),
        'type': result.get_type_display(),
        'homepage': result.homepage,
        'home_city': result.home_city,
        'home_state': result.home_state,
        'home_country': result.home_country,
        'quote': result.quote,
    }
    return JsonResponse(result, safe=False)

@protected_resource()
def medlinks(request):
    result = list(Medlink.objects.filter(removed=None).order_by('ordering').values_list('username', flat=True))
    return JsonResponse(result, safe=False)

@protected_resource()
def grts(request):
    _result = Directory.objects.filter(type=Directory.GRT)
    result = []
    for entry in _result:
        try:
            entry.lounge = entry.lounge
        except:
            entry.lounge = Lounge(description='None')
        result.append(entry.username)
    return JsonResponse(result, safe=False)

@protected_resource()
def me(request):
    #raise Exception(str(request.user.is_authenticated()))
    result = Directory.objects.get(username=request.user.username)

    result = {
        'username': result.username,
        'firstname': result.firstname,
        'lastname': result.lastname,
        'title': result.title,
        'room': result.room,
        'year': str(result.year),
        'type': result.get_type_display(),
        'lounge': result.lounge.description if result.lounge is not None else 'None',
        'homepage': result.homepage,
        'home_city': result.home_city,
        'home_state': result.home_state,
        'home_country': result.home_country,
        'quote': result.quote,
    }
    return JsonResponse(result, safe=False)

class Profile(ProtectedResourceView):
    def get(self, request, username):
        result = Directory.objects.get(username=username)

        result = {
            'username': result.username,
            'firstname': result.firstname,
            'lastname': result.lastname,
            'title': result.title,
            'room': result.room,
            'year': str(result.year),
            'type': result.get_type_display(),
            'lounge': result.lounge.description if result.lounge is not None else 'None',
            'cellphone': result.cellphone,
            'homepage': result.homepage,
            'home_city': result.home_city,
            'home_state': result.home_state,
            'home_country': result.home_country,
            'quote': result.quote,
            'email': result.email,
        }
        return JsonResponse(result, safe=False)

    def post(self, request, username):
        if request.user.username != username: #and not request.user.is_superuser
            raise HttpResponseForbidden('403.html')

        request.user.homepage = request.POST.get('homepage', request.user.homepage)
        request.user.cellphone = request.POST.get('cellphone', request.user.cellphone)
        request.user.home_city = request.POST.get('home_city', request.user.home_city)
        request.user.home_state = request.POST.get('home_state', request.user.home_state)
        request.user.home_country = request.POST.get('home_country', request.user.home_country)
        request.user.quote = request.POST.get('quote', request.user.quote)
        request.user.favorite_category = request.POST.get('favorite_category', request.user.favorite_category)
        request.user.favorite_value = request.POST.get('favorite_value', request.user.favorite_value)

        # if request.user.is_superuser or request.user.groups.filter(name='RAC').exists():
        #     request.user.title = request.POST.get('title', request.user.title)
        #     request.user.firstname = request.POST.get('firstname', request.user.firstname)
        #     request.user.lastname = request.POST.get('lastname', request.user.lastname)
        #     request.user.year = int(request.POST.get('year', request.user.year))
        #     request.user.room = request.POST.get('room', request.user.room)
        #     request.user.email = request.POST.get('email', request.user.email)
        request.user.save()
        return JsonResponse({'status': 'success'})

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(Profile, self).dispatch(*args, **kwargs)
