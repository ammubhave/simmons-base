from django.conf import settings
from django.contrib.auth.backends import RemoteUserBackend
from auth.models import SdbUser as User
import logging

class SimmonsAuthBackend(RemoteUserBackend):
    def clean_username(self, username):
        if '@' in username:
            name, domain = username.split('@')
            assert domain.upper() == 'MIT.EDU'
            return name
        else:
            return username

    def authenticate(self, remote_user=None):
       # raise Exception(remote_user)
        logging.info('authenticate(' + remote_user + ')')
        try:
            user = User.objects.get(username=remote_user, is_active=True)
            return user
        except User.DoesNotExist:
            pass
        return None

    def get_user(self, user_id):
        logging.info('get_user(' + str(user_id) + ')')
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
