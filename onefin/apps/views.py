from onefin.apps.serializers import RegistrationSerializer
from django.contrib.auth import authenticate
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
        cur_user = authenticate(request=request, username=user.get('username'), password=user.get('password'))
        if not cur_user:
            serializer = self.serializer(data=user)
            if serializer.is_valid():
                user_obj = serializer.save()
                token, created = Token.objects.get_or_create(user=user_obj)
                return Response({'token': token.key}, status=status.HTTP_201_CREATED)
            else:
                return Response({"is_success": False, "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            token, created = Token.objects.get_or_create(user=cur_user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        