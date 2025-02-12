from django.shortcuts import render
from . import  models
from . import serializers as ser
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes, parser_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from . import funcs

# --- Add import for drf_yasg decorators ---
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# --- End add import for drf_yasg decorators ---


#########################
# Category
#########################

@swagger_auto_schema(
    method='GET',
    operation_description="View all categories.",
    responses={
        status.HTTP_200_OK: ser.CategorySerializer(many=True),
    },
    tags=["Category"]
)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def viewCategory(request):
    data = models.Category.objects.filter(is_active=True)
    serialized_data = ser.CategorySerializer(data, many=True)
    return Response({"categories": serialized_data.data}, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='PUT',
    operation_description="Update a specific category.",
    request_body=ser.CategorySerializer,
    responses={
        status.HTTP_200_OK: ser.CategorySerializer,
        status.HTTP_400_BAD_REQUEST: "Bad Request",
        status.HTTP_404_NOT_FOUND: "Category not found",
    },
    tags=["Category"]
)
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def updateCategory(request, uuid):
    category = get_object_or_404(models.Category, uuid=uuid)
    serializer = ser.CategorySerializer(category, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='POST',
    operation_description="Create a new category.",
    request_body=ser.CategorySerializer,
    responses={
        status.HTTP_200_OK: ser.CategorySerializer,
        status.HTTP_400_BAD_REQUEST: "Bad Request",
    },
    tags=["Category"]
)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def createCategory(request):
    category = models.Category.objects.create(
        title_uz = request.data['title_uz'],
        image = request.FILES.get('image'),
        description_uz =  request.data.get('description_uz'),
        priority = request.data['priority'],
    )
    serializer = ser.CategorySerializer(category)
    return Response(serializer.data, status=status.HTTP_200_OK)




@swagger_auto_schema(
    method='DELETE',
    operation_description="Delete a specific category.",
    responses={
        status.HTTP_200_OK: "Category deleted",
        status.HTTP_404_NOT_FOUND: "Category not found",
    },
    tags=["Category"]
)
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def deleteCategory(request, uuid):
    print("asdasda s-=-=-=-=-=-=-=-=")
    category = models.Category.objects.get(uuid=uuid)
    print("-=-=--=-=-=-=-=-=-=-=-")
    category.is_active = False  
    category.save()
    return Response({"message": "Category deleted"},status=status.HTTP_200_OK)


#########################
# Product
#########################

