from rest_framework.serializers import ModelSerializer, ValidationError

from accounts.models import UserToken, User

class UserTokenSerializer(ModelSerializer):
    
    class Meta:
        fields = ['id', 'token', 'created_at']
        model = UserToken
        extra_kwargs = {
            'id': {'read_only': True},
            'token': {'read_only': True},
            'created_at': {'read_only': True},
        }

