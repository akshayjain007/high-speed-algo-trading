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
avg_rsi = (min_rsi+max_rsi)/2

sma_50_day = alphabet_csv.SMA_50
sma_25_day = alphabet_csv.SMA_25

no_of_entries = len(volume_of_shares)-50

class AnalystClass:
    def __init__(self):
        self.csvFile = alphabet_csv

    def getRSIArray(self):
        return rsi_14_day

    def getSMA_50_day(self):
        return sma_50_day

    def getSMA_25_day(self):
        return sma_25_day
    
    def getVolumeOfShares(self):
        return volume_of_shares

    def getNumberOfEntries(self):
        return no_of_entries
        

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

for j in range(int(min_rsi),int(avg_rsi)):
    for k in range(int(avg_rsi), int(max_rsi)):
        init()
        upper_bound_rsi = k
        lower_bound_rsi = j
        for i in range(no_of_entries):
            calculate_profit(i)

        diff_num = total_sold - total_bought
        settled_profit = profit - diff_num*closing_value[0]
        # print("Total profit for lower %s and upper %s is %s  " % (j, k, settled_profit))
        # print total_sold, total_bought, j
