from django.contrib import admin
from . import models

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'title_uz',
        'title_ru',
        'title_en',
        'description_uz',
        'description_ru',
        'description_en',
        'priority',
    ]

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'title_uz',
        'title_ru',
        'title_en',
        'description_uz',
        'description_ru',
        'description_en',
    ]

@admin.register(models.ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['uuid']

@admin.register(models.Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = [
        'title_uz',
        'title_ru',
        'title_en',
        'description_uz',
        'description_ru',
        'description_en',
    ]

@admin.register(models.Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = [
        'title_uz',
        'title_ru',
        'title_en',
        'description_uz',
        'description_ru',
        'description_en',
    ]


@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = [
        'title_uz',
        'title_ru',
        'title_en',
        'description_uz',
        'description_ru',
        'description_en',
    ]


@admin.register(models.CompanyAddress)
class CompanyAddressAdmin(admin.ModelAdmin):
    list_display = [
        'address_uz',
        'address_ru',
        'address_en',
    ]

@admin.register(models.CompanyImage)
class CompanyImageAdmin(admin.ModelAdmin):
    list_display = []

@admin.register(models.CompanyPhone)
class CompanyPhoneAdmin(admin.ModelAdmin):
    list_display = ['uuid']

@admin.register(models.CompanyEmail)
class CompanyEmailAdmin(admin.ModelAdmin):
    list_display = ['uuid']

@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['uuid']