@swagger_auto_schema(
    method='get',
    operation_description="View active products. Initially returns 12 products, and more can be loaded incrementally (0-12, 12-24, 24-36, etc.).",
    manual_parameters=[
        openapi.Parameter('category', openapi.IN_QUERY, description="Filter products by category UUID", type=openapi.TYPE_STRING),
        openapi.Parameter('limit', openapi.IN_QUERY, description="Number of products to fetch (increases by 12 each time)", type=openapi.TYPE_INTEGER, default=12),
    ],
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Successful response with product data",
            schema=openapi.Schema(type=openapi.TYPE_OBJECT,properties={
                    "products": openapi.Schema(type=openapi.TYPE_ARRAY,items=openapi.Schema(type=openapi.TYPE_OBJECT)),
                    "next_limit": openapi.Schema(type=openapi.TYPE_INTEGER,description="Next limit for fetching more products"),
                    "has_more": openapi.Schema(type=openapi.TYPE_BOOLEAN,description="Indicates if more products are available")
                },
            ),
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Response(description="Bad Request"),
    },
    tags=["Product"]
)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def viewProduct(request):
    products = models.Product.objects.filter(is_active=True)
    category = request.GET.get('category')


    if category:
        category_instance = get_object_or_404(models.Category, uuid=category)
        products = products.filter(category=category_instance)

    try:
        limit = int(request.GET.get('limit', 12)) 
    except ValueError:
        limit = 12

    total_products = products.count()
    product_list = products[:limit] 

    serialized_data = ser.ProductSerializer(product_list, many=True)

    return Response({
        "products": serialized_data.data,
        "next_limit": limit + 12 if limit + 12 <= total_products else total_products, 
        "has_more": limit < total_products
    }, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='GET',
    operation_description="View a specific product.",
    responses={
        status.HTTP_200_OK: ser.ProductSerializer,
    },
    tags=["Product"]
)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def viewProductDetail(request, uuid):
    product = get_object_or_404(models.Product, uuid=uuid)
    serialized_data = ser.ProductSerializer(product)
    return Response({"productDetail": serialized_data.data}, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='POST',
    operation_description="Create a new product.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['category', 'title_uz', 'price', 'image', 'priority'],
        properties={'category': openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Category UUID"
            ),
            'title_uz': openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Product title in Uzbek"
            ),
            'price': openapi.Schema(
                type=openapi.TYPE_NUMBER,
                description="Product price"
            ),
            'image': openapi.Schema(
                type=openapi.TYPE_STRING,
                format="binary",
                description="Product image"
            ),
            'description_uz': openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Product description in Uzbek",
                nullable=True
            ),
            'priority': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description="Product priority"
            ),
        },
    ),
    responses={
        status.HTTP_200_OK: ser.ProductSerializer(),
        status.HTTP_400_BAD_REQUEST: "Bad Request",
    },
    tags=["Product"]
)
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def createProduct(request):
    try: 
        category = get_object_or_404(models.Category, uuid=request.data['category'])
        product = models.Product.objects.create(
            title_uz = request.data['title_uz'],
            price = request.data['price'] if request.data['price'] else 0, 
            image_min = request.FILES.get('image'),
            image_max = request.FILES.get('image'),
            category = category,
            description_uz =  request.data.get('description_uz'),
            priority = request.data['priority'],
        )
        serializer = ser.ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='PUT',
    operation_description="Update a specific product.",
    request_body=ser.ProductSerializer,
    responses={
        status.HTTP_200_OK: ser.ProductSerializer,
        status.HTTP_400_BAD_REQUEST: "Bad Request",
        status.HTTP_404_NOT_FOUND: "Product not found",
    },
    tags=["Product"]
)
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def updateProduct(request, uuid):
    product = get_object_or_404(models.Product, uuid=uuid)
    category = request.data.get('category')
    try:
        try:
            if bool(category):
                category = get_object_or_404(models.Category, uuid=category)
                product.category = category
        except:
            pass
        product.title_uz = request.data['title_uz']
        product.title_en = request.data['title_en']
        product.title_ru = request.data['title_ru']
        product.price = request.data['price'] if request.data['price'] else 0
        product.image_min = request.FILES.get('image')
        product.image_max = request.FILES.get('image')
        product.description_uz = request.data['description_uz']
        product.description_en = request.data['description_en']
        product.description_ru = request.data['description_ru']
        product.priority = request.data['priority']
        product.save()
        serializer = ser.ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message": str(e)},status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='DELETE',
    operation_description="Delete a specific product.",
    responses={
        status.HTTP_200_OK: "Product deleted",
        status.HTTP_404_NOT_FOUND: "Product not found",
    },
    tags=["Product"]
)
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def deleteProduct(request, uuid):
    product = get_object_or_404(models.Product, uuid=uuid)
    product.is_active = False
    product.save()
    return Response({"message": "Product deleted"},status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='GET',
    operation_description="View all product images. Optionally filter by product.",
    manual_parameters=[openapi.Parameter('product', openapi.IN_QUERY, description="Filter product images by product", type=openapi.TYPE_STRING)],
    responses={
        status.HTTP_200_OK: ser.ProductImageSerializer(many=True),
    },

    tags=["ProductImage"]
)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def viewProductImage(request):
    product_images = models.ProductImage.objects.filter(is_active=True)
    product = request.GET.get('product')
    if product:
        product_images = product_images.filter(product=product)

    serialized_data = ser.ProductImageSerializer(product_images, many=True)
    return Response({"productImages": serialized_data.data}, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='POST',
    operation_description="Create a new product image.",
    request_body=ser.ProductImageSerializer,
    responses={
        status.HTTP_200_OK: ser.ProductImageSerializer,
        status.HTTP_400_BAD_REQUEST: "Bad Request",
    },
    tags=["ProductImage"]
)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@parser_classes([MultiPartParser, FormParser])
def createProductImage(request):
    try:
        product = request.data.get('product')
        if not product:
            return Response({"message": "Product UUID is required"}, status=status.HTTP_400_BAD_REQUEST)

        product_instance = get_object_or_404(models.Product, uuid=product)

        images = request.FILES.getlist('image')

        if not images:
            return Response({"message": "No images provided"}, status=status.HTTP_400_BAD_REQUEST)

        for image in images:
            models.ProductImage.objects.create(product=product_instance, image_min=image, image_max=image)


        serializer = ser.ProductImageSerializer(models.ProductImage.objects.filter(product=product_instance), many=True)
        return Response({"productImages": serializer.data}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='PUT',
    operation_description="Update a specific product image.",
    request_body=ser.ProductImageSerializer,
    responses={
        status.HTTP_200_OK: ser.ProductImageSerializer,
        status.HTTP_400_BAD_REQUEST: "Bad Request",
        status.HTTP_404_NOT_FOUND: "Product Image not found",
    },
    tags=["ProductImage"]
)
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def updateProductImage(request, uuid):
    product = get_object_or_404(models.ProductImage, uuid=uuid)
    serializer = ser.ProductImageSerializer(product, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='DELETE',
    operation_description="Delete a specific product image.",
    responses={
        status.HTTP_200_OK: "Product Image deleted",
        status.HTTP_404_NOT_FOUND: "Product Image not found",
    },
    tags=["ProductImage"]
)
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def deleteProductImage(request, uuid):
    product = get_object_or_404(models.ProductImage, uuid=uuid)
    product.is_active = False
    product.save()
    return Response({"message": "Product Image deleted"},status=status.HTTP_200_OK)



