from django.contrib import admin
from fitness.models import Sport,user,Exercise,Workout,Routine

# Register your models here.
admin.site.register(Sport)
admin.site.register(user)
admin.site.register(Exercise)
admin.site.register(Workout)
admin.site.register(Routine)