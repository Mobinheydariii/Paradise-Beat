from django.contrib import admin
from . import models


admin.site.register(models.Beat)
admin.site.register(models.Category)
admin.site.register(models.BasicBeatLicence)
admin.site.register(models.PermiumBeatLicence)