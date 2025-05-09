from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import PhotoViewSet, ChildPhotoViewSet, ChildViewSet

# Create a router for children
router = DefaultRouter()
router.register(r'children', ChildViewSet, basename='child')

# Create a nested router for children and their photos
children_router = routers.NestedDefaultRouter(router, r'children', lookup='child')
children_router.register(r'photos', ChildPhotoViewSet, basename='child-photos')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(children_router.urls)),
] 