from django.urls import path, include
from rest_framework.routers import DefaultRouter

from log import views


router = DefaultRouter()
router.register(
    'count-by-types',
    views.CountByTypesViewSet,
    'count-by-types'
)
router.register(
    'search-by-body',
    views.SearchByBodyViewSet,
    'search-by-body'
)
router.register(
    'search-by-field',
    views.SearchByFieldViewSet,
    'search-by-field'
)

app_name = 'log'

urlpatterns = [
    path('', include(router.urls)),
]
