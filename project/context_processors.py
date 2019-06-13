from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from project.helpers.LeagueApiHelpers import LolApiHelperInstance


def regions(request):
    server_regions = LolApiHelperInstance.regions
    server_regions_normaliser = LolApiHelperInstance.region_normalizer

    return {
        'server_regions': server_regions,
        'server_regions_normaliser': server_regions_normaliser,
    }
