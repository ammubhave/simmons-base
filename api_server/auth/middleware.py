from django.contrib.auth.middleware import RemoteUserMiddleware

class SimmonsAuthMiddleware(RemoteUserMiddleware):
    header = "SSL_CLIENT_S_DN_Email"
