# This is a bot that gets data from the LOTR api and tweets/toots random quotes
# https://the-one-api.dev/

import configparser, requests, random
from tweepy import OAuthHandler, API
from mastodon import Mastodon

# For automation it helps to have full path to script directory, ie /home/username/bot/
WRK_DIR = ''
# Read config file
config = configparser.ConfigParser()
config.read(f'{WRK_DIR}config')

# LOTR api access
lotr_access_token = config.get('LOTR_API', 'access_token')
headers = {'Authorization' : f'Bearer {lotr_access_token}'}
lotr_api_quote = 'https://the-one-api.dev/v2/quote?limit=2390'
quote_response = requests.get(lotr_api_quote, headers=headers).json()
random_index = random.randint(0, 2390)
quote = quote_response['docs'][random_index]
movie_id = quote['movie']
character_id = quote['character']
lotr_api_quote_movie = f'https://the-one-api.dev/v2/movie/{movie_id}'
lotr_api_quote_character = f'https://the-one-api.dev/v2/character/{character_id}'
movie = requests.get(lotr_api_quote_movie, headers=headers).json()
character = requests.get(lotr_api_quote_character, headers=headers).json()

print(quote['dialog'])
print(character['docs'][0]['name'])
print(movie['docs'][0]['name'])