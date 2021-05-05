import requests
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from onefin.apps.serializers import RegistrationSerializer
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.
class RegistrationAPIViewset(viewsets.ViewSet):

    queryset = User.objects.all()
    serializer = RegistrationSerializer

    def create(self, request):
        user = request.data
        cur_user = authenticate(request=request, username=user.get(
            'username'), password=user.get('password'))
        if not cur_user:
            serializer = self.serializer(data=user)
            if serializer.is_valid():
                user_obj = serializer.save()
                token, created = Token.objects.get_or_create(user=user_obj)
                return Response(
                    {'token': token.key},
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {"is_success": False, "error": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            token, created = Token.objects.get_or_create(user=cur_user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)


class MovieAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        breakpoint()
        movies = requests.get('https://demo.credy.in/api/v1/maya/movies/',
                              auth=(settings.API_USERNAME,
                                    settings.API_PASSWORD)
                              )
        return Response({"response": movies})
