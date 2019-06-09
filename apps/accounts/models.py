from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from project.helpers.LeagueApiHelpers import LolApiHelperInstance


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), related_name='profile', on_delete=models.CASCADE)
    region = models.CharField(max_length=50, choices=LolApiHelperInstance.regions.items(), blank=True)
    icon = models.CharField(max_length=100, blank=True)
    level = models.PositiveIntegerField(blank=True, default=1)
    encrypted_id = models.CharField(max_length=100, blank=True)

    @receiver(post_save, sender=get_user_model())
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=get_user_model())
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
