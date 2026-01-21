from django.db import models
from accounts.models import User

class House(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    area = models.DecimalField(max_digits=10, decimal_places=2)
    floor = models.IntegerField()
    status = models.CharField(max_length=20, default='available')
    salesperson = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'salesperson'})

    def __str__(self):
        return f"House {self.id} - {self.status}"