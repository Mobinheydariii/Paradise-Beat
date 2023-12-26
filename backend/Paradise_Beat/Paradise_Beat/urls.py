from django.contrib import admin
from django.urls import path, include
from . import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls', namespace="account")),
    path('', include('beats.urls', namespace="beats")),
    path('cart/', include('cart.urls', namespace="cart"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
