from . import models
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'
        
                    
class ProductSerializer(serializers.ModelSerializer):
    total_images = serializers.SerializerMethodField()
    product_images = serializers.SerializerMethodField()
    category = CategorySerializer()
    def get_total_images(self, obj):
        return obj.total_images
    
    def get_product_images(self, obj):
        return ProductImageSerializer(obj.productimage_set.all(), many=True).data
    
    def get_category(self, obj):
        return CategorySerializer(obj.category).data

    class Meta:
        model = models.Product

        fields = '__all__'
        

                    
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImage
        fields = '__all__'
        
                        
class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Slider
        fields = '__all__'
        
                    
class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Blog
        fields = '__all__'
        
                    
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company
        fields = '__all__'
        
                    
class CompanyAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CompanyAddress
        fields = '__all__'
        
                        
class CompanyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CompanyImage
        fields = '__all__'
        
                        
class CompanyPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CompanyPhone
        fields = '__all__'
        
                        
class CompanyEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CompanyEmail
        fields = '__all__'
        
                        
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Contact
        fields = '__all__'
        
                    