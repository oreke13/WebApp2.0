from django.db import models

class Student(models.Model):
    telegram_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=150)
    coins = models.IntegerField(default=0)  # Для хранения коинов

    def __str__(self):
        return self.username