#########################
# Slider
#########################


@swagger_auto_schema(
    method='GET',
    operation_description="View all sliders.",
    responses={
        status.HTTP_200_OK: ser.SliderSerializer(many=True),
    },
    tags=["Slider"]
)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def viewSlider(request):
    data = models.Slider.objects.filter(is_active=True)
    serialized_data = ser.SliderSerializer(data, many=True)
    return Response({"sliders": serialized_data.data}, status=status.HTTP_200_OK)



@swagger_auto_schema(
    method='POST',
    operation_description="Create a new slider.",
    request_body=ser.SliderSerializer,
    responses={
        status.HTTP_200_OK: ser.SliderSerializer,
        status.HTTP_400_BAD_REQUEST: "Bad Request",
    },
    tags=["Slider"]
)
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@parser_classes([MultiPartParser, FormParser])
def createSlider(request):
    slider = models.Slider.objects.create(
        title_uz = request.data['title_uz'],
        image_min = request.FILES.get('image'),
        image_max = request.FILES.get('image'),
        description_uz =  request.data['description_uz'],
        priority = request.data['priority'],
    )
    serializer = ser.SliderSerializer(slider)
    return Response(serializer.data, status=status.HTTP_200_OK)




@swagger_auto_schema(
    method='PUT',
    operation_description="Update a specific slider.",
    request_body=ser.SliderSerializer,
    responses={
        status.HTTP_200_OK: ser.SliderSerializer,
        status.HTTP_400_BAD_REQUEST: "Bad Request",
        status.HTTP_404_NOT_FOUND: "Slider not found",
    },
    tags=["Slider"]
)
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def updateSlider(request, uuid):
    try:
        slider = get_object_or_404(models.Slider, uuid=uuid)
        slider.title_uz = request.data['title_uz']
        slider.title_en = request.data['title_en']
        slider.title_ru = request.data['title_ru']
        slider.image_min = request.FILES.get('image')
        slider.image_max = request.FILES.get('image')
        slider.description_uz = request.data['description_uz']
        slider.description_en = request.data['description_en']
        slider.description_ru = request.data['description_ru']
        slider.priority = request.data['priority']
        slider.save()
        serializer = ser.SliderSerializer(slider)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message": str(e)},status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='DELETE',
    operation_description="Delete a specific slider.",
    responses={
        status.HTTP_200_OK: "Slider deleted",
        status.HTTP_404_NOT_FOUND: "Slider not found",
    },
    tags=["Slider"]
)
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def deleteSlider(request, uuid):
    slider = get_object_or_404(models.Slider, uuid=uuid)
    slider.is_active = False
    slider.save()
    return Response({"message": "Slider deleted"},status=status.HTTP_200_OK)




