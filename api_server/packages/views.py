from django.shortcuts import render

# Create your views here.
from django.core import serializers
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.shortcuts import render
from oauth2_provider.decorators import protected_resource
from packages.models import Package
import simplejson as json
from oauth2_provider.views import ProtectedResourceView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


class PackageNotify(ProtectedResourceView):
    def get(self, request):
        result = Package.objects.filter(recipient=request.user.username, pickup=None).order_by('checkin')
        result = {
            'count': len(result),
            'oldest_since': result[0].checkin if len(result) > 0 else 0,
        }
        return JsonResponse(result, safe=False)

    # def post(self, request, username):
    #     if request.user.username != username: #and not request.user.is_superuser
    #         raise HttpResponseForbidden('403.html')

    #     request.user.homepage = request.POST.get('homepage', request.user.homepage)
    #     request.user.cellphone = request.POST.get('cellphone', request.user.cellphone)
    #     request.user.home_city = request.POST.get('home_city', request.user.home_city)
    #     request.user.home_state = request.POST.get('home_state', request.user.home_state)
    #     request.user.home_country = request.POST.get('home_country', request.user.home_country)
    #     request.user.quote = request.POST.get('quote', request.user.quote)
    #     request.user.favorite_category = request.POST.get('favorite_category', request.user.favorite_category)
    #     request.user.favorite_value = request.POST.get('favorite_value', request.user.favorite_value)

    #     # if request.user.is_superuser or request.user.groups.filter(name='RAC').exists():
    #     #     request.user.title = request.POST.get('title', request.user.title)
    #     #     request.user.firstname = request.POST.get('firstname', request.user.firstname)
    #     #     request.user.lastname = request.POST.get('lastname', request.user.lastname)
    #     #     request.user.year = int(request.POST.get('year', request.user.year))
    #     #     request.user.room = request.POST.get('room', request.user.room)
    #     #     request.user.email = request.POST.get('email', request.user.email)
    #     request.user.save()
    #     return JsonResponse({'status': 'success'})

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(PackageNotify, self).dispatch(*args, **kwargs)
