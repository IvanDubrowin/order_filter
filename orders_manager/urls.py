
from django.urls import path
from orders_manager import views



urlpatterns = [
        path('', views.OrderView.as_view(), name='orders'),
        path('register/', views.RegistrationFormView.as_view(), name='register'),
]
