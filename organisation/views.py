from django.conf import settings
from django.shortcuts import render
import jwt
from rest_framework.decorators import api_view, permission_classes
from authapp.models import MainUser, Organisation, UserOrganisation
from authapp.permissions import AuthorizationPermission
from authapp.serializers import OrganisationOutputSerializer, OrganisationPostOutputSerializer, UserInputSerializer, UserLoginSerializer, UserOrganisationSerializer, UserOutputSerializer
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework import serializers
from django.db import transaction
from django.contrib.auth.hashers import make_password


# Create your views here.
@api_view(["GET"])
def get_user_record(request, userId):
    try:
        user = MainUser.objects.get(id=userId)
        serializer = UserOutputSerializer(user, many=False)
        return Response({'status': 'success', 'message': 'Obtained record successfully', 'data':  serializer.data }, status=status.HTTP_201_CREATED)
    except Exception as ex:
        return Response({'message': 'error', 'status': 'Bad Request', 'statusCode': 400}, status=status.HTTP_400_BAD_REQUEST)

    
@api_view(["GET"])
@permission_classes([AuthorizationPermission])
def get_organisations_by_userId(request):
    try:
        token = request.headers.get('Authorization')        
        token = token.split(' ')[1]
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_token.get('user_id')
        
        user_organisations = UserOrganisation.objects.filter(user_id=user_id)
        serializer = UserOrganisationSerializer(user_organisations, many=True)
        return Response({'message': 'success', 'data':  {'organisations': serializer.data} }, status=status.HTTP_201_CREATED)
    except Exception as ex:
        return Response({'message': 'error', 'status': 'Bad Request', 'statusCode': 400}, status=status.HTTP_400_BAD_REQUEST)



@api_view(["GET"])
def get_an_organisation_by_id(request, orgId):
    try:
        organisations = Organisation.objects.get(orgId=orgId)
        serializer = OrganisationOutputSerializer(organisations, many=False)
        return Response({'message': 'success', 'data':  serializer.data }, status=status.HTTP_201_CREATED)
    except Exception as ex:
        return Response({'message': 'error', 'status': 'Bad Request', 'statusCode': 400}, status=status.HTTP_400_BAD_REQUEST)



@api_view(["POST"])
def create_new_organisation(request):
    try:
        name = ""
        description = ""
        userId = request.user.id
        organisation = Organisation(
            name = name,
            description = description,
            createdBy_id = userId
        )
        organisation.save()
        serializer = OrganisationPostOutputSerializer(organisation, many=False)
        return Response({'status': 'success', 'message': 'Organisation created successfully', 'data':  serializer.data }, status=status.HTTP_201_CREATED)
    except Exception as ex:
        return Response({'message': 'Client error', 'status': 'Bad Request', 'statusCode': 400}, status=status.HTTP_400_BAD_REQUEST)



@api_view(["POST"])
def add_user_to_an_organisation(request, orgId):
    try:
        data = request.data
        userId = data["userId"]
        organisation = Organisation.objects.get(orgId=orgId)
        
        user_organisation = UserOrganisation(
            user_id = userId,
            organisation_id = organisation.orgId
        )
        user_organisation.save()
        serializer = UserOrganisationSerializer(user_organisation, many=False)
        return Response({'status': 'success', 'message': 'User added to organisation successfully', 'data':  serializer.data }, status=status.HTTP_201_CREATED)
    except Exception as ex:
        return Response({'message': 'Client error', 'status': 'Bad Request', 'statusCode': 400}, status=status.HTTP_400_BAD_REQUEST)
