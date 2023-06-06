from django.contrib import admin

from nested_inline.admin import NestedTabularInline, NestedModelAdmin, NestedStackedInline

from store.models import (Category, Image, AdditionalInformation, 
                        Tag, AdditionalInformationValue, Review,
                        Product, 
)

admin.site.register(Category)
admin.site.register(Image)
admin.site.register(Tag)

class AdditionalInformationValueAdmin(NestedTabularInline):
    model = AdditionalInformationValue

class AdditionalInformationAdmin(NestedStackedInline):
    model = AdditionalInformation

    inlines = [
        AdditionalInformationValueAdmin,
    ]

class ImageAdmin(NestedTabularInline):
    model = Image

@admin.register(Product)
class ProductAdmin(NestedModelAdmin):

    readonly_fields = ['avarage_rate', 'created']
    inlines = [
        ImageAdmin,
        AdditionalInformationAdmin,
    ]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    readonly_fields = ['created']