#########################
# Blog
#########################

@swagger_auto_schema(
    method='GET',
    operation_description="View all blogs.",
    responses={
        status.HTTP_200_OK: ser.BlogSerializer(many=True),
    },
    tags=["Blog"]
)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def viewBlog(request):
    data = models.Blog.objects.filter(is_active=True)
    serialized_data = ser.BlogSerializer(data, many=True)
    return Response({"blogs": serialized_data.data}, status=status.HTTP_200_OK)



@swagger_auto_schema(
    method='POST',
    operation_description="Create a new blog post.",
    request_body=ser.BlogSerializer,
    responses={
        status.HTTP_200_OK: ser.BlogSerializer,
        status.HTTP_400_BAD_REQUEST: "Bad Request",
    },
    tags=["Blog"]
)
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@parser_classes([MultiPartParser, FormParser])
@permission_classes([IsAuthenticated])
def createBlog(request):
    try:
        blog = models.Blog.objects.create(
            title_uz = request.data['title_uz'],
            image_min = request.FILES.get('image'),
            image_max = request.FILES.get('image'),
            description_uz =  request.data['description_uz'],
            priority = request.data['priority'],
        )
        serializer = ser.BlogSerializer(blog)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message": str(e)},status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='PUT',
    operation_description="Update a specific blog post.",
    request_body=ser.BlogSerializer,
    responses={
        status.HTTP_200_OK: ser.BlogSerializer,
        status.HTTP_400_BAD_REQUEST: "Bad Request",
        status.HTTP_404_NOT_FOUND: "Blog not found",
    },
    tags=["Blog"]
)
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def updateBlog(request, uuid):
    try:
        blog = get_object_or_404(models.Blog, uuid=uuid)
        blog.title_uz = request.data['title_uz']
        blog.title_en = request.data['title_en']
        blog.title_ru = request.data['title_ru']
        blog.image_min = request.FILES.get('image')
        blog.image_max = request.FILES.get('image')
        blog.description_uz = request.data['description_uz']
        blog.description_en = request.data['description_en']
        blog.description_ru = request.data['description_ru']
        blog.priority = request.data['priority']
        blog.save()
        serializer = ser.BlogSerializer(blog)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message": str(e)},status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='GET',
    operation_description="View a specific blog post.",
    responses={
        status.HTTP_200_OK: ser.BlogSerializer,
    },
    tags=["Blog"]
)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def viewBlogDetail(request, uuid):
    try:
        blog = get_object_or_404(models.Blog, uuid=uuid)
        serialized_data = ser.BlogSerializer(blog)
        return Response({"blogDetail": serialized_data.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message": str(e)},status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='DELETE',
    operation_description="Delete a specific blog post.",
    responses={
        status.HTTP_200_OK: "Blog deleted",
        status.HTTP_404_NOT_FOUND: "Blog not found",
    },
    tags=["Blog"]
)
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def deleteBlog(request, uuid):
    blog = get_object_or_404(models.Blog, uuid=uuid)
    blog.is_active = False
    blog.save()
    return Response({"message": "Blog deleted"},status=status.HTTP_200_OK)




#########################
# Company
#########################

@swagger_auto_schema(
    method='GET',
    operation_description="View company details. If multiple companies are found, the last one will be returned.",
    responses={
        status.HTTP_200_OK: ser.CompanySerializer(many=True),
    },
    tags=["Company"]
)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def viewCompany(request):
    try:
        data = models.Company.objects.filter(is_active=True)
        if data.count() >= 1:
            data = data.last()
            serialized_data = ser.CompanySerializer(data)
            return Response({"company": serialized_data.data}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Multiple companies found"},status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"message": str(e)},status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='PUT',
    operation_description="Update company details. Agar uuid berilmasa va kompanya yoq bolsa yangi company yaratadi agar bolsa 400 qaytaradi.",
    request_body=ser.CompanySerializer,
    responses={
        status.HTTP_200_OK: ser.CompanySerializer,
        status.HTTP_400_BAD_REQUEST: "Bad Request",
        status.HTTP_404_NOT_FOUND: "Company not found",
    },
    tags=["Company"]
)


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def updateCompany(request):
    if request.data.get('uuid'):
        company = get_object_or_404(models.Company, uuid=request.data.get('uuid'))
        serializer = ser.CompanySerializer(company, data=request.data, partial=True)
        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        if models.Company.objects.filter(is_active=True).count() >= 1:
            return Response({"message": "Company already exists"},status=status.HTTP_400_BAD_REQUEST)
        else:
            company = models.Company.objects.create(
                title_uz = request.data['title_uz'],
                description_uz = request.data['description_uz'],

            address_uz = request.data['address_uz'],
            latitude = request.data['latitude'],
            longitude = request.data['longitude'],

            video = request.data['video'],
            instagram = request.data['instagram'],
            facebook = request.data['facebook'],
            youtube = request.data['youtube'],
            telegram = request.data['telegram'],
            whatsapp = request.data['whatsapp'],
        )
        serializer = ser.CompanySerializer(company)
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#########################
# CompanyAddress
#########################

@swagger_auto_schema(
    method='GET',
    operation_description="View company addresses.",
    responses={
        status.HTTP_200_OK: ser.CompanyAddressSerializer(many=True),
    },
    tags=["CompanyAddress"]
)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def viewCompanyAddress(request):
    data = models.CompanyAddress.objects.filter(is_active=True)
    serialized_data = ser.CompanyAddressSerializer(data, many=True)
    return Response({"companyAddresses": serialized_data.data}, status=status.HTTP_200_OK)



@swagger_auto_schema(
    method='POST',
    operation_description="Create company address.",
    request_body=ser.CompanyAddressSerializer,
    responses={
        status.HTTP_200_OK: ser.CompanyAddressSerializer,
        status.HTTP_400_BAD_REQUEST: "Bad Request",
    },
    tags=["CompanyAddress"]
)
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def createCompanyAddress(request):
    serializer = ser.CompanyAddressSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='PUT',
    operation_description="Update company address.",
    request_body=ser.CompanyAddressSerializer,
    responses={
        status.HTTP_200_OK: ser.CompanyAddressSerializer,
        status.HTTP_400_BAD_REQUEST: "Bad Request",
        status.HTTP_404_NOT_FOUND: "Company Address not found",
    },
    tags=["CompanyAddress"]
)
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def updateCompanyAddress(request, uuid):
    companyaddress = get_object_or_404(models.CompanyAddress, uuid=uuid)
    serializer = ser.CompanyAddressSerializer(companyaddress, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='DELETE',
    operation_description="Delete company address.",
    responses={
        status.HTTP_200_OK: "Company Address deleted",
        status.HTTP_404_NOT_FOUND: "Company Address not found",
    },
    tags=["CompanyAddress"]
)
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def deleteCompanyAddress(request, uuid):
    companyaddress = get_object_or_404(models.CompanyAddress, uuid=uuid)
    companyaddress.is_active = False
    companyaddress.save()
    return Response({"message": "Company Address deleted"},status=status.HTTP_200_OK)




