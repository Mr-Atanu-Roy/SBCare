from rest_framework import serializers
from .models import ShortURL
from accounts.models import User


class ShortURLSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ShortURL
        fields = ['id', 'title', 'original_url', 'short_url', 'source', 'created_at']
        extra_kwargs = {
            'id': {'read_only': True},
            'short_url': {'read_only': True},
            'created_at': {'read_only': True},
        }
        
    def create(self, validated_data):
        user = self.context['user']
        source = validated_data.get('source')
        
        if source is not None:
            return ShortURL.objects.create(user=user, original_url=validated_data.get('original_url'), source=source, title=validated_data.get('title'))
        else:
            return ShortURL.objects.create(user=user, original_url=validated_data.get('original_url'), title=validated_data.get('title'))
            
