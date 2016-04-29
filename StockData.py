import csv
import pandas as pd

class StockData:
        
    diff_list = []
    gain = []
    loss = []
    avg_gain = []
    avg_loss = []
    RS = []
    rsi_14_day = []
    sma_50_day = []
    sma_25_day = []

    def __init__(self,filename):
        alphabet_csv = pd.read_csv(filename)
        self.csvFile = alphabet_csv
        self.opening_value = alphabet_csv.Open
        self.closing_value = alphabet_csv.Close
        self.volume_of_shares = alphabet_csv.Volume
        
        self.max_volume = max(self.volume_of_shares)
        self.min_volume = min(self.volume_of_shares)

        for i in range(len(self.opening_value)):
            diff = self.closing_value[i] - self.opening_value[i]
            self.diff_list.append(diff)
            if diff>0:
                self.gain.append(diff)
                self.loss.append(0)
            else:
                self.gain.append(0)
                self.loss.append(-diff)

        for j in range(len(self.opening_value)-50):
            gain_avg = 0
            loss_avg = 0
            sum_50_day = 0
            sum_25_day = 0
            for k in range(j+1, j+15):
                gain_avg = gain_avg + self.gain[k]
                loss_avg = loss_avg + self.loss[k]
            self.avg_gain.append(gain_avg/14)
            self.avg_loss.append(loss_avg/14)
            self.RS.append(gain_avg/loss_avg)
            self.rsi_14_day.append(100-100/(1+self.RS[j]))

            for l in range(j+1, j+51):
                sum_50_day = sum_50_day + self.closing_value[l]
            self.sma_50_day.append(sum_50_day/50)

            for m in range(j+1, j+26):
                sum_25_day = sum_25_day + self.closing_value[m]
            self.sma_25_day.append(sum_25_day/25)

        # self.rsi_14_day = alphabet_csv.RSI_day_14
        self.max_rsi = max(self.rsi_14_day)
        self.min_rsi = min(self.rsi_14_day)
        self.avg_rsi = (self.min_rsi+self.max_rsi)/2

        # self.sma_50_day = alphabet_csv.SMA_50
        # self.sma_25_day = alphabet_csv.SMA_25

    def getRSIArray(self):
        return self.rsi_14_day

    def getSMA_50_day(self):
        return self.sma_50_day

    def getSMA_25_day(self):
        return self.sma_25_day
    
    def getVolumeOfShares(self):
        return self.volume_of_shares
        
    def getClosingValue(self):
        return self.closing_value

    def getNumberOfEntries(self):
        no_of_entries = len(self.volume_of_shares)-50
        return no_of_entries
        
    def getMaxRSI(self):
        return int(self.max_rsi)

    def getMinRSI(self):
        return int(self.min_rsi)

    def getAverageRSI(self):
        return int(self.avg_rsi)