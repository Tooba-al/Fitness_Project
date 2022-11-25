from rest_framework import serializers
from .models import *
from django.utils.translation import gettext as _

class UserProfileDataSerializer(serializers.ModelSerializer):
    situation = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['username','email','first_name', 'last_name', 'situation']
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
    # height = serializers.IntegerField()
    # weight = serializers.IntegerField()
    # arm = serializers.IntegerField(allow_null=True)
    # chest = serializers.IntegerField(allow_null=True)
    # waist = serializers.IntegerField(allow_null=True)
    # hip = serializers.IntegerField(allow_null=True)
    # thigh = serializers.IntegerField(allow_null=True)
    wallet = serializers.IntegerField(default=0)

    class Meta:
        model = Member
        fields = ['username','password', 'first_name', 'last_name', 'email', 'sex', 'wallet']
                #   'height', 'weight', 'arm', 'chest', 'waist', 'hip', 'thigh', 'wallet']
        #read_only_fields = ['wallet']

class OwnerSignUpSerializer(serializers.ModelSerializer):
    club_name = serializers.IntegerField(allow_null=True)
    class Meta:
        model = UserProfile
        fields = ['username','password', 'first_name', 'last_name', 'email', 'sex', 'club_name']
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
    
class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=100)

class ResendVerificationCodeSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    
class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
     
 
    
class ClubSerializer(serializers.Serializer):
    class Meta:
        model = Club
        fields = ['name','trainers', 'first_name', 'last_name', 'email', 'sex', 'wallet']

    
class ClubListSerializer(serializers.ModelSerializer):
    owner_data = serializers.SerializerMethodField()
    trainers_list = serializers.SerializerMethodField()
    
    class Meta:
        model = Club
        fields = ['id', 'name', 'owner_data', 'trainers_list', 'specialty', 'role']
        
    def get_owner_data(self, instance):
        _user_profile = instance.user_profile
        _owner_data = {}
        _owner_data['username'] = _user_profile.username
        _owner_data['first_name'] = _user_profile.first_name
        _owner_data['last_name'] = _user_profile.last_name
        
        
class AddToWalletSerializer(serializers.ModelSerializer):
    wallet_data = serializers.SerializerMethodField()
    
    class Meta:
        model = Member
        fields = ['id', 'wallet_data']
        
    def get_wallet_data(self, instance):
        _user_profile = instance.user_profile
        _owner_data = {}
        _owner_data['wallet'] = _user_profile.wallet
