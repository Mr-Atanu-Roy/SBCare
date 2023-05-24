from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.conf import settings

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import ShortURL
from .serializers import ShortURLSerializer

# Create your views here.
        
class GetCreateShortURL(APIView):
    '''This api will show and create urls'''
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        short_urls = ShortURL.objects.filter(user=request.user)
        if short_urls:
            url_serializer = ShortURLSerializer(short_urls, many=True)
                
            response = {
                "status": status.HTTP_200_OK,
                "data": url_serializer.data,
                "message": "data fetched successfully"
            }
        else:
            response = {
                "status": status.HTTP_200_OK,
                "data": None,
                "message": "no records"
            }
        
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request, format=None):
        url_serializer = ShortURLSerializer(data=request.data, context={'user': request.user})
        
        if url_serializer.is_valid():
            newURL = url_serializer.save()

            response = {
                "status": status.HTTP_201_CREATED,
                "data": url_serializer.data,
                "message": "URL created successfully"
            }
            return Response(response, status=status.HTTP_201_CREATED)
        
        else:
            response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "data": url_serializer.data,
                "message": url_serializer.errors
            }
            
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
            

class GetUpdateDeleteShortURL(APIView):
    '''This api will show, update, delete a perticular shorturl model instance'''
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk, user):
        try:
            return ShortURL.objects.get(pk=pk, user=user)
        except ShortURL.DoesNotExist:
            raise Http404
        except Exception as e:
            print(e)
    
    def get(self, request, pk, format=None):
        short_url = self.get_object(pk, request.user)

        url_serializer = ShortURLSerializer(short_url)
        
        response = {
                "status": status.HTTP_200_OK,
                "data": url_serializer.data,
                "message": "data fetched successfully"
        }
        return Response(response, status=status.HTTP_200_OK)
    
    
    def put(self, request, pk, format=None):
        short_url = self.get_object(pk, request.user)
        
        url_serializer = ShortURLSerializer(short_url, data=request.data, partial=True)
        
        if url_serializer.is_valid():
            url_serializer.save()
            response = {
                "status": status.HTTP_202_ACCEPTED,
                "data": url_serializer.data,
                "message": "data updated successfully"
            }
            return Response(response, status=status.HTTP_202_ACCEPTED)
    
    
    def delete(self, request, pk, format=None):
        short_url = self.get_object(pk, request.user)
        short_url.delete()
        
        response = {
                "status": status.HTTP_204_NO_CONTENT,
                "data": None,
                "message": "deleted successfully"
        }
        return Response(response, status=status.HTTP_204_NO_CONTENT)
        
    

def redirect_link(request, token):
    '''Responsible for redirecting page to original url'''
    
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
    
    

