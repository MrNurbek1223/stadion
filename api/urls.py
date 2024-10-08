from django.urls import path, include
from rest_framework.routers import DefaultRouter
from maydon.views import *

router = DefaultRouter()
router.register(r'maydon', MaydonViewSet)

urlpatterns = [
    path('register/', register_user),
    path('login/', LoginAPIView.as_view(), name='token_obtain_pair'),
    path('bron/create/', BronCreateAPIView.as_view(), name='bron-create'),
    path('bron/update/<int:pk>/', BronUpdateAPIView.as_view(), name='bron-update'),
    path('bron/delete/<int:pk>/', BronDeleteAPIView.as_view(), name='bron-delete'),
]
urlpatterns += router.urls
