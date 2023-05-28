from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from accounts.authentication import CustomTokenAuthentication
from accounts.serializers import UserTokenSerializer
from accounts.models import UserToken



class GetCreateAuthToken(APIView):
    '''This api will create Auth Tokens in UserToken model'''
    authentication_classes = [BasicAuthentication, CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        tokens = UserToken.objects.filter(user=request.user)
        if tokens:
            token_serializer = UserTokenSerializer(tokens, many=True)
            response = {
                "status": status.HTTP_200_OK,
                "data": token_serializer.data,
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
        new_token = UserToken.objects.create(user=request.user)
        if new_token:
            response = {
                'token': str(new_token),
                'error': None
            }
        else:
            response = {
                'token': None,
                'error': "Failed to generate token"
            }
            
        return Response(response)