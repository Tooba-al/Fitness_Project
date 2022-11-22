from rest_framework import serializers
from .models import *
from django.utils.translation import gettext as _

class UserProfileDataSerializer(serializers.ModelSerializer):
    situation = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['username','email','first_name', 'last_name', ]
        #read_only_fields = ['wallet']

    def get_situation(self, instance):
        _flag = 0

        if hasattr(instance, 'member'):
            _flag =1
        elif hasattr(instance, 'club_owner'):
            _flag = 2


        if _flag == 0:
            return "None"
        if _flag == 1:
            return "Member"
        if _flag == 2:
            return "Club Owner"


class UserProfileDataEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields =  ['first_name', 'last_name', 'email']


class MemberSignUpSerializer(serializers.ModelSerializer):
    record = serializers.BooleanField(default = False)
    height = serializers.IntegerField()
    weight = serializers.IntegerField()
    arm = serializers.IntegerField(allow_null=True)
    chest = serializers.IntegerField(allow_null=True)
    waist = serializers.IntegerField(allow_null=True)
    hip = serializers.IntegerField(allow_null=True)
    thigh = serializers.IntegerField(allow_null=True)

    class Meta:
        model = Member
        fields = ['username','password', 'first_name', 'last_name', 'email', 'sex',
                  'height', 'weight', 'arm', 'chest', 'waist', 'hip', 'thigh']
        #read_only_fields = ['wallet']

class OwnerSignUpSerializer(serializers.ModelSerializer):
    club_name = serializers.IntegerField(allow_null=True)
    class Meta:
        model = UserProfile
        fields = ['username','password','phone_number','first_name', 'last_name', 'email', 'sex', 'club_name']
        #read_only_fields = ['wallet']

class UserProfileEmailVerificationSerializer(serializers.Serializer):
    """
        Used for verifying emails
    """
    code = serializers.CharField(max_length=10)
    email = serializers.CharField(max_length=15)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=32)
    password = serializers.CharField(max_length=32)
     
    