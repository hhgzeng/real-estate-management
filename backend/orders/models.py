from django.db import models
from accounts.models import User
from houses.models import House

class Order(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE)

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'customer'},
        related_name='customer_orders'  # 解决冲突：为 customer 指定一个唯一的 related_name
    )

    salesperson = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'salesperson'},
        related_name='salesperson_orders'  # 解决冲突：为 salesperson 指定一个唯一的 related_name
    )

    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.house.id}"
