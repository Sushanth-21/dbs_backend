from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','is_staff','first_name','last_name']


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password','is_staff','first_name','last_name']

    def create(self, validated_data):
        hashed_pass = make_password(validated_data['password'])
        print(validated_data)
        user = User.objects.create(
            username=validated_data['username'], password=hashed_pass,is_staff=validated_data["is_staff"],first_name=validated_data["first_name"],last_name=validated_data["last_name"])
        return user