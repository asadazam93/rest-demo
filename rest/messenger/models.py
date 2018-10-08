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
