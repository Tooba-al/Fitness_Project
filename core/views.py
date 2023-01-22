from hashlib import new
from .serializers import *
from rest_framework import generics,status,filters
from rest_framework.response import Response
# from .permissions import *
from django.utils.translation import gettext as _
from django.contrib.auth.hashers import make_password, check_password
from .models import *
import ast
import os
import datetime
from .permissions import *


class UserSignUpView(generics.GenericAPIView):
    """
        Send verification code
        if send failed respond with wait time
    """

    serializer_class = UserSignUpSerializer

    def get_object(self):
        email = self.request.data.get('email')
        username = self.request.data.get('username')

        try:
            return UserProfile.objects.get_if_available(username, email)
        except UserProfile.DoesNotExist:
            return None

    def post(self, request, *args, **kwargs):
        s = self.serializer_class(data=request.data)
        s.is_valid(raise_exception=True)

        user_profile = self.get_object()

        if not user_profile:
            # try:
            with transaction.atomic():
                valid = s.validated_data
                # hash = make_password(valid.get("password"))
                hash = make_password(valid.get("password"))
                user=User.objects.create(username=s.validated_data.get('username'))
                token, created = Token.objects.get_or_create(user=user)
                token.save()
                user_profile = UserProfile.objects.create(username = valid.get('username'),
                                                        password = valid.get('username'),
                                                        email = valid.get('email'),
                                                        first_name = valid.get('first_name'),
                                                        last_name = valid.get('last_name'),
                                                        token=token,                                              
                                                        user=user,)
                user_profile.save()
                # utr = UTR.objects.create(user_profile=user_profile,
                #                          token=str(token))
                # utr.save()
                member = Member.objects.create(user_profile = user_profile,
                                                sex = 0,
                                                height = 165,
                                                weight = 60,
                                                wallet = 0)
                member.save()   
                data = UserProfileDataSerializer(instance = user_profile).data
                
                return Response({'detail': _("wellcome :)"), 'data': data, 'token': token.key})

            # except:
                # return Response({'detail': _("Problem with signing up")}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': _("This profile already exists.")}, status=status.HTTP_400_BAD_REQUEST)
      
class OwnerSignUpView(generics.GenericAPIView):
    
    """
        Send verification code
        if send failed respond with wait time
    """

    serializer_class = OwnerSignUpSerializer

    def get_object(self):
        email = self.request.data.get('email')
        username = self.request.data.get('username')

        try:
            return UserProfile.objects.get_if_available(username, email)
        except UserProfile.DoesNotExist:
            return None

    def post(self, request, *args, **kwargs):
        s = self.serializer_class(data=request.data)
        s.is_valid(raise_exception=True)

        user_profile = self.get_object()

        if not user_profile:
            with transaction.atomic():
                valid = s.validated_data
                hash = make_password(valid.get("password"))
                user=User.objects.create(username=s.validated_data.get('username'))
                token, created = Token.objects.get_or_create(user=user)
                token.save()
                user_profile = UserProfile.objects.create(username = valid.get('username'),
                                                        password = valid.get('username'),
                                                        email = valid.get('email'),
                                                        first_name = valid.get('first_name'),
                                                        last_name = valid.get('last_name'),                                                
                                                        user=user,
                                                        token=token)
                user_profile.save()
                owner = Owner.objects.create(
                    user_profile = user_profile,
                )
                owner.save()
                club = Club.objects.create(
                    owner = owner,
                    name = valid.get('club_name'),
                    address = valid.get('club_address'),
                )
                club.save()

                # upv = UserProfileEmailVerification.objects.create(user_profile=self.get_object())

                # if upv['status'] != 201:
                #     return Response({'detail': _("Code not sent"), 'wait': upv['wait']}, status=upv['status'])

                # if settings.DEBUG:
                #     return Response({'detail': _("Code sent"), 'code': upv['code']})
                data = UserProfileDataSerializer(instance = user_profile).data
                
                return Response({'detail': _("wellcome :)"), 'data': data, 'token': token.key})

            # except:
            #     return Response({'detail': _("Problem with signing up")}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': _("This profile already exists.")}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileAuthTokenView(generics.CreateAPIView):
    """
        match phone number and verification code
        return user token on success
    """

    serializer_class = UserProfileDataSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):

        email = request.data.get('email')
        
        user = User.objects.get(email=email)
        
        if not user:
            return Response({'detail': _('Email not found')}, status=status.HTTP_404_NOT_FOUND)
        
        token, created = Token.objects.get_or_create(user=user)
        user.save()
        
        return Response({'detail': _('You are verified.'), 'token': token.key})

