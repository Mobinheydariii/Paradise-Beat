from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path('add-to-cart/<int:beat_id>/<int:licence_id>/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('remove-from-cart/<int:beat_id>/<int:licence_id>/', views.RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('view-cart/', views.ViewCartView.as_view(), name='view_cart'),
]