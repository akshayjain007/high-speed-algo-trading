# High Speed Algorithmic Trading
INTRODUCTION

Algorithmic trading (automated trading, black-box trading, or simply algo-trading) is the process of using computers programmed to follow a defined set of instructions for placing a trade in order to generate profits at a speed and frequency that is impossible for a human trader.

RSI : The relative strength index (RSI) is a technical momentum indicator that compares the magnitude of recent gains to recent losses in an attempt to determine overbought and oversold conditions of an asset. It is calculated using the following formula:

RSI = 100 - 100/(1 + RS*)

*Where RS = Average of x days' up closes / Average of x days' down closes.

SMA : A simple moving average (SMA) is a simple, or arithmetic, moving average that is calculated by adding the closing price of the security for a number of time periods and then dividing this total by the number of time periods. Short-term averages respond quickly to changes in the price of the underlying, while long-term averages are slow to react.

FILES

StockData.py : Class that reads the csv file of any stock containing the opening value, closing value and the corresponding date. It calculates the 50DaySma, 25DaySma and 14DayRSI and has get functions which provides different instances of the class to access the above mentioned arrays along with minRSI, maxRSI and the number of entries of that particular stock.

goog.csv : CSV file containing stock details of Alphabet for last one year

table.csv : CSV file containing stock details of Bharti Airtel Ltd. for last 14 years

algo_trading_serial.py : python file containing code base to compute the profit for the corresponding stock in a serial way. 
To run this file type "python algo_trading_serial.py" in terminal and look at the corresponding profit on the terminal

openclSample.py: python file on the OpenCL framework used for parallel computing using GPUs. OpenCl uses workers and gangs to achieve speedup by distributing the independent computing work among its various workers.
To run this file install OpenCL and typpe "python openclSample.py"

parallel_mpi.py :  Use of MPI for parallel computing



