from django.contrib import admin
from .models import *

admin.site.register(UserProfile)
admin.site.register(UserProfileEmailVerification)
admin.site.register(Member)
admin.site.register(Club)
admin.site.register(Owner)