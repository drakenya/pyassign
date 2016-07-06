from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Account(models.Model):
    initials = models.CharField(max_length=4)
    khsid = models.IntegerField()

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.last_name + ', ' + self.user.first_name


class PartCategory(models.Model):
    name = models.CharField(max_length=64)
    sort_order = models.IntegerField()

    def __str__(self):
        return self.name


class Part(models.Model):
    name = models.CharField(max_length=64)
    short_name = models.CharField(max_length=8)
    sort_order = models.IntegerField()

    category = models.ForeignKey(PartCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Assignment(models.Model):
    date = models.DateField()
    description = models.CharField(max_length=256)

    account = models.ForeignKey(Account)
    part = models.ForeignKey(Part)

    def __str__(self):
        return self.date.strftime('%m/%d/%Y') + ': ' + str(self.account)