#########################
# CompanyImage
#########################
@swagger_auto_schema(
    method='GET',
    operation_description="View company images.",
    responses={
        status.HTTP_200_OK: ser.CompanyImageSerializer(many=True),
    },
    tags=["CompanyImage"]
) 
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def viewCompanyImage(request):
    data = models.CompanyImage.objects.filter(is_active=True)
    serialized_data = ser.CompanyImageSerializer(data, many=True)
    
    return Response({"companyImages": serialized_data.data}) 

@swagger_auto_schema(
    method='POST',
    operation_description="Create company image.",
    request_body=ser.CompanyImageSerializer,
    responses={
        status.HTTP_200_OK: ser.CompanyImageSerializer,
        status.HTTP_400_BAD_REQUEST: "Bad Request",
    },
    tags=["CompanyImage"]
)
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def createCompanyImage(request):
    try: 
        images = request.FILES.getlist('images')
        for image in images:
            models.CompanyImage.objects.create(
                image = image
            )
        return Response({"message": "Company images created"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='PUT',
    operation_description="Update company image.",
    request_body=ser.CompanyImageSerializer,
    responses={
        status.HTTP_200_OK: ser.CompanyImageSerializer,
        status.HTTP_400_BAD_REQUEST: "Bad Request",
        status.HTTP_404_NOT_FOUND: "Company Image not found",
    },
    tags=["CompanyImage"]
)
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def updateCompanyImage(request, uuid):
    companyimage = get_object_or_404(models.CompanyImage, uuid=uuid)
    serializer = ser.CompanyImageSerializer(companyimage, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='DELETE',
    operation_description="Delete company image.",
    responses={
        status.HTTP_200_OK: "Company Image deleted",
        status.HTTP_404_NOT_FOUND: "Company Image not found",
    },
    tags=["CompanyImage"]
)
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def deleteCompanyImage(request, uuid):
    companyimage = get_object_or_404(models.CompanyImage, uuid=uuid)
    companyimage.is_active = False
    companyimage.save()
    return Response({"message": "Company Image deleted"},status=status.HTTP_200_OK)



#########################
# CompanyPhone
#########################

@swagger_auto_schema(
    method='GET',
    operation_description="View company phone numbers.",
    responses={
        status.HTTP_200_OK: ser.CompanyPhoneSerializer(many=True),
    },
    tags=["CompanyPhone"]
)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def viewCompanyPhone(request):
    data = models.CompanyPhone.objects.filter(is_active=True)
    serialized_data = ser.CompanyPhoneSerializer(data, many=True)
    return Response({"companyPhones": serialized_data.data}, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='POST',
    operation_description="Create company phone number.",
    request_body=ser.CompanyPhoneSerializer,
    responses={
        status.HTTP_200_OK: ser.CompanyPhoneSerializer,
        status.HTTP_400_BAD_REQUEST: "Bad Request",
    },
    tags=["CompanyPhone"]
)
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def createCompanyPhone(request):
    serializer = ser.CompanyPhoneSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='PUT',
    operation_description="Update company phone number.",
    request_body=ser.CompanyPhoneSerializer,
    responses={
        status.HTTP_200_OK: ser.CompanyPhoneSerializer,
        status.HTTP_400_BAD_REQUEST: "Bad Request",
        status.HTTP_404_NOT_FOUND: "Company Phone not found",
    },
    tags=["CompanyPhone"]
)
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def updateCompanyPhone(request, uuid):
    companyphone = get_object_or_404(models.CompanyPhone, uuid=uuid)
    serializer = ser.CompanyPhoneSerializer(companyphone, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='DELETE',
    operation_description="Delete company phone number.",
    responses={
        status.HTTP_200_OK: "Company Phone deleted",
        status.HTTP_404_NOT_FOUND: "Company Phone not found",
    },
    tags=["CompanyPhone"]
)
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def deleteCompanyPhone(request, uuid):
    companyphone = get_object_or_404(models.CompanyPhone, uuid=uuid)
    companyphone.is_active = False
    companyphone.save()
    return Response({"message": "Company Phone deleted"},status=status.HTTP_200_OK)



