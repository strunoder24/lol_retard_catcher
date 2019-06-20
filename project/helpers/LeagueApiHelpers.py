import requests
import json


class BaseInfo:
    _api_key = 'RGAPI-add6bf47-38bb-48a6-a8d3-8d5c259e56ed'

    @staticmethod
    def get_ddragon_last_version():
        ddragon_last_version = requests.get('https://ddragon.leagueoflegends.com/api/versions.json')
        versions_dict = json.loads(ddragon_last_version.text)
        return versions_dict[0]


class Summoners(BaseInfo):
    def _is_summoner_exist(self, username, region):
        response = requests.get(
            f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{username}?api_key={self._api_key}')
        if response.status_code == 200:
            return json.loads(response.text)

        elif response.status_code == 403:
            return {'status_code': 403, 'message': 'Не могу связатся с API игры'}

        return False

    def get_summoner(self, username, region):
        return self._is_summoner_exist(username, region)

    def get_summoner_icon_url(self, summoner=None, **kwargs):
        if summoner is not None:
            summoner_instance = summoner
        else:
            summoner_instance = self.get_summoner(kwargs['username'], kwargs['region'])

        last_version = self.get_ddragon_last_version()
        return (f'http://ddragon.leagueoflegends.com/cdn/{last_version}/img/profileicon/'
                f'{summoner_instance["profileIconId"]}.png')

    def summoner_formatter(self, summoner=None, **kwargs):
        if summoner is not None:
            summoner_instance = summoner
        else:
            summoner_instance = self.get_summoner(kwargs['username'], kwargs['region'])

        return {
            'id': summoner_instance['id'],
            'name': summoner_instance['name'],
            'level': summoner_instance['summonerLevel'],
            'profileIcon': self.get_summoner_icon_url(summoner_instance['name']),
        }


class Region:
    regions = {
                  'euw1': 'Europe West',
                  'ru': 'Россия',
                  'kr': 'Republic of Korea',
                  'br1': 'Brazil',
                  'oc1': 'Oceania',
                  'jp1': 'Japan',
                  'na1': 'North America',
                  'eun1': 'Europe Nordic and East',
                  'tr1': 'Turkey',
                  'la1': 'Latin America North',
                  'la2': 'Latin America South'
              }

    region_normalizer = {
                            'euw1': 'euw',
                            'ru': 'ru',
                            'kr': 'kr',
                            'br1': 'br',
                            'oc1': 'oc',
                            'jp1': 'jp',
                            'na1': 'na',
                            'eun1': 'eun',
                            'tr1': 'tr',
                            'la1': 'lan',
                            'la2': 'las'
                        }


class LolApiHelper(Summoners, Region):
    pass


LolApiHelperInstance = LolApiHelper()
