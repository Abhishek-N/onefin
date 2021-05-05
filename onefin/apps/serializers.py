from django.contrib.auth.models import User
from django.db import models
from rest_framework.authtoken.models import Token
from rest_framework import serializers

class RegistrationSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = User
        fields = ["username", "password"]

    def create(self, validated_data):
        # Use the `create_user` method we wrote earlier to create a new user.
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data.get('password'))
        return user
       