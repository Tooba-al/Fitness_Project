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
        elif hasattr(instance, 'owner'):
            _flag = 2
        elif hasattr(instance, 'trainer'):
            _flag = 3


        if _flag == 0:
            return "None"
        if _flag == 1:
            return "Member"
        if _flag == 2:
            return "Club Owner"
        if _flag == 3:
            return "Trainer"

class UserProfileDataEditSerializer(serializers.ModelSerializer):
    profile_data = serializers.SerializerMethodField()
    class Meta:
        model = Member
        fields =  ['profile_data', 'height', 'weight']

    def get_profile_data(self, instance):
        _user_profile = instance.user_profile
        _profile_data = {}
        _profile_data['first_name'] = _user_profile.first_name
        _profile_data['last_name'] = _user_profile.last_name
        return _profile_data
    
    def put(self, instance):
        _user_profile = instance.user_profile
        _profile_data = {}
        _profile_data['first_name'] = _user_profile.first_name
        _profile_data['last_name'] = _user_profile.last_name

class MemberDataEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields =  ['first_name', 'last_name', 'email', 'sex']
        
class UserDataSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    class Meta:
        model = UserProfile
        fields =  ['user_username', 'username', 'password', 'first_name', 'last_name', 'email']

class UserSignUpSerializer(serializers.ModelSerializer):
    # record = serializers.BooleanField(default = False)
    # height = serializers.IntegerField()
    # weight = serializers.IntegerField()
    # arm = serializers.IntegerField(allow_null=True)
    # chest = serializers.IntegerField(allow_null=True)
    # waist = serializers.IntegerField(allow_null=True)
    # hip = serializers.IntegerField(allow_null=True)
    # thigh = serializers.IntegerField(allow_null=True)
    # wallet = serializers.CharField()
    
    class Meta:
        model = UserProfile
        # fields = ['username','password', 'first_name', 'last_name', 'email', 'wallet']
        fields = ['username','password', 'first_name', 'last_name', 'email']
                #   'height', 'weight', 'arm', 'chest', 'waist', 'hip', 'thigh', 'wallet']
        #read_only_fields = ['wallet']
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        user = UserProfile.objects.create(validated_data['username'], 
                                            validated_data['email'], 
                                            validated_data['password'],
                                            validated_data['first_name'], 
                                            validated_data['last_name'], )

        return user

class OwnerSignUpSerializer(serializers.ModelSerializer):
    club_name = serializers.CharField(allow_null=True)
    club_address = serializers.CharField(allow_null=True)
    class Meta:
        model = UserProfile
        fields = ['username','password', 'first_name', 'last_name', 'email', 'club_name', 'club_address']

class UserProfileEmailVerificationSerializer(serializers.Serializer):
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
   
##################################
##################################
##################################
   
class MemberSerializer(serializers.ModelSerializer):
    profile_data = serializers.SerializerMethodField()
    
    class Meta:
        model = Member
        fields = ['id', 'profile_data', 'weight', 'height', 'wallet', 'sex']
        
    def get_profile_data(self, instance):
        _user_profile = instance.user_profile
        _profile_data = {}
        _profile_data['username'] = _user_profile.username
        _profile_data['first_name'] = _user_profile.first_name
        _profile_data['last_name'] = _user_profile.last_name
        return _profile_data
        
class OwnerSerializer(serializers.ModelSerializer):
    profile_data = serializers.SerializerMethodField()
    
    class Meta:
        model = Owner
        fields = ['id', 'profile_data']
        
    def get_profile_data(self, instance):
        _user_profile = instance.user_profile
        _profile_data = {}
        _profile_data['username'] = _user_profile.username
        _profile_data['first_name'] = _user_profile.first_name
        _profile_data['last_name'] = _user_profile.last_name
        return _profile_data
        
class TrainerSerializer(serializers.ModelSerializer):
    profile_data = serializers.SerializerMethodField()
    
    class Meta:
        model = Trainer
        fields = ['id', 'profile_data']
        
    def get_profile_data(self, instance):
        _user_profile = instance.user_profile
        _profile_data = {}
        _profile_data['username'] = _user_profile.username
        _profile_data['first_name'] = _user_profile.first_name
        _profile_data['last_name'] = _user_profile.last_name
        return _profile_data
   
class MemberListSerializer(serializers.ModelSerializer):
    profile_data = serializers.SerializerMethodField()
    
    class Meta:
        model = Member
        fields = ['id', 'profile_data', 'weight', 'height', 'sex', 'wallet']
        
    def get_profile_data(self, instance):
        _user_profile = instance.user_profile
        _profile_data = {}
        _profile_data['username'] = _user_profile.username
        _profile_data['first_name'] = _user_profile.first_name
        _profile_data['last_name'] = _user_profile.last_name
        return _profile_data
   
class TrainerListSerializer(serializers.ModelSerializer):
    profile_data = serializers.SerializerMethodField()
    
    class Meta:
        model = Trainer
        fields = ['id', 'profile_data']
        
    def get_profile_data(self, instance):
        _user_profile = instance.user_profile
        _profile_data = {}
        _profile_data['username'] = _user_profile.username
        _profile_data['first_name'] = _user_profile.first_name
        _profile_data['last_name'] = _user_profile.last_name
        return _profile_data
   
