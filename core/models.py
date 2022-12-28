from django.db import models, transaction
from django.contrib.auth.models import User
# from .email import *
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


class UserProfileManager(models.Manager):
    
    #def get_by_username(self, username):
    #     return self.get(username__iexact=username)

    def get_if_available(self, username, email):
        try:
            by_username = self.get(username__iexact=username)
            if by_username == None:
                return self.get(email = email)
            return by_username
        except:
            return None
        
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    username = models.CharField(max_length=32, blank=False, null=True, unique=True)
    password = models.CharField(max_length=100, blank=False, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length =255, unique=True)
    
    # created_at = models.DateTimeField(auto_now_add=True)
    objects = UserProfileManager()
    @property
    def token(self):
        token, created = Token.objects.get_or_create(user=self.user)
        return token.key
    
    def __str__(self):
        return self.username
   

# class UserProfileVerificationObjectManager(models.Manager):
#     def create(self, **kwargs):
#         created = False

#         with transaction.atomic():
#             user_profile = kwargs.get('user_profile')

#             # lock the user profile to prevent concurrent creations
#             user_profile = UserProfile.objects.select_for_update().get(pk=user_profile.pk)

#             time = timezone.now() - timezone.timedelta(minutes=UserProfileEmailVerification.RETRY_TIME)

#             # select the latest valid user profile phone verification object
#             user_profile_email = UserProfileEmailVerification.objects.order_by('-created_at'). \
#                 filter(created_at__gte=time,
#                        user_profile__email=user_profile.email) \
#                 .last()

#             # create a new object if none exists
#             if not user_profile_email:
#                 obj = UserProfileEmailVerification(**kwargs)
#                 obj.save()
#                 created = True

#         if created:
#             if settings.DEBUG:
#                 return {'status': 201, 'obj': obj, 'code': obj.code}
#             return {'status': 201, 'obj': obj}

#         return {'status': 403,
#                 'wait': timezone.timedelta(minutes=UserProfileEmailVerification.RETRY_TIME) +
#                         (user_profile_email.created_at - timezone.now())}


# class UserProfileEmailVerification(models.Model):
#     """
#         Used for phone verification by sms
#         auto generates a 5 digit code
#         limits select querying
#         time intervals between consecutive creation
#     """

#     RETRY_TIME = 2
#     MAX_QUERY = 5

#     user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="emails")
#     code = models.CharField(max_length=13, default=generate_code)
#     created_at = models.DateTimeField(auto_now_add=True)
#     query_times = models.IntegerField(default=0)
#     used = models.BooleanField(default=False)
#     burnt = models.BooleanField(default=False)

#     objects = UserProfileVerificationObjectManager()

# @receiver(post_save, sender=UserProfileEmailVerification)
# def send_verification_email(sender, instance, created, **kwargs):
#     """
#         send the verification code if a new object is created
#     """
#     if created:
#         # send_verification_code(instance.user_profile.email, instance.code)
#         send_code_email(instance.user_profile.first_name, instance.user_profile.email, instance.code)
       
class ForgetPasswordLinkObjectManager(models.Manager):
    def create(self, **kwargs):
        created = False

        with transaction.atomic():
            user_profile = kwargs.get('user_profile')

            # lock the user profile to prevent concurrent creations
            user_profile = UserProfile.objects.select_for_update().get(pk=user_profile.pk)

            time = timezone.now() - timezone.timedelta(minutes=ForgetPasswordLink.RETRY_TIME)

            # select the latest valid user profile phone verification object
            user_profile_email = ForgetPasswordLink.objects.order_by('-created_at'). \
                filter(created_at__gte=time,
                       user_profile__email=user_profile.email) \
                .last()

            # create a new object if none exists
            if not user_profile_email:
                obj = ForgetPasswordLink(**kwargs)
                obj.save()
                created = True

        if created:
            if settings.DEBUG:
                return {'status': 201, 'obj': obj, 'link': obj.link}
            return {'status': 201, 'obj': obj}

        return {'status': 403,
                # 'wait': timezone.timedelta(minutes=UserProfileEmailVerification.RETRY_TIME) +
                #         (user_profile_email.created_at - timezone.now())
                }



class ForgetPasswordLink(models.Model):
    RETRY_TIME = 2

    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="forget_password_link")
    link = models.CharField(max_length = 16, default=generate_16char_link)
    used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ForgetPasswordLinkObjectManager()

