from django.urls import include, path
from rest_framework import routers
# from django.urls.conf import re_path
from . import views

router = routers.DefaultRouter()
router.register(r'todo', views.TODOViewSet)

urlpatterns = [
    path('', include(router.urls)),    
]