#########################
# CompanyEmail
#########################

@swagger_auto_schema(
    method='GET',
    operation_description="View company emails.",
    responses={
        status.HTTP_200_OK: ser.CompanyEmailSerializer(many=True),
    },
    tags=["CompanyEmail"]
)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def viewCompanyEmail(request):
    data = models.CompanyEmail.objects.filter(is_active=True)
    serialized_data = ser.CompanyEmailSerializer(data, many=True)
    return Response({"companyEmails": serialized_data.data}, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='POST',
    operation_description="Create company email.",
    request_body=ser.CompanyEmailSerializer,
    responses={
        status.HTTP_200_OK: ser.CompanyEmailSerializer,
        status.HTTP_400_BAD_REQUEST: "Bad Request",
    },
    tags=["CompanyEmail"]
)
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def createCompanyEmail(request):
    serializer = ser.CompanyEmailSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='PUT',
    operation_description="Update company email.",
    request_body=ser.CompanyEmailSerializer,
    responses={
        status.HTTP_200_OK: ser.CompanyEmailSerializer,
        status.HTTP_400_BAD_REQUEST: "Bad Request",
        status.HTTP_404_NOT_FOUND: "Company Email not found",
    },
    tags=["CompanyEmail"]
)
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def updateCompanyEmail(request, uuid):
    companyemail = get_object_or_404(models.CompanyEmail, uuid=uuid)
    serializer = ser.CompanyEmailSerializer(companyemail, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='DELETE',
    operation_description="Delete company email.",
    responses={
        status.HTTP_200_OK: "Company Email deleted",
        status.HTTP_404_NOT_FOUND: "Company Email not found",
    },
    tags=["CompanyEmail"]
)
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def deleteCompanyEmail(request, uuid):
    companyemail = get_object_or_404(models.CompanyEmail, uuid=uuid)
    companyemail.is_active = False
    companyemail.save()
    return Response({"message": "Company Email deleted"},status=status.HTTP_200_OK)




