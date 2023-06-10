from datetime import datetime
from django.core.cache import cache
from rest_framework.throttling import BaseThrottle

from accounts.models import UserProfile, UserToken
from pricing.models import Pricing

class QRCodeThrottle(BaseThrottle):
    def allow_request(self, request, view):
        # Get the user id or any other identifier for the user
        user = request.user
        get_profile = UserProfile.objects.filter(user=user).first()
        get_plan = Pricing.objects.filter(plan_name=get_profile.plan).first()
        
        token = request.META.get('HTTP_AUTHORIZATION')
        if token:
            token = token.replace('Token ', '')
            get_token = UserToken.objects.filter(token=token).first()
            token_role = get_token.role
            
            if token_role.lower() == "app-use":
                qr_lim_day = get_plan.qr_day
            else:
                qr_lim_day = get_plan.api_day

            # Create a key to identify the user's daily request count
            cache_key = f'user_daily_throttle_{user}_{datetime.now().date()}'
            
            # Get the current count from cache
            request_count = cache.get(cache_key, 0)
            
            # Define the maximum number of requests allowed per day
            max_requests_per_day = qr_lim_day
            
            if request_count >= max_requests_per_day:
                return False  # Throttle the request
            
            # Increment the request count and store it in cache
            cache.set(cache_key, request_count + 1, 86400)  # 86400 seconds = 1 day
            
            return True  # Allow the request
        
        else:
            return False  # Dont allow the request
        
