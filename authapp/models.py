import uuid
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser



# Create your models here.
class MainUser(AbstractUser):
    firstName = models.CharField(max_length=255, null=False, blank=False)
    lastName = models.CharField(max_length=255, null=False, blank=False)
    phone = models.CharField(max_length=255, null=False, blank=False)
    userId = models.UUIDField(default=uuid.uuid4, blank=False, unique=False)



class Organisation(models.Model):
    orgId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=False, blank=False)
    createdBy = models.ForeignKey(MainUser, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, null=True, blank=True)
    dateCreated = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    
class UserOrganisation(models.Model):
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    user = models.ForeignKey(MainUser, on_delete=models.CASCADE)
    dateCreated = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.first_name} - {self.organisation.name}"