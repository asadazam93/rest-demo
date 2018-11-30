from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    text = models.CharField(max_length=255, blank=True, default='')
    sender = models.ForeignKey(
        User,
        verbose_name='Sender',
        on_delete=models.CASCADE,
        related_name='sender',
        null=False
    )

    receiver = models.ForeignKey(
        User,
        verbose_name='Receiver',
        on_delete=models.CASCADE,
        related_name='receiver',
        null=False
    )


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    longitude = models.FloatField()
    latitude = models.FloatField()
    distance_from_location = models.FloatField(default=0.00)
    categories = models.ManyToManyField(Category, blank=True, related_name='restaurants')

    def __str__(self):
        return self.name
