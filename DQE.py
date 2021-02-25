import pandas as pd
import numpy as np

class DQE():

    def __init__(self):
        self.data = pd.read_excel('/Users/guoyx/Downloads/output.xlsx')

    # load data
    def get_data(self):
        return self.data

    # check missing value
    def check_missing(self, data, column_name: str):
        result = data[column_name][data[column_name].isnull()]
        Rp = len(result)
        Rt = len(data)
        DQ = Rp / Rt
        return DQ

    # check range
    def check_range(self, data, column_name: str, min, max):
        self.result = data[column_name][(data[column_name] < min) | (data[column_name] > max)]
        self.Rp = len(self.result)
        self.Rt = len(data)
        self.DQ = self.Rp / self.Rt
        return self.DQ

    # check normal
    # depending on different requirements

    # check duplicate
    # mainly check 'timestamp'
    # keep can be set as 'first','last' and 'False'
    def check_duplicate(self, data, column_name: str):
        self.result = data[column_name][data[column_name].duplicated(keep=False)]
        self.Rp = len(data) - len(self.result)
        self.Rt = len(data)
        self.DQ = self.Rp / self.Rt
        return self.DQ

    # check missing record
    # based on 'timestamp'
    def check_record(self, data):
        self.mask = data['timestamp'].diff() == float(data['timestamp'].diff().mode().values)
        self.result = data['timestamp'].diff()[self.mask]
        self.Rp = len(self.result) + 1
        print(self.Rp)
        self.Rt = len(data)
        print(self.Rt)
        self.DQ = self.Rp / self.Rt
        return self.DQ

    # check outlier
    # based on 3-sigma
    def check_outlier(self, data, column_name: str):
        self.mean = np.mean(data[column_name])
        self.std = np.std(data[column_name])
        self.threshold1 = self.mean - 3 * self.std
        self.threshold2 = self.mean + 3 * self.std
        self.result = data[column_name][(data[column_name] < self.threshold1) | (data[column_name] > self.threshold2)]
        self.Rp = len(data) - len(self.result)
        print(self.Rp)
        self.Rt = len(data)
        print(self.Rt)
        self.DQ = self.Rp / self.Rt
        return self.DQ

    # check stability
    def check_stability(self, data, column_name: str):
        self.result = data[column_name].kurt()
        return self.result

    # check balance
    def check_balance(self, data, column_name: str):
        self.result = data[column_name].skew()
        return self.result
