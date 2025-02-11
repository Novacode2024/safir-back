from django.urls import path, re_path 
from . import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
      title="API Documentation",
      default_version='v1',
      description="API documentation for your project",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,), 
)


urlpatterns_views = [

    
    path('category/', views.viewCategory, name='view_category'),
    path('category/create/', views.createCategory, name='create_category'),
    path('category/update/<str:uuid>/', views.updateCategory, name='update_category'),
    path('category/delete/<str:uuid>/', views.deleteCategory, name='delete_category'),

    # Product
    path('product/', views.viewProduct, name='view_product'),
    path('product/detail/<str:uuid>/', views.viewProductDetail, name='view_product_detail'),
    path('product/create/', views.createProduct, name='create_product'),
    path('product/update/<str:uuid>/', views.updateProduct, name='update_product'),
    path('product/delete/<str:uuid>/', views.deleteProduct, name='delete_product'),


    # ProductImage
    path('productimage/', views.viewProductImage, name='view_product_image'),
    path('productimage/create/', views.createProductImage, name='create_product_image'),
    path('productimage/update/<str:uuid>/', views.updateProductImage, name='update_product_image'),
    path('productimage/delete/<str:uuid>/', views.deleteProductImage, name='delete_product_image'),

    # Slider
    path('slider/', views.viewSlider, name='view_slider'),
    path('slider/create/', views.createSlider, name='create_slider'),
    path('slider/update/<str:uuid>/', views.updateSlider, name='update_slider'),
    path('slider/delete/<str:uuid>/', views.deleteSlider, name='delete_slider'),

    # Blog
    path('blog/', views.viewBlog, name='view_blog'),
    path('blog/create/', views.createBlog, name='create_blog'),
    path('blog/update/<str:uuid>/', views.updateBlog, name='update_blog'),
    path('blog/detail/<str:uuid>/', views.viewBlogDetail, name='view_blog_detail'),
    path('blog/delete/<str:uuid>/', views.deleteBlog, name='delete_blog'),

    # Company
    path('company/', views.viewCompany, name='view_company'),
    path('company/update/', views.updateCompany, name='update_company'),

    # CompanyAddress
    path('companyaddress/', views.viewCompanyAddress, name='view_company_address'),
    path('companyaddress/create/', views.createCompanyAddress, name='create_company_address'),
    path('companyaddress/update/<str:uuid>/', views.updateCompanyAddress, name='update_company_address'),
    path('companyaddress/delete/<str:uuid>/', views.deleteCompanyAddress, name='delete_company_address'),

    # CompanyImage
    path('companyimage/', views.viewCompanyImage, name='view_company_image'),
    path('companyimage/create/', views.createCompanyImage, name='create_company_image'),
    path('companyimage/update/<str:uuid>/', views.updateCompanyImage, name='update_company_image'),
    path('companyimage/delete/<str:uuid>/', views.deleteCompanyImage, name='delete_company_image'),

    # CompanyPhone
    path('companyphone/', views.viewCompanyPhone, name='view_company_phone'),
    path('companyphone/create/', views.createCompanyPhone, name='create_company_phone'),
    path('companyphone/update/<str:uuid>/', views.updateCompanyPhone, name='update_company_phone'),
    path('companyphone/delete/<str:uuid>/', views.deleteCompanyPhone, name='delete_company_phone'),

    # CompanyEmail
    path('companyemail/', views.viewCompanyEmail, name='view_company_email'),
    path('companyemail/create/', views.createCompanyEmail, name='create_company_email'),
    path('companyemail/update/<str:uuid>/', views.updateCompanyEmail, name='update_company_email'),
    path('companyemail/delete/<str:uuid>/', views.deleteCompanyEmail, name='delete_company_email'),

    # Contact
    path('contact/', views.viewContact, name='view_contact'),
    path('contact/create/', views.createContact, name='create_contact'),
    path('contact/update/<str:uuid>/', views.updateContact, name='update_contact'),
    path('contact/delete/<str:uuid>/', views.deleteContact, name='delete_contact'),
]

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + urlpatterns_views 


