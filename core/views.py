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
                hash = make_password(valid.get("password"))
                user_profile = UserProfile.objects.create(username = valid.get('username'),
                                                        password = hash,
                                                        email = valid.get('email'),
                                                        first_name = valid.get('first_name'),
                                                        last_name = valid.get('last_name'),                                                
                                                        user=User.objects.create(
                                                            username=s.validated_data.get('username')))
                user_profile.save()
                member = Member.objects.create(user_profile = user_profile,
                                                sex = 0,
                                                height = 165,
                                                weight = 60,
                                                wallet = 0)
                member.save()

                return Response({'detail': _("wellcome :)")})

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
            # try:
            with transaction.atomic():
                valid = s.validated_data
                hash = make_password(valid.get("password"))
                user_profile = UserProfile.objects.create(username = valid.get('username'),
                                                        password = hash,
                                                        email = valid.get('email'),
                                                        first_name = valid.get('first_name'),
                                                        last_name = valid.get('last_name'),                                                
                                                        user=User.objects.create(
                                                        username=s.validated_data.get('username')))
                owner = Owner.objects.create(
                    user_profile = user_profile,
                )
                club = Club.objects.create(
                    owner = owner,
                    name = valid.get('club_name'),
                    address = valid.get('club_address'),
                )
                #wallet = Wallet.objects.create(owner = user_profile)
                #user_profile.wallet = wallet
                user_profile.save()
                owner.save()
                club.save()

                # upv = UserProfileEmailVerification.objects.create(user_profile=self.get_object())

                # if upv['status'] != 201:
                #     return Response({'detail': _("Code not sent"), 'wait': upv['wait']}, status=upv['status'])

                # if settings.DEBUG:
                #     return Response({'detail': _("Code sent"), 'code': upv['code']})

                return Response({'detail': _("wellcome!")})

            # except:
            #     return Response({'detail': _("Problem with signing up")}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': _("This profile already exists.")}, status=status.HTTP_400_BAD_REQUEST)

# class TrainerSignUpView(generics.GenericAPIView):
#     """
#         Send verification code
#         if send failed respond with wait time
#     """

#     serializer_class = TrainerSignUpSerializer

#     def get_object(self):
#         email = self.request.data.get('email')
#         username = self.request.data.get('username')

#         try:
#             return UserProfile.objects.get_if_available(username, email)
#         except UserProfile.DoesNotExist:
#             return None

#     def post(self, request, *args, **kwargs):
#         s = self.serializer_class(data=request.data)
#         s.is_valid(raise_exception=True)

#         user_profile = self.get_object()

#         if not user_profile:
#             try:
#                 with transaction.atomic():
#                     valid = s.validated_data
#                     hash = make_password(valid.get("password"))
#                     user_profile = UserProfile.objects.create(username = valid.get('username'),
#                                                             password = hash,
#                                                             club_name = valid.get('club_name'),
#                                                             email = valid.get('email'),
#                                                             first_name = valid.get('first_name'),
#                                                             last_name = valid.get('last_name'),                                                
#                                                             user=User.objects.create(
#                                                             username=s.validated_data.get('username')))
#                     owner = Owner.objects.create(
#                         user_profile = user_profile,
#                     )
#                     #wallet = Wallet.objects.create(owner = user_profile)
#                     #user_profile.wallet = wallet
#                     user_profile.save()
#                     owner.save()

#                     upv = UserProfileEmailVerification.objects.create(user_profile=self.get_object())

#                     if upv['status'] != 201:
#                         return Response({'detail': _("Code not sent"), 'wait': upv['wait']}, status=upv['status'])

#                     if settings.DEBUG:
#                         return Response({'detail': _("Code sent"), 'code': upv['code']})

#                     return Response({'detail': _("Code sent")})

#             except:
#                 return Response({'detail': _("Problem with signing up")}, status=status.HTTP_400_BAD_REQUEST)

#         return Response({'detail': _("This profile already exists.")}, status=status.HTTP_400_BAD_REQUEST)

