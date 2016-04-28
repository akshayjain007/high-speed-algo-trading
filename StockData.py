import csv
import pandas as pd

class StockData:
    
    def __init__(self,filename):
        alphabet_csv = pd.read_csv(filename)
        self.csvFile = alphabet_csv
        self.closing_value = alphabet_csv.Close
        self.volume_of_shares = alphabet_csv.Volume
        
        self.max_volume = max(self.volume_of_shares)
        self.min_volume = min(self.volume_of_shares)

        self.rsi_14_day = alphabet_csv.RSI_day_14
        self.max_rsi = max(self.rsi_14_day)
        self.min_rsi = min(self.rsi_14_day)
        self.avg_rsi = (self.min_rsi+self.max_rsi)/2

        self.sma_50_day = alphabet_csv.SMA_50
        self.sma_25_day = alphabet_csv.SMA_25

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