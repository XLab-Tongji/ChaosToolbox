import csv

from utils.utils import Utils

class PerformanceDataWriter(object):
    def __init__(self):
        pass

    @staticmethod
    def write2csv_single(filename, metricnames, dataset, printdatetime=True):
        num = 0
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            headers = ['timestamp']
            if printdatetime:
                headers.append('datetime')
            headers += metricnames
            writer.writerow(headers)
            for timestamp in sorted(dataset.keys()):
                # num = num + 1
                # if (num>lines): break
                data_row = [timestamp]
                if printdatetime:
                    data_row.append(Utils.timestamp_datetime(timestamp))
                data_row += dataset[timestamp]
                writer.writerow(data_row)

    @staticmethod
    def write2csv_merged(filename, metricsnameset, datasets, printdatetime=True):

        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            headers = ['timestamp']
            if printdatetime:
                headers.append('datetime')
            for metricnames in metricsnameset:
                headers += metricnames
            writer.writerow(headers)

            timestamps = datasets[0].keys()
            for timestamp in sorted(timestamps):
                data_row = [timestamp]
                if printdatetime:
                    data_row.append(Utils.timestamp_datetime(timestamp))
                for i,dataset in enumerate(datasets):
                    if timestamp in dataset:
                        data_row += dataset[timestamp]
                    else:
                        length = len(metricsnameset[i])
                        for i in range(length):
                            data_row.append('null')
                writer.writerow(data_row)