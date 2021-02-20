from django.urls import path

from .views import AddTrans

urlpatterns = [
    path('add-trans', AddTrans.as_view(), name="add_trans"),
]