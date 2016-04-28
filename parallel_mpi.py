import csv
import pandas as pd
from mpi4py import MPI
import numpy as np 

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
max_rsi = int(max(rsi_14_day))
min_rsi = int(min(rsi_14_day))

mid_rsi = int((max_rsi + min_rsi) / 2)
lower_count = mid_rsi - min_rsi + 1
upper_count = max_rsi - mid_rsi + 1

sma_50_day = alphabet_csv.SMA_50
sma_25_day = alphabet_csv.SMA_25

profit_matrix = np.zeros(shape=(lower_count, upper_count)).astype(np.float32)
profit_matrix_all = np.zeros(shape=(lower_count, upper_count)).astype(np.float32)

def pprint(string="", end="\n", comm=MPI.COMM_WORLD):
    if comm.rank == 0:
        print string

# Initializations and preliminaries
comm = MPI.COMM_WORLD   # get MPI communicator object
size = comm.size        # total number of processes
rank = comm.rank        # rank of this process
status = MPI.Status()   # get MPI status object

mpi_rows = int(np.floor(np.sqrt(comm.size)))
mpi_cols = comm.size / mpi_rows
if mpi_rows*mpi_cols > comm.size:
    mpi_cols -= 1
if mpi_rows*mpi_cols > comm.size:
    mpi_rows -= 1

row_segment = int(lower_count / mpi_rows)
col_segment = int(upper_count / mpi_cols)

pprint("Creating a %d x %d processor grid..." % (mpi_rows, mpi_cols) )
ccomm = comm.Create_cart( (mpi_rows, mpi_cols), periods=(True, True), reorder=True)
my_mpi_row, my_mpi_col = ccomm.Get_coords( ccomm.rank ) 

#print my_mpi_row, my_mpi_col
comm.barrier()

def init():
    global profit, total_bought, total_sold, stocks_left
    profit = 0
    total_bought = 0
    total_sold = 0
    stocks_left = 0
    return

no_of_entries = min(len(volume_of_shares), len(rsi_14_day), len(sma_50_day), len(sma_25_day))

def calculate_profit(upper_bound_rsi, lower_bound_rsi):
    profit = 0
    total_bought = 0
    total_sold = 0
    stocks_left = 0
    for i in range(no_of_entries):
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
    diff_num = total_sold - total_bought
    settled_profit = profit - diff_num*closing_value[0]
    #print settled_profit
    return settled_profit


comm.Barrier()                    ### Start stopwatch ###
t_start = MPI.Wtime()

row_offset = row_segment * my_mpi_row
col_offset = col_segment * my_mpi_col

for r in range(row_segment):
    current_row = r + row_offset
    for c in range(col_segment):
        current_col = c + col_offset
        temp = calculate_profit((max_rsi - current_col), (current_row + min_rsi))
        profit_matrix[current_row][current_col] = temp
        #print profit_matrix[current_row][current_col]

comm.Barrier()
#profit_matrix_all = comm.gather(profit_matrix, root=0)
comm.Reduce(profit_matrix, profit_matrix_all, op=MPI.SUM, root=0)
comm.Barrier()
pprint("Prifit all")
print(profit_matrix_all)
t_diff = MPI.Wtime() - t_start    ### Stop stopwatch ###

comm.Barrier()
if (comm.rank == 0):
    max_profit = 0.0
    x_index = 0
    y_index = 0
    for i in range(lower_count):
        for j in range(upper_count):
            compare = profit_matrix_all[i][j]
            if (compare > max_profit):
                max_profit = compare
                x_index = i
                y_index = j
    print "Min and Max", min_rsi, max_rsi
    print max_profit, (x_index+min_rsi), (max_rsi - y_index)
    print "__19 and 55 wala__", profit_matrix_all[0][37]
pprint("============================================================================")


comm.Barrier()

pprint("time taken by parallel part of code: %5.2fs" % t_diff)
pprint("============================================================================")

