from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from main import models

@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['username', 'password'],
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING),
        'password': openapi.Schema(type=openapi.TYPE_STRING),
    },
))
@api_view(['POST'])
def logIn(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({
            'detail': 'Not Found'
        }, status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user = user)


    context = {
            "user":{
                "token":token.key,
                "username":user.username,
                "first_name":user.first_name,
                "last_name":user.last_name,
            }
        }

    try:
        client = models.ClientStaff.objects.get(profile=user)
        if client:
            context['client_uuid'] = str(client.client.uuid)
            context['client_staff_uuid'] = str(client.uuid)
    except Exception as e:
        print(e)
        pass

    return  Response(context)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def logOut(request):
    print(request.user)
    token = Token.objects.filter(user=request.user)
    print(token)
    if token:
        token.delete()
    return Response({'success':True})