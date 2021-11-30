from django.contrib import admin
from .models import Playername, Teamname, Playerscores
# Register your models here.

admin.site.register(Teamname)
admin.site.register(Playername)
admin.site.register(Playerscores)
