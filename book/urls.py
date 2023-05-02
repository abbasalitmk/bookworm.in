from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls import handler404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('accounts.urls')),
    path('', include('user.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('order.urls')),
    path('dashboard/', include('dashboard.urls')),


]
handler404 = 'user.views.custom_error_page'


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_URL)
