from django.db import models
from django.core.validators import MinValueValidator


class SapphireCard(models.Model):
    card_id = models.CharField(primary_key=True, unique=True, max_length=14)
    sapphires = models.IntegerField(MinValueValidator)
    is_recharge = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    class Meta:
        db_table = 'SapphireCards'
        ordering = ['-sapphires']
