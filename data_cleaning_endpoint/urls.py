from django.urls import path, re_path
from .checking_views import *
from .handling_views import *
from .views import master_handler

urlpatterns = [
    path('<feat>/', master_handler)
]