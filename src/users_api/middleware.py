from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


class SetCookiesMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Set the access and refresh tokens as cookies
            access_token = str(AccessToken.for_user(request.user))
            refresh_token = str(RefreshToken.for_user(request.user))
            response.set_cookie("access_token", access_token, httponly=True)
            response.set_cookie("refresh_token", refresh_token, httponly=True)
        return response
