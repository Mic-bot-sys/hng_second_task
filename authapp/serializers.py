from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

from authapp.models import MainUser, Organisation, UserOrganisation

# Serializers define the API representation.
class UserInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainUser
        fields = ['firstName', 'lastName', 'email', 'password', "phone"]
        
        def validate(self, data):
            if isinstance(data["firstName"], str) and isinstance(data["lastName"], str):
                return data
            return serializers.ValidationError({"error": "firstName is a string object"})
                


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainUser
        fields = ['email', "password"]
                


class UserOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainUser
        fields = ['firstName', 'lastName', 'email', "phone", "userId"]
                


class OrganisationInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ['orgId', 'name', 'description']
                


class OrganisationOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ['name', 'description', "orgId"]


class OrganisationPostOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ['name', 'description']
                


class UserOrganisationSerializer(serializers.ModelSerializer):
    organisation = OrganisationOutputSerializer()
    
    class Meta:
        model = UserOrganisation
        fields = ['organisation']