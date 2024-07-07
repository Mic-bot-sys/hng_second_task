from django.shortcuts import render
from rest_framework.decorators import api_view
from authapp.models import MainUser, Organisation, UserOrganisation
from authapp.serializers import OrganisationOutputSerializer, UserInputSerializer, UserLoginSerializer, UserOutputSerializer
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework import serializers
from django.db import transaction
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken

from django.conf import settings




# Create your views here.
@api_view(["POST"])
def register(request):
    try:        
        data = request.data
        serializer = UserInputSerializer(data=data)
        if not serializer.is_valid():
            return Response({'message': 'Registration unsuccessful', 'errors': "This is an Error" }, status=status.HTTP_400_BAD_REQUEST)
        username = data["email"].split("@")[0]
        password = make_password(data["password"])
        
        
        with transaction.atomic():            
            user = MainUser(
                username = username,
                firstName = data["firstName"],
                lastName = data["lastName"],
                email = data["email"],
                password = password,
                phone = data["phone"],
            )
            user.save()        
            
            organisation = Organisation(name = f"{user.firstName}'s Organisation", createdBy_id=user.id)
            organisation.save()
            
            user_organisation = UserOrganisation(
                    organisation_id = organisation.orgId,
                    user_id = user.id
                )                
            user_organisation.save()
            
        user_serializer = UserOutputSerializer(user)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        response = Response({'message': 'Registration successful', 'data': {'access_token': access_token, 'user':  user_serializer.data} }, status=status.HTTP_201_CREATED)
        
        return response
    
    except Exception as ex:
        return Response({'message': 'Registration unsuccessful', 'status': 'Bad Request', 'statusCode': 400}, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(["POST"])
def login(request):
    try:        
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if not serializer.is_valid():
            return Response({'message': 'Login unsuccessful', 'errors': "This is an Error" }, status=status.HTTP_400_BAD_REQUEST)
        username = data["email"].split("@")[0]
        password = data["password"]
        user = MainUser.objects.get(username=username)
        isCorrect = user.check_password(password)
        
        if isCorrect:
            user_serializer = UserOutputSerializer(user)
            request.user = user_serializer
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            response = Response({'message': 'Login successful', 'data': {'access_token': access_token, 'user':  user_serializer.data} }, status=status.HTTP_201_CREATED)
            response.set_cookie(
                    key='access_token',
                    value=access_token,
                    httponly=True,  # Makes the cookie accessible only via HTTP(S) and not JavaScript
                    secure=settings.DEBUG == False,  # Ensures the cookie is only sent over HTTPS if not in debug mode
                    samesite='Lax',  # Helps protect against CSRF
                    max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()  # Lifetime of the cookie
                )
            
            return response
    
    except Exception as ex:
        return Response({'message': 'Authentication failed', 'status': 'Bad Request', 'statusCode': 401}, status=status.HTTP_401_UNAUTHORIZED)
    

    
# Gets all your organisations the user belongs to or created. If a user is logged in properly, they can get all their organisations. They should not get another user’s organisation [PROTECTED].
@api_view(["GET"])
def organisations(request):
    try:
        organisations = Organisation.objects.filter(user_id=id)
        serializer = OrganisationOutputSerializer(organisations, many=True)
        return Response({'message': 'success', 'organisations':  serializer.data }, status=status.HTTP_201_CREATED)
    except Exception as ex:
        return Response({'message': 'error', 'status': 'Bad Request', 'statusCode': 400}, status=status.HTTP_400_BAD_REQUEST)



