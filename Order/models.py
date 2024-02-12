from django.db import models
from operator import mod
from django.contrib.auth.models import User
from APIproduct.models import Product

class OrderStatus(models.TextChoices):
    PROCESSING='processing'
    SHIPPED='shipped'
    DELIVERED='delivered'
class PaymentMod(models.TextChoices):
    COD='cod'
    CARD='card'
class PaymentSatuts(models.TextChoices):
    PAID='Paid'
    UNPAID='Un Paid'
class Order(models.Model):
    city = models.CharField(max_length=400,default="",blank=False)
    zip_code = models.CharField(max_length=100 , default="", blank=False)
    street = models.CharField(max_length=500 , default="", blank=False)
    state = models.CharField(max_length=100 , default="", blank=False)
    country = models.CharField(max_length=100 , default="", blank=False)
    phone_num = models.CharField(max_length=100 , default="", blank=False)
    total_amount= models.IntegerField(default=0)
    payment_mod = models.CharField(max_length=30 , choices=PaymentMod.choices , default=PaymentMod.COD)
    payment_status = models.CharField(max_length=30 , choices=PaymentSatuts.choices , default=PaymentSatuts.UNPAID)
    orderstatus = models.CharField(max_length=30 , choices=OrderStatus.choices , default=OrderStatus.PROCESSING)
    user= models.ForeignKey(User,null=True, on_delete=models.SET_NULL)
    createA= models.DateTimeField(auto_now_add=True)
    def __str__(self):
      return  str(self.id)

class OrderItems(models.Model):
    product = models.ForeignKey(Product,null=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order,null=True, on_delete=models.CASCADE,related_name='orderitems')
    name = models.CharField(max_length=400 , default="", blank=False)
    quantity= models.IntegerField(default=1)
    price = models.DecimalField(max_digits=7, decimal_places=2,blank=False)

    def __str__(self):
      return  self.name
# Create your models here.
