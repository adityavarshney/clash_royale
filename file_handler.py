from moto import MOTO_KEY, MY_HASH, MY_CLAN_HASH
import clashroyale.official_api as cr
import pandas as pd
from csv import DictWriter
import collections
import os
from pathlib import Path

DIR = 'user_data/'
EXT = '_stats.csv'

# build new client object
client = cr.Client(token=MOTO_KEY)
games_played = 0
ct = 0

def save_stats(client, player_hash=MY_HASH):
	global ct, games_played
	filename = DIR + player_hash + '_' + str(ct // 100) + EXT
	file_exists = os.path.isfile(filename)
	player_info = flatten(client.get_player(MY_HASH).raw_data)

	# if a new game has been played, update the log
	if player_info['battleCount'] > games_played:
		with open(filename, 'a+') as f:
			w = DictWriter(f, player_info.keys())
			if not file_exists:
				w.writeheader()
			w.writerow(player_info)
		ct += 1
		games_played = player_info['battleCount']
		return True
	return False

def read_stats(client, player_hash=MY_HASH):
	global ct
	filename = DIR + player_hash + '_' + str(ct // 100) + EXT
	records = pd.read_csv(filename)
	records.columns = flatten(client.get_player(MY_HASH).raw_data)
	return records


def delete_stats_file(player_hash=MY_HASH):
	global ct
	filename = DIR + player_hash + '_' + str(ct // 100) + EXT
	file_exists = os.path.isfile(filename)
	if file_exists:
		os.remove(filename)

# Helper functions

def flatten(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)
	

