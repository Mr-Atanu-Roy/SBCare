from rest_framework.serializers import ModelSerializer, ValidationError

from accounts.models import UserToken, User

class UserTokenSerializer(ModelSerializer):
    
    class Meta:
        fields = ['token', 'created_at']
        model = UserToken
        extra_kwargs = {
            'token': {'read_only': True},
            'created_at': {'read_only': True},
        }