class OwnerListSerializer(serializers.ModelSerializer):
    profile_data = serializers.SerializerMethodField()
    
    class Meta:
        model = Owner
        fields = ['id', 'profile_data']
        
    def get_profile_data(self, instance):
        _user_profile = instance.user_profile
        _profile_data = {}
        _profile_data['username'] = _user_profile.username
        _profile_data['first_name'] = _user_profile.first_name
        _profile_data['last_name'] = _user_profile.last_name
        return _profile_data
 
class EventSerializer(serializers.ModelSerializer):
    owner_data = serializers.SerializerMethodField()
    member_data = serializers.SerializerMethodField()
    class Meta:
        model = Event
        fields = ['id', 'owner_data', 'member_data', 'title', 'description', 'date', 'capacity', 'attachment']
    
    def get_owner_data(self, instance):
        _owner = instance.owner
        return OwnerSerializer(instance = _owner).data
    
    def get_member_data(self, instance):
        _member = instance.member
        return MemberSerializer(instance = _member).data
  
class CreateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'owner', 'title','description', 'date', 'capacity', 'attachment']
        read_only_fields = ['owner']
        
class SendEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id' ,'title', 'description', 'date', 'capacity', 'attachment']

class RecievedEventsSerializer(serializers.ModelSerializer):
    member_data = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'capacity', 'attachment']

    def get_member_data(self, instance):
        _member = instance.member
        _user_profile = _member.user_profile
        _profile_data = {}
        _profile_data['username'] = _user_profile.username
        _profile_data['first_name'] = _user_profile.first_name
        _profile_data['last_name'] = _user_profile.last_name
        return _profile_data

class SentEventsSerializer(serializers.ModelSerializer):
    owner_username = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id', 'owner', 'owner_username', 'title']

    def get_owner_username(self, instance):
        _owner = instance.owner
        _username = _owner.user_profile.username
        return _username
 
class EventSerializer(serializers.ModelSerializer):
    owner_data = serializers.SerializerMethodField()
    class Meta:
        model = Event
        fields = ['id', 'owner_data', 'title','description', 'date', 'capacity', 'attachment']
    
    def get_owner_data(self, instance):
        _owner = instance.owner
        return OwnerSerializer(instance = _owner).data
    
class EMRSerializer(serializers.ModelSerializer):
    class Meta:
        model = EMR
        fields = []
    
class EventListSerializer(serializers.ModelSerializer):
    owner_data = serializers.SerializerMethodField()
    class Meta:
        model = Event
        fields = ['id', 'owner_data', 'title', 'description', 'date', 'capacity', 'attachment']
    
    def get_owner_data(self, instance):
        _owner = instance.owner
        return OwnerListSerializer(instance = _owner).data
    
class ClubSerializer(serializers.ModelSerializer):
    owner_data = serializers.SerializerMethodField()
    # trainer_data= serializers.SerializerMethodField()
    class Meta:
        model = Club
        # fields = ['name', 'address', 'trainer_data', 'owner_data']
        fields = ['id', 'name', 'address', 'owner_data']

    def get_owner_data(self, instance):
        _user_profile = instance.owner.user_profile
        _owner_data = {}
        _owner_data['username'] = _user_profile.user.username
        _owner_data['first_name'] = _user_profile.user.first_name
        _owner_data['last_name'] = _user_profile.user.last_name
        return _owner_data   
        
class AddToWalletSerializer(serializers.ModelSerializer):
    wallet_data = serializers.SerializerMethodField()
    username = serializers.CharField(max_length=32)
    amount = serializers.IntegerField(default=0)
    
    class Meta:
        model = Member
        fields = ['id', 'wallet_data', 'amount']
        fields = ['id', 'wallet_data', 'username', 'amount']
        
    def get_wallet_data(self, instance):
        _user_profile = instance.user_profile
        _owner_data = {}
        _owner_data['wallet'] = _user_profile.wallet
        return _owner_data

class AddTrainerSerializer(serializers.Serializer):
    owner_username = serializers.CharField(max_length=32)
    trainer_username = serializers.CharField(max_length=32)
    trainer_password= serializers.CharField(max_length=32)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.CharField(max_length =255)

class ProgramSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(max_length=32)
    trainer_username = serializers.CharField(max_length=32)
    club_name = serializers.CharField(max_length=32)
    # owner_data = serializers.SerializerMethodField()
    class Meta:
        model = Program
        fields = ['id', 'name', 'price', 'image', 
                  'club_name', 'trainer_username', 'owner_username']
        
