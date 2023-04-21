from django.contrib import admin
from store import models

admin.site.register(models.Category)
admin.site.register(models.Image)
admin.site.register(models.Review)
admin.site.register(models.Tag)

class ImageAdmin(admin.TabularInline):
    model = models.Image

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):

    inlines = [
        ImageAdmin,
    ]