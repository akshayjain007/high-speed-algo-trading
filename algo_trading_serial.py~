import csv
import pandas as pd

profit = 0
total_sold = 0
total_bought = 0
stocks_left = 0
upper_bound_rsi = 0
lower_bound_rsi = 0
range_for_bound = 15

alphabet_csv = pd.read_csv('goog.csv')
closing_value = alphabet_csv.Close
volume_of_shares = alphabet_csv.Volume
max_volume = max(volume_of_shares)
min_volume = min(volume_of_shares)

rsi_14_day = alphabet_csv.RSI_day_14
max_rsi = max(rsi_14_day)
min_rsi = min(rsi_14_day)

sma_50_day = alphabet_csv.SMA_50
sma_25_day = alphabet_csv.SMA_25

def init():
	global profit, total_bought, total_sold, stocks_left
	profit = 0
	total_bought = 0
	total_sold = 0
	stocks_left = 0
	return

def calculate_profit(i):
	global profit, total_bought, total_sold, stocks_left
	if (rsi_14_day[i]> upper_bound_rsi and sma_25_day[i]<sma_50_day[i]):
		profit = profit - closing_value[i]
		total_bought = total_bought + 1
		stocks_left = stocks_left + 1
		# print "Buying a volume_of_shares"
	elif (rsi_14_day[i]<lower_bound_rsi and sma_25_day[i]>sma_50_day[i]):
		if stocks_left > 0:
			profit = profit + closing_value[i]
			total_sold = total_sold + 1
			stocks_left -= 1
		# print "Selling a share"
	# else:
		# print "No action"
	return

no_of_entries = min(len(volume_of_shares), len(rsi_14_day), len(sma_50_day), len(sma_25_day))

for j in range(15,25):
	init()
	upper_bound_rsi = max_rsi - j
	lower_bound_rsi = min_rsi + j
	for i in range(no_of_entries):
		calculate_profit(i)

	diff_num = total_sold - total_bought
	settled_profit = profit - diff_num*closing_value[0]
	print("Total profit for %s is %s  " % (j, settled_profit))

	print total_sold, total_bought, j
