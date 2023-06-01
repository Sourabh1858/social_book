from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Profile,CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [ 'designation', 'salary', 'profile_photo']

class CustomUserSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer(read_only=True)
    class Meta:
        model = CustomUser
        fields = [ 'id','username','email','publicVisibility','birthYear','address','age','profile',
                  'is_staff','is_active','is_superuser']


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [ 'designation', 'salary', 'profile_photo']

        def update(self,instance,validated_data):
            instance.salary=validated_data.get('salary',instance.salary) 
            instance.designation=validated_data.get('designation',instance.designation) 
            instance.profile_photo=validated_data.get('salary',instance.profile_photo) 


     