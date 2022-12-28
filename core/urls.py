from django.urls import path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from .views import *

schema_view = get_schema_view(
    openapi.Info(
        title="Fitness API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="toobaaliabadi@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('owner/signup/', OwnerSignUpView.as_view()),
    path('user/signup/', UserSignUpView.as_view()),
    path('user/login/', LoginView.as_view()),
    path('forget-password/', ForgetPasswordView.as_view()),
    # path('change-password/<str:change_link>/', ChangePasswordView.as_view()),
    path('change-password/', ChangePasswordView.as_view()),
    path('resend-code/', ResendVerificationCodeView.as_view()),
    # path('verify-email/', UserProfileAuthTokenView.as_view()),
    path('profile/data/', RetrieveUserProfileDataView.as_view()),
    path('profile/edit/', RetrieveUserProfileEditView.as_view()),
    path('profile/add-to-wallet/', AddToWalletView.as_view()),
    
    path('member/list/', ShowMemberListView.as_view()),
    path('member/join/club/', JoinToClubView.as_view()),
    path('member/enroll/program/', EnrollToProgramView.as_view()),
    # path('member/enroll/diet/', .as_view()),
    
    path('owner/list/', ShowOwnerListView.as_view()),
    path('club/list/', ShowClubListView.as_view()),
    
    path('event/create/', AddToWalletView.as_view()),
    
    path('trainer/list/', ShowTrainerListView.as_view()),
    path('trainer/add/', AddTrainerView.as_view()),
    
    path('program/create/', CreateProgramView.as_view()),
    path('program/list/', ProgramListView.as_view()),
    
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]