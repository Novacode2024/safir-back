from django.db import models
from shortuuidfield import ShortUUIDField
from django_resized import ResizedImageField


class Main(models.Model):
    uuid = ShortUUIDField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(Main):
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    description_uz = models.TextField()
    description_ru = models.TextField()
    description_en = models.TextField()
    image = models.ImageField(upload_to='category_images/')
    priority = models.IntegerField(default=0)

    def __str__(self):
        return self.title_uz
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ('priority',)


class Product(Main):
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    description_uz = models.TextField()
    description_ru = models.TextField()
    description_en = models.TextField()
    price = models.DecimalField(max_digits=20, decimal_places=2)
    
    image_min = ResizedImageField(size = [300,300], quality=100, upload_to='product_images/300/')
    image_max = ResizedImageField(size = [600,600], quality=100, upload_to='product_images/600/')

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    priority = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title_uz

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ('priority',)


class ProductImage(Main):
    image_min = ResizedImageField(size = [300,300], quality=100, upload_to='product_images/300/')
    image_max = ResizedImageField(size = [600,600], quality=100, upload_to='product_images/600/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.title_uz

    class Meta:
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'
        ordering = ('-created_at',)


class Slider(Main):
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    description_uz = models.TextField()
    description_ru = models.TextField()
    description_en = models.TextField()

    image_min = ResizedImageField(size = [300,300], quality=100, upload_to='product_images/300/', null=True, blank=True)
    image_max = ResizedImageField(size = [1200,600], quality=100, upload_to='product_images/600/', null=True, blank=True)

    priority = models.IntegerField(default=0)

    def __str__(self):
        return self.title_uz

    class Meta:
        verbose_name = 'Slider'
        verbose_name_plural = 'Sliders'
        ordering = ('priority',)


class Blog(Main):
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    description_uz = models.TextField()
    description_ru = models.TextField()
    description_en = models.TextField()

    image_min = ResizedImageField(size = [300,300], quality=100, upload_to='product_images/300/', null=True, blank=True)
    image_max = ResizedImageField(size = [1200,600], quality=100, upload_to='product_images/600/', null=True, blank=True)

    priority = models.IntegerField(default=0)

    def __str__(self):
        return self.title_uz

    class Meta:
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'
        ordering = ('priority',)



class Company(Main):
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    
    description_uz = models.TextField()
    description_ru = models.TextField()
    description_en = models.TextField()

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    address_uz = models.CharField(max_length=255)
    address_ru = models.CharField(max_length=255)
    address_en = models.CharField(max_length=255)

    instagram = models.CharField(max_length=255, null=True, blank=True)
    facebook = models.CharField(max_length=255, null=True, blank=True)
    telegram = models.CharField(max_length=255, null=True, blank=True)
    whatsapp = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.title_uz
    
    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'


class CompanyAddress(Main):
    address_uz = models.CharField(max_length=255)
    address_ru = models.CharField(max_length=255)
    address_en = models.CharField(max_length=255)

    def __str__(self):
        return self.address_uz

    class Meta:
        verbose_name = 'Company Address'
        verbose_name_plural = 'Company Addresses'


class CompanyImage(Main):
    image = models.ImageField(upload_to='company_images/')

    def __str__(self):
        return self.image.name

    class Meta:
        verbose_name = 'Company Image'
        verbose_name_plural = 'Company Images'


class CompanyPhone(Main):
    phone = models.CharField(max_length=255)

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = 'Company Phone'
        verbose_name_plural = 'Company Phones'


class CompanyEmail(Main):
    email = models.EmailField()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Company Email'
        verbose_name_plural = 'Company Emails'


class Contact(Main):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'