class ProgramListSerializer(serializers.ModelSerializer):
    trainer_data = serializers.SerializerMethodField()
    club_data = serializers.SerializerMethodField()
    
    class Meta:
        model = Program
        fields = ['id', 'name', 'price', 'image', 'trainer_data', 'club_data']
        # fields = ['name', 'price', 'image']
        
    def get_trainer_data(self, instance):
        _user_profile = instance.trainer.user_profile
        _trainer_data = {}
        _trainer_data['first_name'] = _user_profile.first_name
        _trainer_data['last_name'] = _user_profile.last_name
        return _trainer_data
    
        
    def get_club_data(self, instance):
        _club = instance.club
        _club_data = {}
        _club_data['owner_first'] = _club.owner.user_profile.first_name
        _club_data['owner_last'] = _club.owner.user_profile.last_name
        _club_data['name'] = _club.name
        _club_data['address'] = _club.address
        return _club_data
    
# class MemberProgramShowToOwnerSerializer(serializers.Serializer):
#     club_name = serializers.CharField(max_length = 32)
#     member_data = serializers.SerializerMethodField()
#     program_data = serializers.SerializerMethodField()
    
#     class Meta:
#         model = Program
#         fields = ['id', 'club_name', 'member_data', 'program_data']
#         # fields = ['name', 'price', 'image']
        
#     def get_member_data(self, instance):
#         _user_profile = instance.member.user_profile
#         _member_data = {}
#         _member_data['first_name'] = _user_profile.first_name
#         _member_data['last_name'] = _user_profile.last_name
#         _member_data['height'] = _user_profile.height
#         _member_data['weight'] = _user_profile.weight
#         _member_data['sex'] = _user_profile.sex
#         return _member_data
        
#     def get_program_data(self, instance):
#         _program = instance.program
#         _program_data = {}
#         _program_data['name'] = _program.name
#         _program_data['trainer'] = _program.trainer.username
#         _program_data['club'] = _program.club.name
#         return _program_data

class DietSerializer(serializers.ModelSerializer):
    trainer_username = serializers.CharField(max_length=32)
    club_name = serializers.CharField(max_length=32)
    class Meta:
        model = Diet
        fields = ['id', 'name', 'description', 'price', 
                  'image', 'day', 'trainer_username', 'club_name']

class DietistSerializer(serializers.ModelSerializer):
    trainer_data = serializers.SerializerMethodField()
    club_data = serializers.SerializerMethodField()
    
    class Meta:
        model = Diet
        fields = ['id', 'name', 'price', 'image', 'trainer_data', 'club_data']
        # fields = ['name', 'price', 'image']
        
    def get_trainer_data(self, instance):
        _user_profile = instance.trainer.user_profile
        _trainer_data = {}
        _trainer_data['first_name'] = _user_profile.first_name
        _trainer_data['last_name'] = _user_profile.last_name
        return _trainer_data
    
        
    def get_club_data(self, instance):
        _club = instance.club
        _club_data = {}
        _club_data['owner_first'] = _club.owner.user_profile.first_name
        _club_data['owner_last'] = _club.owner.user_profile.last_name
        _club_data['name'] = _club.name
        _club_data['address'] = _club.address
        return _club_data

class EnrollProgramSerializer(serializers.Serializer):
    member_username = serializers.CharField(max_length=32)
    program_name = serializers.CharField(max_length=32)
    club_name = serializers.CharField(max_length=32)
    
class EnrollDietSerializer(serializers.Serializer):
    member_username = serializers.CharField(max_length=32)
    diet_name = serializers.CharField(max_length=32)
    club_name = serializers.CharField(max_length=32)
    
class JoinToClubSerializer(serializers.Serializer):
    member_username = serializers.CharField(max_length=32)
    club_name = serializers.CharField(max_length=32)  

# Trainer-Club Relation
class TCRSerializer(serializers.ModelSerializer):
    class Meta:
        model = TCR
        fields = []

# Member-Club Relation
class MCRSerializer(serializers.ModelSerializer):
    class Meta:
        model = MCR
        fields = []
        
# Event-Member Relation
class EMRSerializer(serializers.ModelSerializer):
    class Meta:
        model = EMR
        fields = []

# Member-Program Relation
class MPRSerializer(serializers.ModelSerializer):
    class Meta:
        model = MPR
        fields = []

# Diet-Member Relation
class DMRSerializer(serializers.ModelSerializer):
    class Meta:
        model = DMR
        fields = []

###############################
###############################
###############################

# Bounus Part

class EducationSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField()
    trainer_data = serializers.SerializerMethodField()
    
    class Meta:
        model = Education
        fields = ['id', 'trainer_data','name', 'text', 'image', 'created_at', 
                  'likes_count', 'is_liked']
        read_only_fields = ['trainer']
        

    def get_is_liked(self,instance):
        request = self.context.get('request',None)
        _user_profile = request.user.user_profile
        return instance.is_liked(_user_profile)

    def get_trainer_data(self, instance):
        _care_giver = instance.care_giver
        return TrainerListSerializer(instance = _care_giver).data

class EducationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['id', 'trainer', 'name', 'text', 'image', 'created_at']
        read_only_fields = ['trainer']

# Education-Member Relation
class EdMRSerializer(serializers.ModelSerializer):
    class Meta:
        model = EdMR
        fields = []