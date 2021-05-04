from onefin.apps.serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth.models import User


# Create your views here.
class RegistrationAPIView(viewsets.ViewSet):

    queryset = User.objects.all()
    serializer = RegistrationSerializer

    def create(self, request):
        user = request.data
        serializer = self.serializer(data=user)
             
        if serializer.is_valid():
            user_obj = serializer.save()
            token, created = Token.objects.get_or_create(user=user_obj)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED) 
        else:
            return Response({"is_success": False, "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        
