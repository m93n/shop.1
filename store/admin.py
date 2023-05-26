from django.contrib import admin
from nested_inline.admin import NestedTabularInline, NestedModelAdmin, NestedStackedInline
from store import models

admin.site.register(models.Category)
admin.site.register(models.Image)
admin.site.register(models.Tag)
admin.site.register(models.Profile)

class AdditionalInformationValueAdmin(NestedTabularInline):
    model = models.AdditionalInformationValue

class AdditionalInformationAdmin(NestedStackedInline):
    model = models.AdditionalInformation

    inlines = [
        AdditionalInformationValueAdmin,
    ]

class ImageAdmin(NestedTabularInline):
    model = models.Image

@admin.register(models.Product)
class ProductAdmin(NestedModelAdmin):

    readonly_fields = ['avarage_rate', 'created']
    inlines = [
        ImageAdmin,
        AdditionalInformationAdmin,
    ]

@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):

    readonly_fields = ['created']

class OrderItemAdmin(admin.TabularInline):
    model = models.OrderItem
    fieldsets = [
        ('Product', {'fields': ['product'], }),
        ('Quantity', {'fields': ['quantity'], }),
        ('Price', {'fields': ['price'], }),
    ]
    readonly_fields = ['product', 'quantity', 'price']
    can_delete = False
    max_num = 0


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'billingName', 'emailAddress', 'created']
    list_display_links = ('id', 'billingName')
    search_fields = ['id', 'billingName', 'emailAddress']
    readonly_fields = ['id', 'token', 'total', 'emailAddress', 'created',
                       'billingName', 'billingAddress1', 'billingCity', 'billingPostcode',
                       'billingCountry', 'shippingName', 'shippingAddress1', 'shippingCity',
                       'shippingPostcode', 'shippingCountry']

    fieldsets = [
        ('ORDER INFORMATION', {'fields': ['id', 'token', 'total', 'created']}),
        ('BILLING INFORMATION', {'fields': ['billingName', 'billingAddress1',
                                            'billingCity', 'billingPostcode', 'billingCountry', 'emailAddress']}),
        ('SHIPPING INFORMATION', {'fields': ['shippingName', 'shippingAddress1',
                                             'shippingCity', 'shippingPostcode', 'shippingCountry']}),
    ]

    inlines = [
        OrderItemAdmin,
    ]

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False
    