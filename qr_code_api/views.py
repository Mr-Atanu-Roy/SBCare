from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from accounts.authentication import CustomTokenAuthentication

from .models import QRCode
from .throttle import QRCodeThrottle
from .serializers import QRCodeSerializer


# Create your views here.
class GetCreateQR(APIView):
    '''This api will show and create qr-codes'''
    
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [QRCodeThrottle]
    
    
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
                "message": "QR created successfully"
            }
            return Response(response, status=status.HTTP_201_CREATED)
        
        else:
            response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "data": url_serializer.data,
                "message": url_serializer.errors
            }
            
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    
class GetDeleteQR(APIView):
    '''This api will delete qr-codes'''
    
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [QRCodeThrottle]


    def get_object(self, pk, user):
        try:
            return QRCode.objects.get(pk=pk, user=user)
        except QRCode.DoesNotExist:
            raise Http404
        except Exception as e:
            print(e)
            
    
    def get(self, request, pk, format=None):
        qr_code = self.get_object(pk, request.user)

        qr_code_serializer = QRCodeSerializer(qr_code)
        
        response = {
                "status": status.HTTP_200_OK,
                "data": qr_code_serializer.data,
                "message": "data fetched successfully"
        }
        return Response(response, status=status.HTTP_200_OK)


    def delete(self, request, pk, format=None):
        qr_code = self.get_object(pk, request.user)
        qr_code.delete()
        
        response = {
                "status": status.HTTP_204_NO_CONTENT,
                "data": None,
                "message": "deleted successfully"
        }
        return Response(response, status=status.HTTP_204_NO_CONTENT)
    
    