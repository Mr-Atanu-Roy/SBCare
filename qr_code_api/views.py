from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.conf import settings

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import QRCode
from .serializers import QRCodeSerializer

# Create your views here.
class GetCreateQR(APIView):
    '''This api will show and create qr-codes'''
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    
    def get(self, request, format=None):
        qr = QRCode.objects.filter(user=request.user)
        if qr:
            qr_serializer = QRCodeSerializer(qr, many=True)
                
            response = {
                "status": status.HTTP_200_OK,
                "data": qr_serializer.data,
                "message": "data fetched successfully"
            }
        else:
            response = {
                "status": status.HTTP_200_OK,
                "data": None,
                "message": "no records"
            }
        
        return Response(response, status=status.HTTP_200_OK)
    
    
    def post(self, request, format=None):
        url_serializer = QRCodeSerializer(data=request.data, context={'user': request.user})
        
        if url_serializer.is_valid():
            newQR = url_serializer.save()

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
    
    
    
    
    