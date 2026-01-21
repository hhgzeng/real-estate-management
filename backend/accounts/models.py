from django.db import models

class User(models.Model):
    ROLES = [
        ('customer', 'Customer'),
        ('salesperson', 'Salesperson'),
        ('admin', 'Administrator'),
    ]
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=20, choices=ROLES)

    def __str__(self):
        return self.username
