from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from guestlist.models import Guestlist
from people.models import Directory, Officer

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def my_profile(request):
    msg = None
    if request.method == 'POST':
        if request.POST['action'] == 'removeguest':
            guest = Guestlist.objects.get(username=request.user.username, guestlistid=request.POST['guestlistid'])
            guest.current = False
            guest.save()
            msg = ('success', 'Guest removed')
        elif request.POST['action'] == 'addguest':
            if len(Guestlist.objects.filter(username=request.user.username, guest=request.POST['name'])) > 0:
                msg = ('danger', 'Guest already exists')
            else:
                count = len(Guestlist.objects.filter(username=request.user.username))
                if count >= 25:
                    msg = ('danger', 'You sure have a lot of friends.  Unfortunately, 25 is the max for your Guest List.')
                else:
                    now = datetime.now()
                    exp = None
                    if request.profile.guest_list_expiration == 'year':
                        exp = datetime(now.year, 6, 10)
                        if exp < now:
                            exp = datetime(now.year + 1, 6, 10)
                    else:
                        if now.month == 12:
                            exp = datetime(now.year + 1, 1, 1)
                        else:
                            exp = datetime(now.year, now.month + 1, 1)

                    Guestlist.objects.create(username=request.profile, guest=request.POST['name'], date_invalid=exp)
                    msg = ('success', 'Guest added successfully')
        elif request.POST['action'] == 'saveprofile':
            profile = request.profile
            profile.cellphone = request.POST['cellphone']
            profile.homepage = request.POST['homepage']
            profile.home_city = request.POST['home_city']
            profile.home_state = request.POST['home_state']
            profile.home_country = request.POST['home_country']
            profile.quote = request.POST['quote']
            profile.favorite_category = request.POST['favorite_category']
            profile.favorite_value = request.POST['favorite_value']
            profile.save()
            msg = ('success', 'Your profile was saved successfully.')
    return render(request, 'my_profile.html', {'guestlist': Guestlist.objects.filter(username=request.user.username).order_by('guest'), 'msg': msg})

@login_required
def view_profile(request, username):
    profile = Directory.objects.get(username=username)
    return render(request, 'view_profile.html', {'profile': profile})


@login_required
def officers(request):
    positions = zip(Officer.objects.order_by('ordering').values_list('position', flat=True),
        Officer.objects.order_by('ordering').values_list('position_text', flat=True))
    def getUniqueItems(iterable):
        result = []
        for item in iterable:
            if item not in result:
                result.append(item)
        return result
    positions = getUniqueItems(positions)
    all_officers = [{'position': position[0], 'position_text': position[1], 'officers': [officer.username for officer in Officer.objects.filter(position=str(position[0])).order_by('ordering')]} for position in positions]
    all_officers.insert(0, {
        'position': 'housemaster',
        'position_text': 'Housemaster',
        'officers': [
            {'firstname': 'John'},
            {'firstname': 'Ellen'}
        ]
    })
    all_officers.insert(1, {
        'position': 'associate_housemaster',
        'position_text': 'Assc. HM',
        'officers': [
            {'username': 'srhall', 'firstname': 'Steve'}
        ]
    })
    all_officers.insert(2, {'position': 'blank'});
    all_officers.insert(7, {'position': 'blank'});
    all_officers.insert(8, {
        'position': 'house_manager',
        'position_text': 'House Mgr.',
        'officers': [
            {'username': 'nika_h', 'firstname': 'Nika'}
        ]
    })
    all_officers.insert(9, {'position': 'blank'});
    all_officers.insert(10, {
        'position': 'rlad',
        'position_text': 'Area Director',
        'officers': [
            {'username': 'jogon_1', 'firstname': 'Josh'}
        ]
    })
    all_officers.insert(11, {'position': 'blank'});
    all_officers.insert(12, {'position': 'blank'});
    all_officers.insert(18, {'position': 'blank'});
    all_officers.insert(20, {'position': 'blank'});
    all_officers.insert(21, {'position': 'blank'});
    all_officers.insert(26, {'position': 'blank'});
    all_officers.insert(27, {'position': 'blank'});
    all_officers.insert(29, {'position': 'blank'});
    all_officers.insert(30, {'position': 'blank'});
    all_officers.insert(31, {'position': 'blank'});
    all_officers.insert(32, {'position': 'blank'});
    all_officers.insert(33, {'position': 'blank'});
    return render(request, 'officers.html', {'all_officers': all_officers})

@login_required
def govtracker_home(request):
    return render(request, 'govtracker_home.html')

def messenger_callback(request):
    if request.REQUEST['hub.verify_token'] == 'MmLq7XgaE2cQKmRQmgfxDQBU':
        return HttpResponse(request.REQUEST['hub.challenge'])
    else:
        return HttpResponse('Error, wrong validation token');
