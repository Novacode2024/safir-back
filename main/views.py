from django.shortcuts import render
from . import  models
from . import serializers as ser
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404

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
@permission_classes([IsAuthenticated])
def viewCategory(request):
    data = models.Category.objects.all()
    serialized_data = ser.CategorySerializer(data, many=True)
    return Response(serialized_data.data, status=status.HTTP_200_OK)

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
    tags=["Category"] # ADD TAGS HERE
)
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def createCategory(request):
    serializer = ser.CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    category = get_object_or_404(models.Category, uuid=uuid)
    category.delete()
    return Response({"message": "Category deleted"},status=status.HTTP_200_OK)


#########################
# Product
#########################


@swagger_auto_schema(
    method='GET',
    operation_description="View all products.",
    responses={
        status.HTTP_200_OK: ser.ProductSerializer(many=True),
    },
    tags=["Product"]
)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def viewProduct(request):
    data = models.Product.objects.all()
    serialized_data = ser.ProductSerializer(data, many=True)
    return Response(serialized_data.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='POST',
    operation_description="Create a new product.",
    request_body=ser.ProductSerializer,
    responses={
        status.HTTP_200_OK: ser.ProductSerializer,
        status.HTTP_400_BAD_REQUEST: "Bad Request",
    },
    tags=["Product"]
)
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def createProduct(request):
    serializer = ser.ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    serializer = ser.ProductSerializer(product, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    product.delete()
    return Response({"message": "Product deleted"},status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='GET',
    operation_description="View all product images.",
    responses={
        status.HTTP_200_OK: ser.ProductImageSerializer(many=True),
    },
    tags=["ProductImage"]
)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def viewProductImage(request):
    data = models.ProductImage.objects.all()
    serialized_data = ser.ProductImageSerializer(data, many=True)
    return Response(serialized_data.data)

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
@permission_classes([IsAuthenticated])
def createProductImage(request):
    serializer = ser.ProductImageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    product.delete()
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
@permission_classes([IsAuthenticated])
def viewSlider(request):
    data = models.Slider.objects.all()
    serialized_data = ser.SliderSerializer(data, many=True)
    return Response(serialized_data.data)


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
@permission_classes([IsAuthenticated])
def createSlider(request):
    serializer = ser.SliderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    slider = get_object_or_404(models.Slider, uuid=uuid)
    serializer = ser.SliderSerializer(slider, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    slider.delete()
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
@permission_classes([IsAuthenticated])
def viewBlog(request):
    data = models.Blog.objects.all()
    serialized_data = ser.BlogSerializer(data, many=True)
    return Response(serialized_data.data)


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
@permission_classes([IsAuthenticated])
def createBlog(request):
    serializer = ser.BlogSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    blog = get_object_or_404(models.Blog, uuid=uuid)
    serializer = ser.BlogSerializer(blog, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    blog.delete()
    return Response({"message": "Blog deleted"},status=status.HTTP_200_OK)



#########################
# Company
#########################

@swagger_auto_schema(
    method='GET',
    operation_description="View company details.",
    responses={
        status.HTTP_200_OK: ser.CompanySerializer(many=True),
    },
    tags=["Company"]
)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def viewCompany(request):
    data = models.Company.objects.all()
    serialized_data = ser.CompanySerializer(data, many=True)
    return Response(serialized_data.data)


@swagger_auto_schema(
    method='POST',
    operation_description="Create company details.",
    request_body=ser.CompanySerializer,
    responses={
        status.HTTP_200_OK: ser.CompanySerializer,
        status.HTTP_400_BAD_REQUEST: "Bad Request",
    },
    tags=["Company"]
)
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def createCompany(request):
    serializer = ser.CompanySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='PUT',
    operation_description="Update company details.",
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
def updateCompany(request, uuid):
    company = get_object_or_404(models.Company, uuid=uuid)
    serializer = ser.CompanySerializer(company, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='DELETE',
    operation_description="Delete company details.",
    responses={
        status.HTTP_200_OK: "Company deleted",
        status.HTTP_404_NOT_FOUND: "Company not found",
    },
    tags=["Company"]
)
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def deleteCompany(request, uuid):
    company = get_object_or_404(models.Company, uuid=uuid)
    company.delete()
    return Response({"message": "Company deleted"},status=status.HTTP_200_OK)


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
@permission_classes([IsAuthenticated])
def viewCompanyAddress(request):
    data = models.CompanyAddress.objects.all()
    serialized_data = ser.CompanyAddressSerializer(data, many=True)
    return Response(serialized_data.data)


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
    companyaddress.delete()
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
@permission_classes([IsAuthenticated])
def viewCompanyImage(request):
    data = models.CompanyImage.objects.all()
    serialized_data = ser.CompanyImageSerializer(data, many=True)
    return Response(serialized_data.data)

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
    serializer = ser.CompanyImageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    companyimage.delete()
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
@permission_classes([IsAuthenticated])
def viewCompanyPhone(request):
    data = models.CompanyPhone.objects.all()
    serialized_data = ser.CompanyPhoneSerializer(data, many=True)
    return Response(serialized_data.data)


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
    companyphone.delete()
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
@permission_classes([IsAuthenticated])
def viewCompanyEmail(request):
    data = models.CompanyEmail.objects.all()
    serialized_data = ser.CompanyEmailSerializer(data, many=True)
    return Response(serialized_data.data)


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
    companyemail.delete()
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
@permission_classes([IsAuthenticated])
def viewContact(request):
    data = models.Contact.objects.all()
    serialized_data = ser.ContactSerializer(data, many=True)
    return Response(serialized_data.data)


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
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
def deleteContact(request, uuid):
    contact = get_object_or_404(models.Contact, uuid=uuid)
    contact.delete()
    return Response({"message": "Contact deleted"},status=status.HTTP_200_OK)