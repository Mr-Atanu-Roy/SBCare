from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from accounts.models import UserToken

class CustomTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Retrieve the token from the request headers or other sources
        token = request.META.get('HTTP_AUTHORIZATION')
        
        if token:
            token = token.replace('Token ', '')

            # Lookup the UserToken model for the given token
            try:
                user_token = UserToken.objects.get(token=token)
                user = user_token.user
                return (user, None)
            except UserToken.DoesNotExist:
                raise AuthenticationFailed('Invalid token')
        
        return None  # No token provided, return None for authentication failure
    
    