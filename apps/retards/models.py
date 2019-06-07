from django.db import models
from django.contrib.auth import get_user_model


class Retard(models.Model):
    name = models.CharField(default='idiot', max_length=100)
    player = models.ForeignKey(get_user_model(), related_name='retards', on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    puuid = models.CharField(blank=True, max_length=78)
    summonerLevel = models.PositiveIntegerField(blank=True)
    revisionDate = models.CharField(blank=True, max_length=100)
    summonerId = models.CharField(max_length=63)
    accountId = models.CharField(max_length=56)

    def __str__(self):
        return self.name
