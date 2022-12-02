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
    # def post(self, request, *args, **kwargs):
    #     s = self.get_serializer(data=request.data)
    #     s.is_valid(raise_exception=True)
    #     user = UserProfile.objects.create(s.validated_data['username'], 
    #                                     s.validated_data['email'], 
    #                                     s.validated_data['password'], 
    #                                     s.validated_data['first_name'],
    #                                     s.validated_data['last_name'],)
    #     user = s.save()
    #     return Response({
    #     "user": UserSignUpSerializer(user
    #                                 , context=self.get_serializer_context()).data,
    #     # "token": AuthToken.objects.create(user)[1]
    #     })

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

                # upv = UserProfileEmailVerification.objects.create(user_profile=self.get_object())
                # if upv['status'] != 201:
                #     return Response({'detail': _("Code not sent"), 'wait': upv['wait']}, status=upv['status'])

                # if settings.DEBUG:
                #     return Response({'detail': _("Code sent"), 'code': upv['code']})

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
            try:
                with transaction.atomic():
                    valid = s.validated_data
                    hash = make_password(valid.get("password"))
                    user_profile = UserProfile.objects.create(username = valid.get('username'),
                                                            password = hash,
                                                            club_name = valid.get('club_name'),
                                                            club_address = valid.get('club_address'),
                                                            email = valid.get('email'),
                                                            first_name = valid.get('first_name'),
                                                            last_name = valid.get('last_name'),                                                
                                                            user=User.objects.create(
                                                            username=s.validated_data.get('username')))
                    owner = Owner.objects.create(
                        user_profile = user_profile,
                    )
                    #wallet = Wallet.objects.create(owner = user_profile)
                    #user_profile.wallet = wallet
                    user_profile.save()
                    owner.save()

                    # upv = UserProfileEmailVerification.objects.create(user_profile=self.get_object())

                    # if upv['status'] != 201:
                    #     return Response({'detail': _("Code not sent"), 'wait': upv['wait']}, status=upv['status'])

                    # if settings.DEBUG:
                    #     return Response({'detail': _("Code sent"), 'code': upv['code']})

                    return Response({'detail': _("Code sent")})

            except:
                return Response({'detail': _("Problem with signing up")}, status=status.HTTP_400_BAD_REQUEST)

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
    serializer_class = UserProfileDataSerializer
    # permission_classes = (IsAuthenticated,)

    def get_object(self):
        try:
            return self.request.user.user_profile
        except UserProfile.DoesNotExist:
            return None


class RetrieveUserProfileEditView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileDataEditSerializer
    # permission_classes = (IsAuthenticated,)

    def get_object(self):
        try:
            return self.request.user.user_profile
        except UserProfile.DoesNotExist:
            return None


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
        try:
            if(check_password(password, user_profile.password)):
                token = Token.objects.get(user=user_profile.user)
                data = UserProfileDataSerializer(instance = user_profile).data
                return Response({'data': data, 'token': token.key})
            else:
                return Response({'detail': _('Wrong password'),}, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({'detail': _('You may not be verified yet.'),}, status=status.HTTP_404_NOT_FOUND)


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
                change_link = self.kwargs['change_link']

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
    
class AddEventView(generics.CreateAPIView):
    serializer_class = CreateEventSerializer
    queryset = Event.objects.all()
    # permission_classes = [IsOwner,]

    def perform_create(self, serializer):
        with transaction.atomic():
            event = serializer.save(care_giver=self.request.user.user_profile.owner)
            event.save()


class SendEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'capacity', 'attachment']

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

class RejisterEventView(generics.GenericAPIView):
    serializer_class = EMRSerializer
    # permission_classes = [IsMember,]

    def put(self, request, *args, **kwargs):
        user_request_data = self.serializer_class(data=request.data)
        user_request_data.is_valid(raise_exception=True)
    
        try:
            with transaction.atomic():
                member = self.request.user.user_profile.member
                event_id = self.kwargs['request_id']
                event = Event.objects.get(id = event_id)
                emr = EMR.objects.get(event = event, member = member)
                emr.isRegistered = True
                emr.save()
                    
                return Response({'detail': _("You registered to this event.")}, status=status.HTTP_200_OK)
        except:
            return Response({'detail': _("There was a problem with registering to this event.")}, status=status.HTTP_400_BAD_REQUEST)


class UnrejisterEventRequestView(generics.GenericAPIView):
    serializer_class = EMRSerializer
    # permission_classes = [IsMember,]

    def put(self, request, *args, **kwargs):
        user_request_data = self.serializer_class(data=request.data)
        user_request_data.is_valid(raise_exception=True)
        
        try:
            with transaction.atomic():
                member = self.request.user.user_profile.member
                event_id = self.kwargs['request_id']
                event = Event.objects.get(id = event_id)
                emr = EMR.objects.get(event = event, member = member)
                emr.isRegistered = False
                emr.save()
                    
                return Response({'detail': _("You registered to this event.")}, status=status.HTTP_200_OK)
        except:
            return Response({'detail': _("There was a problem with registering to this event.")}, status=status.HTTP_400_BAD_REQUEST)

    
class EventView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'event_id'
    # permission_classes = [IsAuthenticated,]

class ShowEventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    # permission_classes = [IsAuthenticated,]
    # filter_backends = [filters.OrderingFilter]
    # ordering_fields = ['name']

class AddToWalletView(generics.RetrieveAPIView):
    queryset = Member.objects.all()
    serializer_class = AddToWalletSerializer

    def put(self, request, *args, **kwargs):
        user_request_data = self.serializer_class(data=request.data)
        user_request_data.is_valid(raise_exception=True)
        
        try:
            with transaction.atomic():
                valid = user_request_data.validated_data
                
                member = Member.objects.get(self.request.user.user_profile)
                member.wallet.remove()
                member.wallet.add(wallet = AddToWalletSerializer.get_wallet_data + valid.get('wallet'))
                member.save()
                    
                return Response({'detail': _("Your wallet successfuly updated.")}, status=status.HTTP_200_OK)
        except:
            return Response({'detail': _("There was a problem with updating your wallet.")}, status=status.HTTP_400_BAD_REQUEST)


