from django.http import Http404

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
        tokens = UserToken.objects.filter(user=request.user, role="api-use")
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
        no_tokens = UserToken.objects.filter(user=request.user, role="api-use")
        if len(no_tokens) <= 10:
        
            new_token = UserToken.objects.create(user=request.user)
            if new_token:
                response = {
                    'token': str(new_token),
                    'error': None
                }
                return Response(response, status=status.HTTP_201_CREATED)
            else:
                response = {
                    'token': None,
                    'error': "Failed to generate token"
                }
                
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = {
                'token': None,
                'error': "Token creation limit is 10. Delete a token to create more"
            }
            
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        
class DeleteAuthToken(APIView):
    '''This api view is responsible for deleting a particular auth token'''
    
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk, user):
        try:
            return UserToken.objects.get(pk=pk, user=user)
        except UserToken.DoesNotExist:
            raise Http404
        except Exception as e:
            print(e)
            
    def delete(self, request, pk, format=None):
        token = self.get_object(pk, request.user)
        token.delete()
        
        response = {
                "status": status.HTTP_204_NO_CONTENT,
                "data": None,
                "message": "deleted successfully"
        }
        return Response(response, status=status.HTTP_204_NO_CONTENT)
        
    
    