class RetrieveUserProfileDataView(generics.RetrieveAPIView):
# class RetrieveUserProfileDataView(generics.GenericAPIView):
    # serializer_class = UserDataSerializer
    serializer_class = UserProfileDataSerializer
    # permission_classes = (IsAuthenticated,)

    def get_object(self):
        try:
            # username = self.request.data.get('username')
            # user_profile = UserProfile.objects.get(username = username)
            # return UserProfileDataSerializer(instance = user_profile).data
            return (self.request.user)
        except UserProfile.DoesNotExist:
            return None


    # def post(self, request, *args, **kwargs):
    #     username = request.data.get('username')
    #     print("username: ", username)
    #     try:
    #         user_profile = UserProfile.objects.get(username = username)
    #     except:
    #         user_profile = None
            
    #     print(user_profile)
        
    #     if user_profile!=None:
    #         data = UserProfileDataSerializer(instance = user_profile).data
    #         # data = self.get_object()

    #         return Response({'data:': data,})
    #     return Response({'detail': _('Nothing to return.'),}, status=status.HTTP_404_NOT_FOUND)


class RetrieveUserProfileEditView(generics.RetrieveUpdateAPIView):
# class RetrieveUserProfileEditView(generics.GenericAPIView):
    # serializer_class = UserDataSerializer
    serializer_class = UserProfileDataSerializer
    # permission_classes = (IsAuthenticated,)

    def get_object(self):
        try:
            # username = self.request.data.get('username')
            # user_profile = UserProfile.objects.get(username = username)
            # return UserProfileDataSerializer(instance = user_profile).data
            return (self.request.user)
        except UserProfile.DoesNotExist:
            return None

    # def get_object(self):
    #     try:
    #         username = self.request.data.get('user_username')
    #         user_profile = UserProfile.objects.get(user__username = username)
    #         return user_profile
    #     except UserProfile.DoesNotExist:
    #         return None



# class UserProfileAuthTokenView(generics.CreateAPIView):
#     """
#         match Email and verification code
#         return user token on success
#     """

#     serializer_class = UserProfileEmailVerificationSerializer

#     def post(self, request, *args, **kwargs):

#         email = request.data.get('email')
#         code = request.data.get('code')

#         user_profile_email_ = UserProfileEmailVerification.objects.order_by('created_at'). \
#             filter(
#             query_times__lt=UserProfileEmailVerification.MAX_QUERY,
#             used=False,
#             burnt=False,
#             user_profile__email=email
#         )
#         user_profile_email = user_profile_email_.last()

#         if not user_profile_email:
#             return Response({'detail': _('Email not found')}, status=status.HTTP_404_NOT_FOUND)

#         if code != user_profile_email.code:
#             user_profile_email.query_times += 1
#             user_profile_email.save()

#             return Response({'detail': _('Invalid verification code'),
#                              'allowed_retry_times':
#                                  UserProfileEmailVerification.MAX_QUERY -
#                                  user_profile_email.query_times},
#                             status=status.HTTP_403_FORBIDDEN)

#         user_profile_email.user_profile.save()
#         token, created = Token.objects.get_or_create(user=user_profile_email.user_profile.user)

#         user_profile_email.used = True
#         user_profile_email.save()

#         # mark all other codes as burnt
#         user_profile_email_.update(burnt=True)

#         #return Response({'phone_number': phone, 'token': token.key})
#         return Response({'detail': _('You are verified.'), 'token': token.key})

class LoginView(generics.GenericAPIView):

    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):

        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user_profile = UserProfile.objects.get(username = username)
        except:
            user_profile = None

        if not user_profile:
            return Response({'detail': _('Username not found')}, status=status.HTTP_404_NOT_FOUND)
        # try:
        if(check_password(password, user_profile.password)):
            # token = Token.objects.get(user=user_profile.user)
            data = UserProfileDataSerializer(instance = user_profile).data
            # return Response({'data': data, 'token': token.key})
            return Response({'data': data,})
        else:
            return Response({'detail': _('Wrong password'),}, status=status.HTTP_404_NOT_FOUND)
        # except:
        #     return Response({'detail': _('You may not be verified yet.'),}, status=status.HTTP_404_NOT_FOUND)


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
    # permission_classes = [IsAuthenticated,]
    # filter_backends = [filters.OrderingFilter]
    # ordering_fields = ['id']

class ShowOwnerListView(generics.ListAPIView):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    # permission_classes = [IsAuthenticated,]
    # filter_backends = [filters.OrderingFilter]
    # ordering_fields = ['name']

