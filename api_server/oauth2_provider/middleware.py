from django.contrib.auth import authenticate, login


class OAuth2TokenMiddleware(object):
    """
    Middleware for OAuth2 user authentication

    This middleware is able to work along with AuthenticationMiddleware and its behaviour depends
    on the order it's processed with.

    If it comes *after* AuthenticationMiddleware and request.user is valid, leave it as is and does
    not proceed with token validation. If request.user is the Anonymous user proceeds and try to
    authenticate the user using the OAuth2 access token.

    If it comes *before* AuthenticationMiddleware, or AuthenticationMiddleware is not used at all,
    tries to authenticate user with the OAuth2 access token and set request.user field. Setting
    also request._cached_user field makes AuthenticationMiddleware use that instead of the one from
    the session.
    """
    def process_request(self, request):
        # do something only if request contains a Bearer token
        if request.META.get('REDIRECT_HTTP_AUTHORIZATION', '').startswith('Bearer') or request.META.get('HTTP_AUTHORIZATION', '').startswith('Bearer'):
            #raise Exception(request)
            if not hasattr(request, 'user') or request.user.is_anonymous():
                user = authenticate(request=request)
                if user:
                    request.user = request._cached_user = user
                    #login(request, user)
