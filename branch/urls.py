from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import BranchViewSet
from rest_framework.authtoken.views import obtain_auth_token


router = DefaultRouter()
router.register(r'branches', BranchViewSet)

urlpatterns = router.urls

urlpatterns = [
    path('api/token/', obtain_auth_token)
    ]