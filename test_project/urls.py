from django.contrib import admin
from django.conf.urls import include
from django.conf.urls.static import static
from django.urls import path
from orders_manager.admin import admin_site
from test_project import settings

urlpatterns = [
    path('admin/', admin_site.urls),
    path('', include(('orders_manager.urls', 'orders_manager'), namespace='orders_manager')),
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