#########################
# Contact
#########################

@swagger_auto_schema(
    method='GET',
    operation_description="View all contacts.",
    responses={
        status.HTTP_200_OK: ser.ContactSerializer(many=True),
    },
    tags=["Contact"]
) 
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def viewContact(request):
    data = models.Contact.objects.filter(is_active=True)
    serialized_data = ser.ContactSerializer(data, many=True)
    return Response({"contacts": serialized_data.data}, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='POST',
    operation_description="Create a new contact message.",
    request_body=ser.ContactSerializer,
    responses={
        status.HTTP_200_OK: ser.ContactSerializer,
        status.HTTP_400_BAD_REQUEST: "Bad Request",
    },
    tags=["Contact"]
)
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def createContact(request):
    serializer = ser.ContactSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='PUT',
    operation_description="Update a specific contact.",
    request_body=ser.ContactSerializer,
    responses={
        status.HTTP_200_OK: ser.ContactSerializer,
        status.HTTP_400_BAD_REQUEST: "Bad Request",
        status.HTTP_404_NOT_FOUND: "Contact not found",
    },
    tags=["Contact"]
)
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
def updateContact(request, uuid):
    contact = get_object_or_404(models.Contact, uuid=uuid)
    serializer = ser.ContactSerializer(contact, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='DELETE',
    operation_description="Delete a specific contact.",
    responses={
        status.HTTP_200_OK: "Contact deleted",
        status.HTTP_404_NOT_FOUND: "Contact not found",
    },
    tags=["Contact"]
)
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
def deleteContact(request, uuid):
    contact = get_object_or_404(models.Contact, uuid=uuid)
    contact.is_active = False
    contact.save()
    return Response({"message": "Contact deleted"},status=status.HTTP_200_OK)