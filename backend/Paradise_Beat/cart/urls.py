from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path('detail/', views.CartDetail.as_view()),
    path('add/<int:beat_id>/<int:licence>/', views.CartAddView.as_view()),
    path('remove/<int:beat_id>/', views.CartRemove.as_view())
]