from django.db import models
from shortuuid.django_fields import ShortUUIDField
from userauths.models import User
from django.utils.html import mark_safe

from datetime import timedelta


# Create your models here.
STATUS_CHOICE = (
    ("not processed", "Not Processed"),
    ("processing", "Processing"),
    ("paid", "Paid"),
)
STATUS = (
    ("daily", "daily"),
    ("weekly", "weekly"),
    ("monthly", "monthly"),
    ("hourly", "hourly"),
)
def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)
class Plan(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="plan", alphabet="abcdefgh12345") #product uuid field
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    user_count = models.IntegerField(default="100")
    title = models.CharField(max_length=100, default="Plan")
    description = models.TextField(null=True, blank=True)
    initial = models.CharField(max_length=7, default="BTC")
    image = models.ImageField(upload_to=user_directory_path, default="product.jpg")
    least_amount = models.IntegerField(default="100")
    max_amount = models.IntegerField(default="100")
    interval = models.CharField(choices=STATUS, max_length=16, default="daily")
    invested_amount = models.DecimalField(max_digits=1000, decimal_places=2, default="0.00")
    percentage_return = models.DecimalField(max_digits=1000, decimal_places=2, default="1.99")
    featured = models.BooleanField(default=False)
    payment_status = models.CharField(choices=STATUS_CHOICE, max_length=16, default="in_review")
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        verbose_name_plural = "Plans"

    def __str__(self):
        return self.title
    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    def get_profit(self):
        value = ((self.percentage_return)/100)*self.invested_amount
        profit = self.invested_amount + value
        return profit

class UserComplaints(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    question = models.CharField(max_length=50)
    question_details = models.TextField(null=True, blank=True)
    class Meta:
        verbose_name_plural = "Users Complaints"
    def __str__(self):
        return self.name
    
class BtcAddress(models.Model):
    address = models.CharField(max_length=100, default="btc address")
    initial = models.CharField(max_length=10, default="BTC")
    class Meta:
        verbose_name_plural = "BTC Address"
    def __str__(self):
        return self.address
    
class EthAddress(models.Model):
    address = models.CharField(max_length=100, default="eth address")
    initial = models.CharField(max_length=10, default="ETH")
    class Meta:
        verbose_name_plural = "ETH Address"
    def __str__(self):
        return self.address
    
class OtherAddress(models.Model):
    address = models.CharField(max_length=100, default="eth address")
    initial = models.CharField(max_length=10, default="Other")
    class Meta:
        verbose_name_plural = "USDT Address"
    def __str__(self):
        return self.address