from django.db import models
from django.contrib.auth import get_user_model

from project.helpers.LeagueApiHelpers import LolApiHelperInstance


class Profile(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='profile', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    encrypted_id = models.CharField(max_length=100)
    region = models.CharField(max_length=50, choices=LolApiHelperInstance.regions.items())
    icon = models.CharField(max_length=100, blank=True)
    level = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name
