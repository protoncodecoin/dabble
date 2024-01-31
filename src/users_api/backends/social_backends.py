from urllib.parse import urlencode
from social_core.backends.oauth import BaseOAuth2


class FacebookOAuth2(BaseOAuth2):
    """Facebook OAuth authentication backend"""
    name = 'facebook'
    AUTHORIZATION_URL = 'https://www.facebook.com/dialog/oauth'
    ACCESS_TOKEN_URL = 'https://graph.facebook.com/v12.0/oauth/access_token'
    ACCESS_TOKEN_METHOD = 'GET'
    SCOPE_SEPARATOR = ','
    EXTRA_DATA = [
        ('id', 'id'),
        ('expires', 'expires')
    ]

    def get_user_details(self, response):
        """Return user details from Facebook account"""
        data = {
            'username': response.get('name'),
            'email': response.get('email') or "",
            'first_name': response.get('first_name'),
            'last_name': response.get('last_name'),
        }
        print(data, "============================")
        return data

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        url = 'https://graph.facebook.com/v12.0/me?' + urlencode({
            'access_token': access_token,
            'fields': 'id,name,email,first_name,last_name',
        })
        
        return self.get_json(url)
