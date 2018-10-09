from django.db import models
from django.contrib.auth.models import User


class Agent(User):
    # номер ИНН, уникальный и длина ограничена
    number_inn = models.DecimalField(max_digits=12, decimal_places=0, unique=True)

class Order(models.Model):
    # ссылка на агента
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    # уникальный номер заказа
    number_order = models.IntegerField(unique=True)
    # цена, максимум 15 значное число, также показывает копейки
    price = models.DecimalField(max_digits=15, decimal_places=2)
    # дата создания
    date = models.DateTimeField(auto_now_add=True)
