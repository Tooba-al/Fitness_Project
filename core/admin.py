from django.contrib import admin
from .models import *

admin.site.register(UserProfile)
admin.site.register(UserProfileEmailVerification)
admin.site.register(ForgetPasswordLink)
admin.site.register(Member)
admin.site.register(Club)
admin.site.register(Trainer)
admin.site.register(Owner)
admin.site.register(Event)
admin.site.register(EMR)
