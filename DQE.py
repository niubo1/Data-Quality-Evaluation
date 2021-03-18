import pandas as pd
import numpy as np

class DQE():

    def __init__(self):
        self.data = pd.read_excel('/Users/user/Downloads/output.xlsx')

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
        result = data[column_name][(data[column_name] < min) | (data[column_name] > max)]
        Rp = len(result)
        Rt = len(data)
        DQ = Rp / Rt
        return DQ

    # check normal
    # depending on different requirements

    # check duplicate
    # mainly check 'timestamp'
    # keep can be set as 'first','last' and 'False'
    def check_duplicate(self, data, column_name: str):
        result = data[column_name][data[column_name].duplicated(keep=False)]
        Rp = len(data) - len(result)
        Rt = len(data)
        DQ = Rp / Rt
        return DQ

    # check missing record
    # based on 'timestamp'
    def check_record(self, data):
        mask = data['timestamp'].diff() == float(data['timestamp'].diff().mode().values)
        result = data['timestamp'].diff()[mask]
        Rp = len(result) + 1
        Rt = len(data)
        DQ = Rp / Rt
        return DQ

    # check outlier
    # based on 3-sigma
    def check_outlier(self, data, column_name: str):
        mean = np.mean(data[column_name])
        std = np.std(data[column_name])
        threshold1 = mean - 3 * std
        threshold2 = mean + 3 * std
        result = data[column_name][(data[column_name] < threshold1) | (data[column_name] > threshold2)]
        Rp = len(data) - len(result)
        Rt = len(data)
        DQ = Rp / Rt
        return DQ

    # check stability
    def check_stability(self, data, column_name: str):
        result = data[column_name].kurt()
        return result

    # check balance
    def check_balance(self, data, column_name: str):
        result = data[column_name].skew()
        return result