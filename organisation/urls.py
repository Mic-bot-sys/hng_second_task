from django.urls import path
from . import views

urlpatterns = [
    path('users/<str:userId>/', views.get_user_record, name="get_user_record"),
    path('organisations/', views.get_organisations_by_userId, name="get_organisations_by_userId"),
    path('organisations/<str:orgId>/', views.get_an_organisation_by_id, name="get_an_organisation_by_id"),
    path('organisations/:orgId/users', views.add_user_to_an_organisation, name="add_user_to_organisation"),
]
