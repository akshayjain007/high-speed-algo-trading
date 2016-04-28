import csv
import pandas as pd
from StockData import StockData

upper_bound_rsi = 0
lower_bound_rsi = 0

profits_list = []
total_stocks_sold_list = []
total_stocks_bought_list = []

#init basic variabls for each iteration
def init():
    global profit, total_bought, total_sold, stocks_left
    profit = 0
    total_bought = 0
    total_sold = 0
    stocks_left = 0
    return

#function to calculate profit
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
    return


analyst = StockData('goog.csv')
closing_value = analyst.getClosingValue()
rsi_14_day = analyst.getRSIArray()
sma_50_day = analyst.getSMA_50_day()
sma_25_day = analyst.getSMA_25_day()

max_rsi = analyst.getMaxRSI()
min_rsi = analyst.getMinRSI()
avg_rsi = analyst.getAverageRSI()

no_of_entries = analyst.getNumberOfEntries()

for j in range(min_rsi, avg_rsi):
# for j in range(33, 35):
    # for k in range(60, 65):
    for k in range(avg_rsi, max_rsi):
        init()
        upper_bound_rsi = k
        lower_bound_rsi = j
        for i in range(no_of_entries):
            calculate_profit(i)

        diff_num = total_sold - total_bought
        # print diff_num
        settled_profit = profit - diff_num*closing_value[0]
        print settled_profit
        profits_list.append(settled_profit)
        total_stocks_bought_list.append(total_bought)
        total_stocks_sold_list.append(total_sold)

max_profit = max(profits_list)
max_profit_index = profits_list.index(max(profits_list))

# print profits_list
print ("Total profit for %s stocks bought and %s sold is %s %s " % (total_stocks_bought_list[max_profit_index], total_stocks_sold_list[max_profit_index], max_profit, max_profit_index))
        # print("Total profit for lower %s and upper %s is %s  " % (j, k, settled_profit))
        # print total_sold, total_bought, j
