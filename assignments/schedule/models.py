from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Account(models.Model):
    initials = models.CharField(max_length=4, blank=True)
    khsid = models.IntegerField(null=True, blank=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        if self.user.last_name and self.user.first_name:
            return self.user.last_name + ', ' + self.user.first_name
        return self.user.username


class PartCategory(models.Model):
    name = models.CharField(max_length=64)
    sort_order = models.IntegerField()

    def __str__(self):
        return self.name


class Part(models.Model):
    name = models.CharField(max_length=64)
    short_name = models.CharField(max_length=8)
    sort_order = models.IntegerField()

    khs_id_field = models.CharField(max_length=64, null=True, blank=True)
    khs_title_field = models.CharField(max_length=64, null=True, blank=True)

    category = models.ForeignKey(PartCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Assignment(models.Model):
    date = models.DateField()
    description = models.CharField(max_length=256, null=True)

    account = models.ForeignKey(Account)
    part = models.ForeignKey(Part)

    def __str__(self):
        return self.date.strftime('%m/%d/%Y') + ': ' + str(self.account)


class Incoming(models.Model):
    date = models.DateField()
    outline_name = models.CharField(max_length=256)
    speaker_full_name = models.CharField(max_length=256)
    congregation_name = models.CharField(max_length=128)


class Emailer(models.Model):
    days_before = models.IntegerField(default=2)

    account = models.ForeignKey(Account)
