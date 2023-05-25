from rest_framework import serializers
from .models import ShortURL
from accounts.models import User


class ShortURLSerializer(serializers.ModelSerializer):
    # original_url = serializers.CharField(max_length=500)
    
    class Meta:
        model = ShortURL
        fields = ['user', 'title', 'original_url', 'short_url', 'source']
        extra_kwargs = {
            'user': {'required': False},
            'short_url': {'read_only': True}
        }
        
    def create(self, validated_data):
        user = self.context['user']
        source = validated_data.get('source')
        
        if source is not None:
            return ShortURL.objects.create(user=user, original_url=validated_data.get('original_url'), source=source)
        else:
            return ShortURL.objects.create(user=user, original_url=validated_data.get('original_url'))
            
