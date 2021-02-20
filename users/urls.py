from django.urls import path
from .views import *

app_name = "users"

urlpatterns = [
    path('', Dashboard, name="dashboard"),
    path('add-user/', AddUser.as_view(), name="add_user"),
    path('List-Users/', ListUsers.as_view(), name="list_users"),
    path('Update-Users/<int:pk>/', UpdateUsers.as_view(), name="update_user"),
    # path('add-retailer/', AddRetailer.as_view(), name="add_retailer"),
]