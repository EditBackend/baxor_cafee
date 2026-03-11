from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import KitchenTicketViewSet
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'kitchen-tickets', KitchenTicketViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', obtain_auth_token, name='api_token_auth'),  # faqat 'token/' yoziladi
]