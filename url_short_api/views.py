from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication

from .models import ShortURL
from .serializers import ShortURLSerializer

# Create your views here.

class CreateShortURL(APIView):
    permission_classes = [TokenAuthentication]
    
    def post(self, request, format=None):
        create_url_serializer = ShortURLSerializer(data=request.data, context={'user': request.user})
        
        if create_url_serializer.is_valid():
            newURL = create_url_serializer.save()

            response = {
                "status": status.HTTP_201_CREATED,
                "data": create_url_serializer.data,
                "message": "URL created successfully"
            }
            return Response(response, status=status.HTTP_201_CREATED)
        
        else:
            response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "data": create_url_serializer.data,
                "message": create_url_serializer.errors
            }
            
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
            


def redirect_link(request, token):
    try:
        short_url = settings.BASE_URL+f"r/{token}"
        get_url = ShortURL.objects.filter(short_url=short_url)
        if get_url:
            return redirect(get_url[0].original_url)
        else:
            return HttpResponse("INVALID URL")
    except Exception as e:
        print(e)
        return HttpResponse("SOMETHING WENT WRONG")
    
    

