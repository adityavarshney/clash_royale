from file_handler import read_stats, client
import pandas as pd
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np

def wins_and_losses(records):
	plt.plot(records['wins'] / (records['battleCount']))
	plt.title('Win Rate vs. Time')
	# plt.plot(records['losses'] / (records['battleCount']))
	# plt.legend()
	plt.show()


def trophies(records):
	plt.plot(records['trophies'])
	plt.title('Trophies vs. Time')
	plt.show()
	print('Average trophies per match: {}'.format(records.loc['trophies', len(records)-1] / records.loc['battleCount', -1]))


def run_all():
	records = read_stats(client)
	wins_and_losses(records)
	# trophies(records)


run_all()