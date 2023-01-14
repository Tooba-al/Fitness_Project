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
    
    path('search/owner/<str:owner_username>/', OwnerSearchView.as_view()),
    path('search/trainer/<str:trainer_username>/', TrainerSearchView.as_view()),
    path('search/member/<str:member_username>/', MemberSearchView.as_view()),
    path('search/program/<str:program_name>/', ProgramSearchView.as_view()),
    path('search/diet/<str:diet_name>/', DietSearchView.as_view()),
    path('search/club/<str:club_name>/', ClubSearchView.as_view()),
    path('search/education/<str:text>/', EducationSearchView.as_view()),
    
    path('member/<str:memver_username>/', MemberView.as_view()),
    path('member/list/', ShowMemberListView.as_view()),
    path('member/join/club/', JoinToClubView.as_view()),
    path('member/enroll/program/', EnrollToProgramView.as_view()),
    path('member/enroll/diet/', EnrollToDietView.as_view()),
    
    path('owner/list/', ShowOwnerListView.as_view()),
    path('club/list/', ShowClubListView.as_view()),
    path('owner/mem-prog/list/<str:owner_username>/', MemberProgramShowToOnwer.as_view()),
    
    path('event/create/', CreateEventView.as_view()),
    path('event/<int:request_id>/register/', RejisterEventView.as_view()),
    path('event/<int:request_id>/unregister/', UnrejisterEventView.as_view()),
    path('event/list/', ShowEventListView.as_view()),
    
    path('trainer/list/', ShowTrainerListView.as_view()),
    path('trainer/add/', AddTrainerView.as_view()),
    
    path('program/create/', CreateProgramView.as_view()),
    path('program/list/', ProgramListView.as_view()),
    path('program/<int:program_id>/', ProgramView.as_view()),
    
    path('diet/create/', CreateDietView.as_view()),
    path('diet/list/', DietListView.as_view()),
    path('diet/<int:diet_id>/', DietView.as_view()),
    
    path('education/create/', CreateEducationView.as_view()),
    # path('education/delete/', DeleteEducationView.as_view()),
    path('education/<int:education_id>/like/', EducationLikeView.as_view()),
    path('education/<int:education_id>/dislike/', EducationDislikeView.as_view()),
    path('education/feed-page/', FeedPageForEducationView.as_view()),
    path('education/<int:education_id>/', EducationView.as_view()),
    
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]