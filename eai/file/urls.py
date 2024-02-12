from django.urls import path, re_path
from .views import FileView
from .listviews import ListFileView

urlpatterns = [
    path('', FileView.as_view()),
    path('list/', ListFileView.as_view())
]