from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    ordered_by=models.ForeignKey(User,on_delete=models.CASCADE)
    stock_name=models.CharField(max_length=64,null=False)
    quantity=models.PositiveIntegerField()
    type=models.CharField(max_length=6)
    executed_qty=models.PositiveIntegerField()
    price=models.PositiveBigIntegerField(default=0)
    status=models.CharField(max_length=15)
    date=models.DateField(null=False,blank=False)


class Market(models.Model):
    status=models.CharField(max_length=10)