class RetrieveUserProfileDataView(generics.RetrieveAPIView):
    serializer_class = UserProfileDataSerializer
    # permission_classes = (IsAuthenticated,)

    def get_object(self):
        try:
            # return self.request.user
            return UserProfile.objects.get(token = str(self.request.auth)).user
        except UserProfile.DoesNotExist:
            return None

class RetrieveUserProfileEditView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileDataEditSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        try:
            return self.request.user
        except UserProfile.DoesNotExist:
            return None

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        # password = make_password(request.data.get('password'))

        try:
            user_profile = UserProfile.objects.get(username = username)
        except:
            user_profile = None

        if not user_profile:
            return Response({'detail': _('Username not found')}, status=status.HTTP_404_NOT_FOUND)

        if(password == user_profile.password):
            token = Token.objects.get_or_create(user=user_profile.user)[0]
            token.save()
            data = UserProfileDataSerializer(instance = user_profile).data
            return Response({'detail': _("Wellcome Back :)"), 'data': data, 'token': token.key})

        else:
            return Response({'detail': _('Wrong password'),}, status=status.HTTP_404_NOT_FOUND)

class ForgetPasswordView(generics.CreateAPIView):

    serializer_class = ForgetPasswordSerializer

    def post(self, request, *args, **kwargs):
        s = self.serializer_class(data=request.data)
        s.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                valid = s.validated_data
                user_profile = UserProfile.objects.get(email = valid.get('email'))
                fpl = ForgetPasswordLink.objects.create(user_profile=user_profile)

                if fpl['status'] != 201:
                    return Response({'detail': _("Code not sent"), 'wait': fpl['wait']}, status=fpl['status'])

                if settings.DEBUG:
                    return Response({'detail': _("Code sent"), 'link': fpl['link']})

                return Response({'detail': _("Code sent")})

        except UserProfile.DoesNotExist:
            return Response({'detail': _("No user profiles with this email.")}, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(generics.UpdateAPIView):

    serializer_class = ChangePasswordSerializer

    def put(self, request, *args, **kwargs):
        s = self.serializer_class(data=request.data)
        s.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                valid = s.validated_data
                change_link = valid.get('change_link')
                

                fpl = ForgetPasswordLink.objects.get(link = change_link)
                time = datetime.datetime.now(datetime.timezone.utc) - fpl.created_at

                if fpl.used == True:
                    return Response({'detail': _("You have already used this link.")}, status=status.HTTP_400_BAD_REQUEST)
                elif time > datetime.timedelta(hours = 1):
                    return Response({'detail': _("This link has surpassed its valid time.")}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    fpl.used = True
                    new_password = make_password(valid.get("password"))
                    user_profile = fpl.user_profile
                    user_profile.password = new_password
                    user_profile.save()
                    fpl.save()
                    return Response({'detail': _("Your password changed successfully")}, status=status.HTTP_200_OK)


        except ForgetPasswordLink.DoesNotExist:
            return Response({'detail': _("This link isn't valid.")}, status=status.HTTP_400_BAD_REQUEST)

# class ChangePasswordView(generics.UpdateAPIView):

    # serializer_class = ChangePasswordSerializer

    # def put(self, request, *args, **kwargs):
    #     s = self.serializer_class(data=request.data)
    #     s.is_valid(raise_exception=True)

    #     try:
    #         with transaction.atomic():
    #             valid = s.validated_data
    #             change_link = self.kwargs['change_link']

    #             fpl = ForgetPasswordLink.objects.get(link = change_link)
    #             time = datetime.datetime.now(datetime.timezone.utc) - fpl.created_at

    #             if fpl.used == True:
    #                 return Response({'detail': _("You have already used this link.")}, status=status.HTTP_400_BAD_REQUEST)
    #             elif time > datetime.timedelta(hours = 1):
    #                 return Response({'detail': _("This link has surpassed its valid time.")}, status=status.HTTP_400_BAD_REQUEST)
    #             else:
    #                 fpl.used = True
    #                 new_password = make_password(valid.get("password"))
    #                 user_profile = fpl.user_profile
    #                 user_profile.password = new_password
    #                 user_profile.save()
    #                 fpl.save()
    #                 return Response({'detail': _("Your password changed successfully")}, status=status.HTTP_200_OK)


    #     except ForgetPasswordLink.DoesNotExist:
    #         return Response({'detail': _("This link isn't valid.")}, status=status.HTTP_400_BAD_REQUEST)


class ResendVerificationCodeView(generics.CreateAPIView):

    serializer_class = ResendVerificationCodeSerializer

    def post(self, request, *args, **kwargs):
        s = self.serializer_class(data=request.data)
        s.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                valid = s.validated_data
                user_profile = UserProfile.objects.get(email = valid.get('email'))

                # upv = UserProfileEmailVerification.objects.create(user_profile=user_profile)

                # if upv['status'] != 201:
                #     return Response({'detail': _("Code not sent"), 'wait': upv['wait']}, status=upv['status'])

                # if settings.DEBUG:
                #     return Response({'detail': _("Code sent"), 'code': upv['code']})

                return Response({'detail': _("Code sent")})

        except UserProfile.DoesNotExist:
            return Response({'detail': _("This user doesn't exist.")}, status=status.HTTP_400_BAD_REQUEST)

##################################
##################################
##################################

class ShowMemberListView(generics.ListAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class ShowOwnerListView(generics.ListAPIView):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer

class ShowTrainerListView(generics.ListAPIView):
    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer

class ShowClubListView(generics.ListAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubListSerializer
    ordering_fields = ['name']
    
class ProgramListView(generics.ListAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramListSerializer
    
class DietListView(generics.ListAPIView):
    queryset = Diet.objects.all()
    serializer_class = ProgramListSerializer
    
class MemberView(generics.ListAPIView):
    serializer_class = MemberSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'username'
    
    def get_queryset(self):
        username = self.kwargs['username']
        try:
            return [Member.objects.filter(user_profile__username = username)][0]
        except Member.DoesNotExist:
            return None
    
class TrainerView(generics.ListAPIView):
    serializer_class = TrainerSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'username'
    
    def get_queryset(self):
        username = self.kwargs['username']
        try:
            return [Trainer.objects.filter(user_profile__username = username)][0]
        except Trainer.DoesNotExist:
            return None
    
    
class OwnerView(generics.ListAPIView):
    serializer_class = OwnerSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'username'
    
    def get_queryset(self):
        username = self.kwargs['username']
        try:
            return [Owner.objects.filter(user_profile__username = username)][0]
        except Owner.DoesNotExist:
            return None

class ClubView(generics.ListAPIView):
    serializer_class = ClubSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'club_id'
    
    def get_queryset(self):
        id = self.kwargs['club_id']
        try:
            return [Club.objects.filter(id = id)][0]
        except Club.DoesNotExist:
            return None

class EventView(generics.ListAPIView):
    serializer_class = EventSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'event_id'
    
    def get_queryset(self):
        id = self.kwargs['event_id']
        try:
            return [Event.objects.filter(id = id)][0]
        except Event.DoesNotExist:
            return None
    
class ProgramView(generics.ListAPIView):
    serializer_class = ProgramSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'program_id'
    
    def get_queryset(self):
        id = self.kwargs['program_id']
        try:
            return [Program.objects.filter(id = id)][0]
        except Program.DoesNotExist:
            return None

class DietView(generics.ListAPIView):
    serializer_class = DietSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'diet_id'
    
    def get_queryset(self):
        id = self.kwargs['diet_id']
        try:
            return [Diet.objects.filter(id = id)][0]
        except Diet.DoesNotExist:
            return None
        
###################################
###################################
###################################

class CreateEventView(generics.GenericAPIView):
    serializer_class = CreateEventSerializer
    
    def get_object(self):
        try:
            return Owner.objects.get(user_profile__username = self.request.data.get('owner_username'))
        except Owner.DoesNotExist:
            return None
        
    def post(self, request, *args, **kwargs):
        s = self.serializer_class(data=request.data)
        s.is_valid(raise_exception=True)
        valid = s.validated_data

        owner = self.get_object()
        if owner!=None:
            event = Event.objects.create(
                    owner = owner,
                    title = valid.get("title"),  
                    description = valid.get("description"),  
                    date = valid.get("date"),  
                    hour = valid.get("hour"),  
                    minute = valid.get("minute"),  
                    duration = valid.get("duration"),  
                    capacity = valid.get("capacity"),  
                    attachment = valid.get("attachment"),
            )
            event.save()
            return Response({'detail': _("Event successfully created.")})
        
        return Response({'detail': _("Problem with creating the event.")}, status=status.HTTP_400_BAD_REQUEST)

class RegisterEventView(generics.UpdateAPIView):
    serializer_class = EMRSerializer

    def post(self, request, *args, **kwargs):
        s = self.serializer_class(data=request.data)
        s.is_valid(raise_exception=True)
        valid = s.validated_data

        try:
            member = Member.objects.get(user_profile__username = valid.get('member_username'))
            event = Event.objects.get(id = self.kwargs['event_id'])
            event.capacity -= 1
            event.save()
            emr = EMR.objects.get_or_create(
                event = event, 
                member = member
            )
            emr[0].isRegistered = True
            emr[0].save()
            
            return Response({'detail': _("You registered to this event.")}, status=status.HTTP_200_OK)
        except:
            return Response({'detail': _("There was a problem with registering to this event.")}, status=status.HTTP_400_BAD_REQUEST)

class UnregisterEventView(generics.UpdateAPIView):
    serializer_class = EMRSerializer

    def post(self, request, *args, **kwargs):
        s = self.serializer_class(data=request.data)
        s.is_valid(raise_exception=True)
        valid = s.validated_data

        try:
            member = Member.objects.get(user_profile__username = valid.get('member_username'))
            event = Event.objects.get(id = self.kwargs['event_id'])
            event.capacity += 1
            event.save()
            emr = EMR.objects.get(
                event = event, 
                member = member
            )
            emr.isRegistered = False
            emr.save()
                
            return Response({'detail': _("You unregistered to this event.")}, status=status.HTTP_200_OK)
        except:
            return Response({'detail': _("There was a problem with unregistering to this event.")}, status=status.HTTP_400_BAD_REQUEST)

class ShowEventRegistrationListView(generics.ListAPIView):
    queryset = EMR.objects.all()
    serializer_class = RegisterationSerializer

class ShowEventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class MemberSearchView(generics.ListAPIView):
    serializer_class = MemberListSerializer

    def get_queryset(self):
        member_username = self.kwargs['member_username']

        try:
            return Member.objects.filter(user_profile__username__icontains = member_username)
        except Member.DoesNotExist:
            return None

class TrainerSearchView(generics.ListAPIView):
    serializer_class = TrainerListSerializer

    def get_queryset(self):
        trainer_username = self.kwargs['trainer_username']

        try:
            return Trainer.objects.filter(user_profile__username__icontains = trainer_username)
        except Trainer.DoesNotExist:
            return None

class OwnerSearchView(generics.ListAPIView):
    serializer_class = OwnerListSerializer

    def get_queryset(self):
        owner_username = self.kwargs['owner_username']

        try:
            return Owner.objects.filter(user_profile__username__icontains = owner_username)
        except Owner.DoesNotExist:
            return None

class AddToWalletView(generics.RetrieveAPIView):
    serializer_class = AddToWalletSerializer

    def get_object(self):
        try:
            username = self.request.data.get('username')
            user_profile = UserProfile.objects.get(username = username)
            return user_profile
        except UserProfile.DoesNotExist:
            return None

    def put(self, request, *args, **kwargs):
        user_profile = self.get_object()
        user_request_data = self.serializer_class(data=request.data)
        user_request_data.is_valid(raise_exception=True)
        
        try:
            with transaction.atomic():
                valid = user_request_data.validated_data
                member = Member.objects.get(user_profile = user_profile)
                member.wallet += valid.get('amount')
                member.save()
                    
                return Response({'detail': _("Your wallet successfuly updated.")}, status=status.HTTP_200_OK)
        except:
            return Response({'detail': _("There was a problem with updating your wallet.")}, status=status.HTTP_400_BAD_REQUEST)

class AddTrainerView(generics.GenericAPIView):
    serializer_class = AddTrainerSerializer
    
    def post(self, request, *args, **kwargs):        
        username = request.data.get('owner_username')
        
        s = self.serializer_class(data=request.data)
        s.is_valid(raise_exception=True)
        valid = s.validated_data
        
        try:
            owner = Owner.objects.get(user_profile__username = username)
        except:
            owner = None
        
        if not owner:
            return Response({'detail': _('Username not found')}, status=status.HTTP_404_NOT_FOUND)
        
        elif owner != None:
            user_profile = UserProfile.objects.create(
                username = valid.get('trainer_username'),
                password = valid.get('trainer_password'),
                first_name = valid.get('first_name'),
                last_name = valid.get('last_name'),
                email = valid.get('email'),
                user = User.objects.create(username=valid.get('trainer_username'))
            )
            user_profile.save()
            
            trainer = Trainer.objects.create(user_profile = user_profile)
            trainer.save()
    
            club = Club.objects.get(owner = owner)
            tcr = TCR.objects.create(club = club, 
                                     trainer = trainer)
            tcr.save()
            return Response({'detail': _('Trainer added successfully')})
        return Response({'detail': _("There was a problem with adding a trainer.")}, status=status.HTTP_400_BAD_REQUEST)

class CreateProgramView(generics.GenericAPIView):
    serializer_class = CreateProgramSerializer
    
    def get_object(self):
        try:
            return Owner.objects.get(user_profile__username = self.request.data.get('owner_username'))
        except Owner.DoesNotExist:
            return None
    
    def put(self, request, *args, **kwargs):
        s = self.serializer_class(data=request.data)
        s.is_valid(raise_exception=True)
        valid = s.validated_data
        
        owner = self.get_object()
        if owner!=None:
            club = Club.objects.get(owner=owner, name=valid.get('club_name'))
            trainer = Trainer.objects.get(user_profile__username=valid.get('trainer_username'))
            # owner = Owner.objects.get(user_profile__username = valid.get('owner_username'))
            program = Program.objects.create(
                name = valid.get('name'),
                image = valid.get('image'),
                price = valid.get('price'),
                trainer = trainer,
                club = club,
            )
            program.save()
            return Response({'detail': _('Program added successfully')})
        
        return Response({'detail': _("There was a problem with adding a program.")}, status=status.HTTP_400_BAD_REQUEST)

class DeleteProgramView(generics.DestroyAPIView):
    def delete(self, request, *args, **kwargs):

        try:
            with transaction.atomic():
                program_id = self.kwargs['program_id']
                program = Program.objects.get(id = program_id)
                program.delete()
                return Response({'detail': _("Program deleted.")}, status=status.HTTP_200_OK)

        except Program.DoesNotExist:
            return Response({'detail': _("This program doesn't exist.")}, status=status.HTTP_400_BAD_REQUEST)

class ProgramSearchView(generics.ListAPIView):
    serializer_class = ProgramSerializer

    def get_queryset(self):
        program_name = self.kwargs['program_name']

        try:
            return Program.objects.filter(name__icontains = program_name)
        except Program.DoesNotExist:
            return None

class EnrollersListView(generics.ListAPIView):
    queryset = MCR.objects.all()
    serializer_class = MCRListSerializer
    
class MemberProgramShowToOnwer(generics.ListAPIView):
    serializer_class = MPRListSerializer
    
    def get_queryset(self):
        mpr_list = []
        try:
            return MPR.objects.filter(program__club__owner__user_profile__username = self.kwargs['owner_username'])
        except MPR.DoesNotExist:
            return None

class CreateDietView(generics.GenericAPIView):
    serializer_class = CreateDietSerializer
    
    def get_object(self):
        try:
            username = self.request.data.get('trainer_username')
            trainer = Trainer.objects.get(user_profile__username = username)
            return trainer
        except UserProfile.DoesNotExist:
            return None
    
    def put(self, request, *args, **kwargs):
        s = self.serializer_class(data=request.data)
        s.is_valid(raise_exception=True)
        valid = s.validated_data
        
        trainer = self.get_object()
        if trainer!=None:
            owner = Owner.objects.get(user_profile__username=valid.get('owner_username'))
            club = Club.objects.get(owner=owner, name=valid.get('club_name'))

            diet = Diet.objects.create(
                name = valid.get('name'),
                description = valid.get('description'),
                image = valid.get('image'),
                price = valid.get('price'),
                # day = valid.get('day'),
                trainer = trainer,
                club = club,
                # owner = owner,
            )
            diet.save()
            return Response({'detail': _('Diet added successfully')})
        
        return Response({'detail': _("There was a problem with adding a diet.")}, status=status.HTTP_400_BAD_REQUEST)

class DeleteDietView(generics.DestroyAPIView):
    def delete(self, request, *args, **kwargs):

        try:
            with transaction.atomic():
                diet_id = self.kwargs['diet_id']
                diet = Diet.objects.get(id = diet_id)
                diet.delete()
                return Response({'detail': _("Diet deleted.")}, status=status.HTTP_200_OK)

        except Diet.DoesNotExist:
            return Response({'detail': _("This diet doesn't exist.")}, status=status.HTTP_400_BAD_REQUEST)

class DietSearchView(generics.ListAPIView):
    serializer_class = DietSerializer

    def get_queryset(self):
        diet_name = self.kwargs['diet_name']

        try:
            return Diet.objects.filter(name__icontains = diet_name)
        except Diet.DoesNotExist:
            return None

class MemberDietShowToOnwer(generics.ListAPIView):
    serializer_class = ProgramSerializer
    
    def get_object(self):
        try:
            club_name = Diet.objects.get(
                owner__user_profile__username = self.kwargs['owner_username'])
            diet = Diet.objects.get(club__name = club_name)
            return DMR.objects.get(diet = diet)
        except DMR.DoesNotExist:
            return None
    
class ClubSearchView(generics.ListAPIView):
    serializer_class = ClubSerializer

    def get_queryset(self):
        club_name = self.kwargs['club_name']

        try:
            return Club.objects.filter(name__icontains = club_name)
        except Club.DoesNotExist:
            return None

class JoinToClubView(generics.GenericAPIView):
    serializer_class = JoinToClubSerializer
    
    def get_object(self):
        try:
            club = Club.objects.get(name = self.request.data.get('club_name'))
            return club
        except:
            return None
    
    def put(self, request, *args, **kwargs):
        s = self.serializer_class(data=request.data)
        s.is_valid(raise_exception=True)
        valid = s.validated_data
        
        club = self.get_object()
        if club!=None:
            member = Member.objects.get(user_profile__username=valid.get('member_username'))
            mcr = MCR.objects.create(
                member = member,
                club = club,
            )
            mcr.save()
            return Response({'detail': _('Member enrolled to this club successfully')})
        
        return Response({'detail': _("There was a problem with enrolling to club.")}, status=status.HTTP_400_BAD_REQUEST)

class EnrollToProgramView(generics.GenericAPIView):
    serializer_class = EnrollProgramSerializer
    
    def get_object(self):
        try:
            program = Program.objects.get(name = self.request.data.get('program_name'))
            return program
        except:
            return None
    
    def put(self, request, *args, **kwargs):
        s = self.serializer_class(data=request.data)
        s.is_valid(raise_exception=True)
        valid = s.validated_data
        
        program = self.get_object()
        member = Member.objects.get(user_profile__username=valid.get('member_username'))
        mcr = MCR.objects.get(member = member, club__name = valid.get('club_name'))
        # if mcr.member==member:
        if program!=None and mcr.member==member:
            mpr = MPR.objects.create(
                member = member,
                program = program,
                is_finished = False
            )
            member.wallet -= program.price
            mpr.save()
            return Response({'detail': _('Member enrolled to this program successfully')})
        
        return Response({'detail': _("There was a problem with enrolling to program.")}, status=status.HTTP_400_BAD_REQUEST)
        
class EnrollToDietView(generics.GenericAPIView):
    serializer_class = EnrollDietSerializer
    
    def get_object(self):
        try:
            diet = diet.objects.get(name = self.request.data.get('diet_name'))
            return diet
        except:
            return None
    
    def put(self, request, *args, **kwargs):
        s = self.serializer_class(data=request.data)
        s.is_valid(raise_exception=True)
        valid = s.validated_data
        
        diet = self.get_object()
        member = Member.objects.get(user_profile__username=valid.get('member_username'))
        mcr = MCR.objects.get(member = member, club__name = valid.get('club_name'))
        # if mcr.member==member:
        if diet!=None and mcr.member==member:
            dmr = DMR.objects.create(
                member = member,
                diet = diet,
                is_finished = False
            )
            dmr.save()
            return Response({'detail': _('Member enrolled to this diet successfully')})
        
        return Response({'detail': _("There was a problem with enrolling to diet.")}, status=status.HTTP_400_BAD_REQUEST)
        

########################################
########################################
########################################

# Bonus Part

class CreateBlogView(generics.GenericAPIView):
    serializer_class = CreateBlogSerializer
    
    def get_object(self):
        try:
            return Trainer.objects.get(
                user_profile__username = self.request.data.get('trainer_username'))
        except Trainer.DoesNotExist:
            return None
        
    def post(self, request, *args, **kwargs):
        s = self.serializer_class(data=request.data)
        s.is_valid(raise_exception=True)
        valid = s.validated_data

        trainer = self.get_object()
        if trainer!=None:
            blog = Blog.objects.create(
                    trainer = trainer,
                    name = valid.get("name"),
                    text = valid.get("text"),
                    image = valid.get("image"),
            )
            blog.save()
            return Response({'detail': _("Blog successfully created.")})
        
        return Response({'detail': _("Problem with creating the Blog.")}, status=status.HTTP_400_BAD_REQUEST)

class BlogView(generics.ListAPIView):
    serializer_class = BlogSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'blog_id'
    
    def get_queryset(self):
        id = self.kwargs['blog_id']
        try:
            return [Blog.objects.filter(id = id)][0]
        except Blog.DoesNotExist:
            return None
    
class BlogListView(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

class BlogLikeView(generics.UpdateAPIView):
    serializer_class = BMRSerializer

    def post(self, request, *args, **kwargs):
        s = self.serializer_class(data=request.data)
        s.is_valid(raise_exception=True)
        valid = s.validated_data

        try:
            member = Member.objects.get(user_profile__username = valid.get('member_username'))
            Blog =  Blog.objects.get(id = self.kwargs['blog_id'])
            emr = BMR.objects.get_or_create(
                Blog = Blog,
                member = member,
            )
            emr[0].isLiked = True
            emr[0].save()
            return Response({'detail': _("You liked the Blog.")}, status=status.HTTP_200_OK)
        except:
            return Response({'detail': _("There was a problem with liking the Blog.")}, status=status.HTTP_400_BAD_REQUEST)

class BlogDislikeView(generics.CreateAPIView):
    serializer_class = BMRSerializer

    def post(self, request, *args, **kwargs):
        s = self.serializer_class(data=request.data)
        s.is_valid(raise_exception=True)
        valid = s.validated_data

        try:
            member = Member.objects.get(user_profile__username = valid.get('member_username'))
            Blog =  Blog.objects.get(id = self.kwargs['blog_id'])
            emr = BMR.objects.get(
                Blog = Blog,
                member = member,
            )
            emr.isLiked = False
            emr.save()
            return Response({'detail': _("You disliked the Blog.")}, status=status.HTTP_200_OK)
        except:
            return Response({'detail': _("There was a problem with disliking the Blog.")}, status=status.HTTP_400_BAD_REQUEST)

class FeedPageView(generics.ListAPIView):
    serializer_class = BlogListSerializer
    ordering_fields = ['likes_count', 'created_at']

    def get_queryset(self):
        try:
            member = Member.objects.get(
                user_profile__username = self.kwargs['member_username'])
            mcr = MCR.objects.get(member=member)
            club = Club.objects.get(id=mcr.club.id)
            tcrs = TCR.objects.filter(club=club)
            for tcr in tcrs:
                trainer = Trainer.objects.get(
                    user_profile__username=tcr.trainer.user_profile.username)
                blogs =Blog.objects.filter(
                            trainer=trainer
                        ) 
                return blogs
        except Blog.DoesNotExist:
            return None

class BlogSearchView(generics.ListAPIView):
    serializer_class = BlogSerializer

    def get_queryset(self):
        text = self.kwargs['text']

        try:
            return Blog.objects.filter(text__icontains = text)
        except Blog.DoesNotExist:
            return None
       
class CreateCouponView(generics.GenericAPIView):
    serializer_class = CreateCouponSerializer
    
    def get_object(self):
        try:
            return Club.objects.get(id = self.kwargs['club_id'])
        except Club.DoesNotExist:
            return None
        
    def post(self, request, *args, **kwargs):
        s = self.serializer_class(data=request.data)
        s.is_valid(raise_exception=True)
        valid = s.validated_data

        club = self.get_object()
        if club!=None:
            member = Member.objects.get(
                        user_profile__username=valid.get("member_username"))
            coupon = Coupon.objects.create(
                    club = club,
                    member = member,
                    percentage = valid.get("percentage"),
            )
            coupon.save()
            return Response({'detail': _("Coupon successfully created.")})
        
        return Response({'detail': _("Problem with creating the Coupon.")}, status=status.HTTP_400_BAD_REQUEST)
     
class CouponListView(generics.ListAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    
class ShowCouponView(generics.ListAPIView):
    serializer_class = CouponSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'coupon_id'
    
    def get_queryset(self):
        id = self.kwargs['coupon_id']
        try:
            return [Coupon.objects.filter(id = id)][0]
        except Coupon.DoesNotExist:
            return None
    
class EnterCouponView(generics.RetrieveAPIView):
    serializer_class = EnterCouponSerializer

    def get_object(self):
        try:
            return Coupon.objects.get(id = self.kwargs['coupon_id'])
        except Coupon.DoesNotExist:
            return None

    def put(self, request, *args, **kwargs):
        user_profile = self.get_object()
        user_request_data = self.serializer_class(data=request.data)
        user_request_data.is_valid(raise_exception=True)
        
        print(user_profile)
        s = self.serializer_class(data=request.data)
        s.is_valid(raise_exception=True)
        valid = s.validated_data
        
        # coupon = self.get_object()
        coupon = Coupon.objects.get(id = self.kwargs['coupon_id'])
        print(coupon)
        try:
            print(valid.get('member_username'))
            member = Member.objects.get(user_profile = user_profile)
            # member = Member.objects.get(
            #         user_profile__usrename=valid.get('member_username'))
            print(member)
            print(coupon.member)
            if (coupon.member == member):
                print("yes")
                program = Program.objects.get(name=valid.get('item_name'))
                diet = Diet.objects.get(name=valid.get('item_name'))
                
                if program!=None:
                    program.price -= (program.price*coupon.percentage)/100
                    program.price.save()
                    return Response({'detail': _("This coupon successfuly used.")}, status=status.HTTP_200_OK)
                
                elif diet!=None:
                    diet.price -= (diet.price*coupon.percentage)/100
                    diet.price.save()
                    return Response({'detail': _("This coupon successfuly used.")}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': _("This user can't user this coupon.")}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'detail': _("There was a problem with using this coupon.")}, status=status.HTTP_400_BAD_REQUEST)
