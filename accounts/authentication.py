from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from accounts.models import UserToken, UserProfile
from accounts.utils import current_time

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
                try:
                    user_profile = UserProfile.objects.get(user=user, api_access=True)
                    if user_profile:
                        if user_profile.plan_expires < current_time:
                        # if user_profile.plan_expires > current_time:
                            if request.method == "POST" or request.method == "PUT" or request.method == "PATCH":
                                raise AuthenticationFailed('Your Plan has expired. Please renew it')
                            else:
                                return (user, None)
                        else:
                            return (user, None)
                            
                    
                except UserProfile.DoesNotExist:
                    raise AuthenticationFailed('Invalid token. User with this token is not allowed to access API')
                    
            except UserToken.DoesNotExist:
                raise AuthenticationFailed('Invalid token')
        
        return None  # No token provided, return None for authentication failure
    
    