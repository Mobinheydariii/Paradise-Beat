from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views


app_name = "beats"


urlpatterns = []

router = DefaultRouter()
router.register(r'beat', views.BeatViewSet, basename='beat')
urlpatterns += router.urls