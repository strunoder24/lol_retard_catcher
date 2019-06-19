from django.db import models
from apps.accounts.models import Profile


class Retard(models.Model):
    name = models.CharField(default='SirGay', max_length=100)
    player = models.ForeignKey(Profile, related_name='retards', on_delete=models.CASCADE)
    icon = models.CharField(max_length=100, blank=True)
    description = models.CharField(blank=True, max_length=1000)
    encrypted_id = models.CharField(blank=True, max_length=100)
    level = models.PositiveIntegerField(blank=True)

    def __str__(self):
        return self.name
