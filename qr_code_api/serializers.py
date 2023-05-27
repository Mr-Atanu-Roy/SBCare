from rest_framework import serializers
from .models import QRCode


class QRCodeSerializer(serializers.ModelSerializer):
    # original_url = serializers.CharField(max_length=500)
    
    class Meta:
        model = QRCode
        exclude = ['user', 'updated_at']
        extra_kwargs = {
            'id': {'read_only': True},
            'qr_code': {'read_only': True}
        }
        
    
    def validate(self, data):
        type = data.get("type", "url")
        
        if type=="url":
            if not data.get("url"):
                raise serializers.ValidationError("url field is required for type url")
            
        elif type=="me-card":
            if (not data.get("name")) or (not data.get("email")) or (not data.get("phone")):
                raise serializers.ValidationError("name, email, Phone field is required for type me-card")
            
        elif type=="wifi":
            if (not data.get("ssid")) or (not data.get("password")) or (not data.get("security")):
                raise serializers.ValidationError("ssid, password, security field is required for type wifi")
        
        return data
    
        
    def create(self, validated_data):
        user = self.context['user']
        source = validated_data.get('source')

        if source is not None:
            del validated_data["source"]
            return QRCode.objects.create(user=user, source=source, **validated_data)
        else:
            return QRCode.objects.create(user=user, **validated_data)
        
        
            
