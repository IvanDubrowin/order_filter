from django.contrib.admin import AdminSite
from .models import Agent, Order


# регистрируем модели в админке
admin_site = AdminSite(name='admin')
admin_site.register([Agent, Order])
