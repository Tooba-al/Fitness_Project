from django.contrib import admin
from .models import *

admin.site.register(UserProfile)
# admin.site.register(UserProfileEmailVerification)
admin.site.register(ForgetPasswordLink)
admin.site.register(Member)
admin.site.register(Trainer)
admin.site.register(Owner)
admin.site.register(Club)
admin.site.register(Event)
admin.site.register(TargetCategory)
admin.site.register(Target)
admin.site.register(UTR)        # UserProfile-Token Relation
admin.site.register(TCR)        # Trainer-Club Relation
admin.site.register(MCR)        # Member-Club Relation
admin.site.register(EMR)        # Event-Members Relation
admin.site.register(Program)
admin.site.register(MPR)        # Member-Program Relation
admin.site.register(Diet)
admin.site.register(DMR)        # Diet-Member Relation

# Bounus Part
admin.site.register(Blog)
admin.site.register(BMR)        # Blog-Member Relation


