import requests
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from onefin.apps.models import Collections
from onefin.apps.serializers import (CollectionSerialzer,
                                     RegistrationSerializer)
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.mixins import UpdateModelMixin


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
        page = "?page=" + \
            request.GET.get('page') if request.GET.get('page') else ''
        cur_url = reverse('api:movie_api', request=request)
        response = requests.get('https://demo.credy.in/api/v1/maya/movies/' +
                                page,
                                auth=(settings.API_USERNAME,
                                      settings.API_PASSWORD)
                                )
        response_obj = response.json()
        response_obj['next'] = response_obj['next'].replace(
            'https://demo.credy.in/api/v1/maya/movies/', cur_url) \
            if 'next' in response_obj and response_obj['next'] \
            else None
        response_obj['previous'] = response_obj['previous'].replace(
            'https://demo.credy.in/api/v1/maya/movies/', cur_url) \
            if 'previous' in response_obj and response_obj['previous'] \
            else None
        return Response(response_obj)


class CollectionsViewSet(viewsets.GenericViewSet, UpdateModelMixin):

    permission_classes = [IsAuthenticated]
    serializer = CollectionSerialzer
    queryset = Collections.objects.all()

    def create(self, request):
        collection = self.serializer(data=request.data)
        collection.is_valid(raise_exception=True)
        created_collection = collection.save(user=request.user)

        return Response({'collection_uuid': created_collection.uuid})

    def update(self, request,  *args, **kwargs):
        try:
            collection = self.get_object()
            data_to_update = request.data
            if collection.user == request.user:
                updated_collection = self.serializer(
                    collection, data=data_to_update, partial=True)
                updated_collection.is_valid(raise_exception=True)
                updated_collection.save()
                return Response(updated_collection.data,
                                status=status.HTTP_202_ACCEPTED)
            else:
                raise Exception('Unauthorised')
        except Exception as e:
            return Response({'is_success': False, 'error': e.args[0]},
                            status=status.HTTP_400_BAD_REQUEST)


# class CollectionAPIView(APIView):

#     permission_classes = [IsAuthenticated]
#     serializer = CollectionListSerialzer

#     def get(self, request):
#         try:
#             collection_id = request.query_params.get('collection_id')
#         except Exception as e:
#             return Response({'sts': False, 'msg': 'Collection doesn\'t \
#                             'code': str(e.args[0])})
#         collection = CollectionListSerialzer(data=request.data)
#         collection.is_valid(raise_exception=True)
#         collection_data = collection.save(user=request.user)

#         return Response(collection_data)