class ShowTrainerListView(generics.ListAPIView):
    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer
    # permission_classes = [IsAuthenticated,]
    # filter_backends = [filters.OrderingFilter]
    # ordering_fields = ['name']

class ShowClubListView(generics.ListAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    # permission_classes = [IsAuthenticated,]
    # filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name']
    
class ProgramListView(generics.ListAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramListSerializer
    # permission_classes = [IsAuthenticated,]
    # filter_backends = [filters.OrderingFilter]
    # ordering_fields = ['name']
    
class DietListView(generics.ListAPIView):
    queryset = Diet.objects.all()
    serializer_class = ProgramListSerializer
    # permission_classes = [IsAuthenticated,]
    # filter_backends = [filters.OrderingFilter]
    # ordering_fields = ['name']
    
# class AddEventView(generics.CreateAPIView):
#     serializer_class = CreateEventSerializer
#     queryset = Event.objects.all()
#     # permission_classes = [IsOwner,]

#     def perform_create(self, serializer):
#         with transaction.atomic():
#             event = serializer.save(care_giver=self.request.user.user_profile.owner)
#             event.save()

# class CreateEventView(generics.GenericAPIView):
#     serializer_class = CreateEventSerializer

#     def get_object(self):
#         username = self.request.data.get('username')

#         try:
#             return UserProfile.objects.get(username=username)
#         except UserProfile.DoesNotExist:
#             return None

#     def post(self, request, *args, **kwargs):
#         s = self.serializer_class(data=request.data)
#         s.is_valid(raise_exception=True)

#         user_profile = self.get_object()

#         if not user_profile:
#             try:
#                 with transaction.atomic():
#                     valid = s.validated_data
#                     # hash = make_password(valid.get("password"))
#                     user_profile = UserProfile.objects.create(username = valid.get('username'),
#                                                         # password = hash,
#                                                         password = valid.get('password'),
#                                                         user=User.objects.create(
#                                                             username=s.validated_data.get('username')))
                    
#                     user_profile.save()
#                     owner = Owner.objects.get()
#                     # user_profile.save(using='secondary')
#                     event = Event.objects.create(
#                             user = user_profile,
#                             ap = 100,  
#                             coins = 100,  
#                             has_disaster = False,  
#                     )
#                     group.save()
#                     initial_cat = ["Primary", "Primary", "Primary", "Secondary", "Secondary", "Secondary", "Secondary"]
#                     initial_name = ["Water", "Food", "Fuel", "Iron", "Copper", "Gold", "Diamond"]
#                     initial_val = [0.1, 0.1, 0.1, 1, 2, 5, 13]
#                     for index in range(6):
#                         resource = Resource.objects.create(
#                                 name = initial_name[index],
#                                 amount = initial_val[index],
#                                 price = 0,
#                                 category = initial_cat[index],
#                         )
#                         resource.save()
#                         rgr = RGR.objects.create(
#                             group = group,
#                             resource = resource,
#                         )
#                         rgr.save()
#                     ini_name = ["Power", "Wealth", "Fame"]
#                     for index in range(3):
#                         point = Point.objects.create(
#                                 name = ini_name[index],
#                                 amount = 10,
#                         )
#                         point.save()
#                         pgr = PGR.objects.create(
#                             group = group,
#                             point = point,
#                         )
#                         pgr.save()
#                     # group.save(using='secondary')
#                     return Response({'detail': _("Group successfully added")})
#             except:
#                 return Response({'detail': _("Problem with signing up")}, status=status.HTTP_400_BAD_REQUEST)

#         return Response({'detail': _("This profile already exists.")}, status=status.HTTP_400_BAD_REQUEST)
        

# class RejisterEventView(generics.GenericAPIView):
#     serializer_class = EMRSerializer
#     # permission_classes = [IsMember,]

#     def put(self, request, *args, **kwargs):
#         user_request_data = self.serializer_class(data=request.data)
#         user_request_data.is_valid(raise_exception=True)
    
#         try:
#             with transaction.atomic():
#                 member = self.request.user.user_profile.member
#                 event_id = self.kwargs['request_id']
#                 event = Event.objects.get(id = event_id)
#                 emr = EMR.objects.get(event = event, member = member)
#                 emr.isRegistered = True
#                 emr.save()
                    
#                 return Response({'detail': _("You registered to this event.")}, status=status.HTTP_200_OK)
#         except:
#             return Response({'detail': _("There was a problem with registering to this event.")}, status=status.HTTP_400_BAD_REQUEST)


# class UnrejisterEventRequestView(generics.GenericAPIView):
#     serializer_class = EMRSerializer
#     # permission_classes = [IsMember,]

#     def put(self, request, *args, **kwargs):
#         user_request_data = self.serializer_class(data=request.data)
#         user_request_data.is_valid(raise_exception=True)
        
#         try:
#             with transaction.atomic():
#                 member = self.request.user.user_profile.member
#                 event_id = self.kwargs['request_id']
#                 event = Event.objects.get(id = event_id)
#                 emr = EMR.objects.get(event = event, member = member)
#                 emr.isRegistered = False
#                 emr.save()
                    
#                 return Response({'detail': _("You registered to this event.")}, status=status.HTTP_200_OK)
#         except:
#             return Response({'detail': _("There was a problem with registering to this event.")}, status=status.HTTP_400_BAD_REQUEST)

    
# class EventView(generics.RetrieveAPIView):
#     queryset = Event.objects.all()
#     serializer_class = EventSerializer
#     lookup_field = 'id'
#     lookup_url_kwarg = 'event_id'
#     # permission_classes = [IsAuthenticated,]

# class ShowEventListView(generics.ListAPIView):
#     queryset = Event.objects.all()
#     serializer_class = EventSerializer
#     # permission_classes = [IsAuthenticated,]
#     # filter_backends = [filters.OrderingFilter]
#     # ordering_fields = ['name']

class MemberSearchView(generics.ListAPIView):
    serializer_class = MemberSerializer
    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        member_username = self.kwargs['member_username']

        try:
            # first = Member.objects.filter(user_profile__first_name__icontains = member_name)
            # last = Member.objects.filter(user_profile__last_name__icontains = member_name)
            # username = Member.objects.filter(user_profile__username__icontains = member_name)
            return Member.objects.filter(user_profile__username__icontains = member_username)
        except Member.DoesNotExist:
            return None

class TrainerSearchView(generics.ListAPIView):
    serializer_class = TrainerSerializer
    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        trainer_username = self.kwargs['trainer_username']

        try:
            # first = Member.objects.filter(user_profile__first_name__icontains = member_name)
            # last = Member.objects.filter(user_profile__last_name__icontains = member_name)
            # username = Member.objects.filter(user_profile__username__icontains = member_name)
            return Trainer.objects.filter(user_profile__username__icontains = trainer_username)
        except Trainer.DoesNotExist:
            return None

class OwnerSearchView(generics.ListAPIView):
    serializer_class = OwnerSerializer
    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        owner_username = self.kwargs['owner_username']

        try:
            # first = Member.objects.filter(user_profile__first_name__icontains = member_name)
            # last = Member.objects.filter(user_profile__last_name__icontains = member_name)
            # username = Member.objects.filter(user_profile__username__icontains = member_name)
            return Owner.objects.filter(user_profile__username__icontains = owner_username)
        except Owner.DoesNotExist:
            return None

class AddToWalletView(generics.RetrieveAPIView):
    queryset = Member.objects.all()
    serializer_class = AddToWalletSerializer

    def get_object(self):
        try:
            username = self.request.data.get('username')
            user_profile = UserProfile.objects.get(user_profile__username = username)
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
                
                # member = Member.objects.get(self.request.user.user_profile)
                member = Member.objects.get(user = user_profile)
                member.wallet.remove()
                member.wallet.add(wallet = AddToWalletSerializer.get_wallet_data + valid.get('amount'))
                member.save()
                    
                return Response({'detail': _("Your wallet successfuly updated.")}, status=status.HTTP_200_OK)
        except:
            return Response({'detail': _("There was a problem with updating your wallet.")}, status=status.HTTP_400_BAD_REQUEST)

class AddTrainerView(generics.GenericAPIView):
    # queryset = Owner.objects.all()
    # lookup_field = 'id'
    # lookup_url_kwarg = 'owner_username'
    serializer_class = AddTrainerSerializer
    # permission_classes = (IsAuthenticated,)
    
    def get_object(self):
        try:
            username = self.request.data.get('owner_username')
            owner = Owner.objects.get(user_profile__username = username)
            return owner
        except UserProfile.DoesNotExist:
            return None
    
    def put(self, request, *args, **kwargs):
        s = self.serializer_class(data=request.data)
        s.is_valid(raise_exception=True)
        valid = s.validated_data
        
        owner = self.get_object()
        
        if owner!=None:
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
            return Response({'detail': _('Trainer added successfully')})
        
        return Response({'detail': _("There was a problem with adding a trainer.")}, status=status.HTTP_400_BAD_REQUEST)


class CreateProgramView(generics.GenericAPIView):
    serializer_class = ProgramSerializer
    
    def get_object(self):
        try:
            username = self.request.data.get('owner_username')
            owner = Owner.objects.get(user_profile__username = username)
            return owner
        except UserProfile.DoesNotExist:
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
                # owner = owner,
            )
            program.save()
            return Response({'detail': _('Program added successfully')})
        
        return Response({'detail': _("There was a problem with adding a program.")}, status=status.HTTP_400_BAD_REQUEST)

class ProgramSearchView(generics.ListAPIView):
    serializer_class = ProgramSerializer
    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        program_name = self.kwargs['program_name']

        try:
            return Program.objects.filter(name__icontains = program_name)
        except Program.DoesNotExist:
            return None


class MemberProgramShowToOnwer(generics.ListAPIView):
    # queryset = Program.objects.all()
    # serializer_class = MemberProgramShowToOwnerSerializer
    serializer_class = ProgramSerializer
    
    def get_object(self):
        try:
            club_name = Club.objects.get(
                owner__user_profile__username = self.kwargs['owner_username'])
            program = Program.objects.get(club__name = club_name)
            return MPR.objects.get(program = program)
        except MPR.DoesNotExist:
            return None
    
    # def get_object(self):
    #     try:
    #         club_name = self.request.data.get('club_name')
    #         club = Club.objects.get(name = club_name)
    #         return club
    #     except Club.DoesNotExist:
    #         return None
    
    # def put(self, request, *args, **kwargs):
    #     s = self.serializer_class(data=request.data)
    #     s.is_valid(raise_exception=True)
    #     valid = s.validated_data
        
    #     club = self.get_object()
        
    #     if club!=None:
    #         data = self.serializer_class.objects.get(
    #              = program_data.club.name
    #         )
    #         return Response({'data': data})
        
    #     return Response({'detail': _("There was a problem with adding a trainer.")}, status=status.HTTP_400_BAD_REQUEST)



class CreateDietView(generics.GenericAPIView):
    serializer_class = ProgramSerializer
    
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
                day = valid.get('day'),
                trainer = trainer,
                club = club,
                # owner = owner,
            )
            diet.save()
            return Response({'detail': _('Diet added successfully')})
        
        return Response({'detail': _("There was a problem with adding a diet.")}, status=status.HTTP_400_BAD_REQUEST)

class DietSearchView(generics.ListAPIView):
    serializer_class = DietSerializer
    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        diet_name = self.kwargs['diet_name']

        try:
            return Diet.objects.filter(name__icontains = diet_name)
        except Diet.DoesNotExist:
            return None


# class MemberDietShowToOnwer(generics.ListAPIView):
#     # queryset = Diet.objects.all()
#     serializer_class = ProgramSerializer
    
#     def get_object(self):
#         try:
#             club_name = Diet.objects.get(
#                 owner__user_profile__username = self.kwargs['owner_username'])
#             diet = Diet.objects.get(club__name = club_name)
#             return DMR.objects.get(diet = diet)
#         except DMR.DoesNotExist:
#             return None
    
class ClubSearchView(generics.ListAPIView):
    serializer_class = ClubSerializer
    # permission_classes = (IsAuthenticated,)

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
            mpr.save()
            return Response({'detail': _('Member enrolled to this club successfully')})
        
        return Response({'detail': _("There was a problem with enrolling to club.")}, status=status.HTTP_400_BAD_REQUEST)
        
        # return Response({'detail': _("You are not joint to this club.")})
