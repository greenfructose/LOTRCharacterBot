# This is a bot that gets data from the LOTR api and tweets/toots random quotes
# https://the-one-api.dev/

import configparser, requests, random
from datetime import datetime

from tweepy import OAuthHandler, API
from mastodon import Mastodon

# For automation it helps to have full path to script directory, ie /home/username/bot/
WRK_DIR = ''
# Read config file
config = configparser.ConfigParser()
config.read(f'{WRK_DIR}config')

# LOTR api access
lotr_access_token = config.get('LOTR_API', 'access_token')
headers = {'Authorization': f'Bearer {lotr_access_token}'}
lotr_api_quote = 'https://the-one-api.dev/v2/quote?limit=2390'
quote_response = requests.get(lotr_api_quote, headers=headers).json()
random_index = random.randint(0, 2390)
quote_response = quote_response['docs'][random_index]
movie_id = quote_response['movie']
character_id = quote_response['character']
lotr_api_quote_movie = f'https://the-one-api.dev/v2/movie/{movie_id}'
lotr_api_quote_character = f'https://the-one-api.dev/v2/character/{character_id}'
quote = quote_response['dialog']
movie = requests.get(lotr_api_quote_movie, headers=headers).json()['docs'][0]['name']
character = requests.get(lotr_api_quote_character, headers=headers).json()['docs'][0]['name']
quote = " ".join(quote.split()).replace(" ,", " ")
print(quote)
print(character)
print(movie)
print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
print('____________________________________________________________')

message = (f'"{quote.strip()}"\n'
           f'{character.strip()},\n'
           f'{movie.strip()}\n'
           f'Source: https://the-one-api.dev\n'
           f'#lotr #lordoftherings')

# Toot
mastodon_access_token = config.get('MASTODON_API', 'access_token')
mastodon_instance_url = config.get('MASTODON_API', 'instance_url')
mastodon = Mastodon(
    access_token=mastodon_access_token,
    api_base_url=mastodon_instance_url
)
mastodon.status_post(message)

# Tweet
consumer_key = config.get('TWITTER_API', 'consumer_key')
consumer_key_secret = config.get('TWITTER_API', 'consumer_key_secret')
oauth_token = config.get('TWITTER_API', 'oauth_token')
oauth_token_secret = config.get('TWITTER_API', 'oauth_token_secret')
account_screen_name = config.get('TWITTER_API', 'account_screen_name')
account_user_id = config.get('TWITTER_API', 'account_user_id')
auth = OAuthHandler(consumer_key, consumer_key_secret)
auth.set_access_token(oauth_token, oauth_token_secret)
twitter_api = API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
twitter_api.update_status(message)