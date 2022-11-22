from django.db import models, transaction
from django.contrib.auth.models import User
from .email import *
from .helpers import *
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.utils import timezone
from Fitness import settings
from django.db.models.signals import post_save
from django.core.validators import RegexValidator
from django.utils.translation import gettext as _
import json
from sys import platform

        
class UserProfile(models.Model):
    Male = 0
    Female = 1

    genders = (
        (Male, "Male"),
        (Female, "Female")
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    #wallet = models.OneToOneField('Wallet', on_delete=models.CASCADE, related_name='user_profile', blank=True,
    #                              null=True)
    username = models.CharField(max_length=32, blank=False, null=True, unique=True)
    password = models.CharField(max_length=100, blank=False, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length =255, unique=True)
    sex = models.IntegerField(choices=genders, default=Male)
    # created_at = models.DateTimeField(auto_now_add=True)

    @property
    def token(self):
        token, created = Token.objects.get_or_create(user=self.user)
        return token.key
    

class UserProfileVerificationObjectManager(models.Manager):
    def create(self, **kwargs):
        created = False

        with transaction.atomic():
            user_profile = kwargs.get('user_profile')

            # lock the user profile to prevent concurrent creations
            user_profile = UserProfile.objects.select_for_update().get(pk=user_profile.pk)

            time = timezone.now() - timezone.timedelta(minutes=UserProfileEmailVerification.RETRY_TIME)

            # select the latest valid user profile phone verification object
            user_profile_phone = UserProfileEmailVerification.objects.order_by('-created_at'). \
                filter(created_at__gte=time,
                       user_profile__email=user_profile.email) \
                .last()

            # create a new object if none exists
            if not user_profile_phone:
                obj = UserProfileEmailVerification(**kwargs)
                obj.save()
                created = True

        if created:
            if settings.DEBUG:
                return {'status': 201, 'obj': obj, 'code': obj.code}
            return {'status': 201, 'obj': obj}

        return {'status': 403,
                'wait': timezone.timedelta(minutes=UserProfileEmailVerification.RETRY_TIME) +
                        (user_profile_phone.created_at - timezone.now())}


class UserProfileEmailVerification(models.Model):
    """
        Used for phone verification by sms
        auto generates a 5 digit code
        limits select querying
        time intervals between consecutive creation
    """

    RETRY_TIME = 2
    MAX_QUERY = 5

    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="emails")
    code = models.CharField(max_length=13, default=generate_code)
    created_at = models.DateTimeField(auto_now_add=True)
    query_times = models.IntegerField(default=0)
    used = models.BooleanField(default=False)
    burnt = models.BooleanField(default=False)

    objects = UserProfileVerificationObjectManager()

@receiver(post_save, sender=UserProfileEmailVerification)
def send_verification_email(sender, instance, created, **kwargs):
    """
        send the verification code if a new object is created
    """
    if created:
        # send_verification_code(instance.user_profile.email, instance.code)
        send_code_email(instance.user_profile.first_name, instance.user_profile.email, instance.code)
        
# model Member
class Member(models.Model):    
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name="member")
    height = models.IntegerField(max_length =255)
    weight = models.IntegerField(max_length =255)
    arm = models.IntegerField(max_length =255, null=True, blank=True)
    chest = models.IntegerField(max_length =255, null=True, blank=True)
    waist = models.IntegerField(max_length =255, null=True, blank=True)
    hip = models.IntegerField(max_length =255, null=True, blank=True)
    thigh = models.IntegerField(max_length =255, null=True, blank=True)
    # record = models.BooleanField(default = False)
    # group = models.IntegerField(default = 1)
        
# model Club
class Club(models.Model):
    # programs = models.OneToOneField(Program, on_delete=models.CASCADE, related_name="program")
    name = models.CharField(max_length=32)
    
class Owner(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name="owner")
    club = models.OneToOneField(Club, on_delete=models.CASCADE, related_name="club")

    

     