# @receiver(post_save, sender=ForgetPasswordLink)
# def send_verification_email(sender, instance, created, **kwargs):
#     """
#         send the change password if a new object is created
#     """
#     if created:
#         #send_verification_code(instance.user_profile.email, instance.code)
#         #link_text = "/api/v1/change_password/" + instance.link + "/"
#         #link = request.build_absolute_uri(link_text)
#         #link = str(request.get_host) + link_text
#         #link = request.build_absolute_uri(reverse('view_name', args=(instance.link, )))
#         send_change_password_email(instance.user_profile.first_name, instance.user_profile.email, instance.link)

        
        
        
        
# model Member
class Member(models.Model):    
    Male = 0
    Female = 1

    genders = (
        (Male, "Male"),
        (Female, "Female")
    )
    
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name="member")
    height = models.IntegerField(default=165)
    weight = models.IntegerField(default=60)
    sex = models.IntegerField(choices=genders, default=Male)
    # arm = models.IntegerField(max_length =255, null=True, blank=True)
    # chest = models.IntegerField(max_length =255, null=True, blank=True)
    # waist = models.IntegerField(max_length =255, null=True, blank=True)
    # hip = models.IntegerField(max_length =255, null=True, blank=True)
    # thigh = models.IntegerField(max_length =255, null=True, blank=True)
    wallet = models.BigIntegerField(default=0)
    # record = models.BooleanField(default = False)
    # group = models.IntegerField(default = 1)
    
    def __str__(self):
        return self.user_profile.username
        
# model Club
class Trainer(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name="trainer")
    def __str__(self):
        return self.user_profile.username

class Owner(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name="owner")
    # club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="club")
    def __str__(self):
        return self.user_profile.username

class Club(models.Model):
    owner = models.OneToOneField(Owner, on_delete=models.CASCADE, related_name="club")
    # programs = models.OneToOneField(Program, on_delete=models.CASCADE, related_name="program")
    # trainers = models.ManyToManyField(Trainer, related_name="trainers", blank=True)
    name = models.CharField(max_length=32)
    address = models.TextField(max_length=500)
    # phone_number = models.CharField(max_length=12)
    def __str__(self):
        return (self.owner.user_profile.username + " -> " + self.name)

class Event(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name="send_event_owner")
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="receiver_event_owner")
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=300)
    date = models.DateField(null = True, blank = True)
    hour = models.IntegerField(null = True, blank = True)
    minute = models.IntegerField(null = True, blank = True)
    duration = models.IntegerField(null = True, blank = True)
    capacity = models.IntegerField(default=0)
    attachment = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100, null = True, blank = True)
    
    def __str__(self):
        return (self.owner.user_profile.username +
                "->" + self.title)
 
 
class TargetCategory(models.Model):
    name = models.CharField(max_length=110)
    def __str__(self):
        return self.name
   
class Target(models.Model):
    member = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name="target")
    category = models.OneToOneField(TargetCategory, on_delete=models.CASCADE, related_name="target",blank=True)
    num_days = models.IntegerField(default=0, blank=True, null=True)
    target_height = models.IntegerField(default=165, blank=True, null=True)
    target_weight = models.IntegerField(default=60, blank=True, null=True)
    def __str__(self):
        return (self.member.user_profile.username + 
                "->" + self.category.name)
    
    
# Trainer-Club Relation
class TCR(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name="TCR_trainers")
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="TCR_club")
    

# Member-Club Relation
class MCR(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="MCR_club")
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="MCR_member")
    
    
# Event-Members Relation
class EMR(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="EMR_event")
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="EMR_member")
    isRegistered = models.BooleanField(default=False)
    
    
class Program(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=50, blank=True, null=True)
    price = models.IntegerField(default=0)
    capacity = models.IntegerField(default=0)
    image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100, null = True, blank = True)
    # owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name="program_owner")
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name="program_trainer")
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="program_club")
    
    def __str__(self):
        return (self.trainer.user_profile.username + "->" + self.name)
    
# Member-Program Relation
class MPR(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name="MPR_program")
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="MPR_member")
    is_finished = models.BooleanField(default=False)
    
    
    
class Diet(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=50, blank=True, null=True)
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100, null = True, blank = True)
    day = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100, null = True, blank = True)
    # owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name="program_owner")
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name="diet_trainer")
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="diet_club")
    
    def __str__(self):
        return (self.trainer.user_profile.username + "->" + self.name)
    
    
# Diet-Member Relation
class DMR(models.Model):
    pass
    
    
    