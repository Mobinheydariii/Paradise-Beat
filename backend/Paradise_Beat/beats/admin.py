from django.contrib import admin
from . import models


admin.site.register(models.Beat)
admin.site.register(models.Category)
admin.site.register(models.BeatLicence)
admin.site.register(models.LicenceType)