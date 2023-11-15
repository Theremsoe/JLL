from django.db import models


class Account(models.Model):
    id = models.BigAutoField(primary_key=True)
    balance = models.IntegerField(default=0)


class Payment(models.Model):
    id = models.BigAutoField(primary_key=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='payments')
    amount = models.IntegerField()
