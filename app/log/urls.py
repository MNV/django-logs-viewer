from django.urls import path, include
from rest_framework.routers import DefaultRouter

from log import views


router = DefaultRouter()
router.register('count-by-types', views.LogViewSet)

app_name = 'log'

urlpatterns = [
    path('', include(router.urls))
]
