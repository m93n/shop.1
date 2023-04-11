from django.contrib import admin
from store import models

admin.site.register(models.Category)
admin.site.register(models.Product)
admin.site.register(models.Image)
admin.site.register(models.Review)
admin.site.register(models.Tag)