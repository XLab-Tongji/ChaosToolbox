from influxdb import InfluxDBClient
import time
import csv
import os
import json

client = InfluxDBClient('10.60.38.173', '8086')


class InfluxdbObserver(object):
    def __init__(self):
        pass

    @staticmethod
    def select_measurements(database):
        find = 0
        result_ = []
        path = os.path.abspath('./data/sock-measurements-InfluxDB.csv')

        response_database = client.get_list_database()
        for database_ in response_database:
            if database_['name'] == database:
                find = 1
        if find == 1:
            aim_client = InfluxDBClient('10.60.38.173', '8086', '', '', database)
            response_measurements = aim_client.query('show measurements;')
            if response_measurements:
                for set_ in response_measurements:
                    for dict_ in set_:
                        result_.append(dict_['name'])
                InfluxdbObserver.write_measurements_name(path, result_)
                return result_
            else:
                return "no measurements in " + database
        else:
            return "could not find the database, please check"

    @staticmethod
    def datetime_timestamp(dt):
        time.strptime(dt, '%Y-%m-%d %H:%M:%S')
        s = time.mktime(time.strptime(dt, '%Y-%m-%d %H:%M:%S'))
        result_ = str(int(s))+'000000000'
        return result_

    @staticmethod
    def select_measurements_values(database, measurements_name, start_time, end_time):
        csvset = []
        path = os.path.abspath('./data/InfluxDB-values.csv')
        start_ = InfluxdbObserver.datetime_timestamp(start_time)
        end_ = InfluxdbObserver.datetime_timestamp(end_time)
        aim_client = InfluxDBClient('10.60.38.173', '8086', '', '', database)
        response_values = aim_client.query('select * from ' +
                                           measurements_name + ' where time>' + start_ + ' and time<' + end_)
        if response_values:
            for set_ in response_values:
                for dict_ in set_:
                    csvset.append(dict_)
            InfluxdbObserver.write_to_csv(path, csvset)
            return csvset
        else:
            "response error , please check the param"

    @staticmethod
    def write_to_csv(filename, values):
        if not os.path.exists(filename):
            fd = open(filename, mode="w")
            fd.close()

        with open(filename, 'wb') as _file:
            writer = csv.writer(_file)
            headers = values[0].keys()
            writer.writerow(headers)

            for value in values:
                data_row = []
                for title in headers:
                    data_row.append(value[title])
                writer.writerow(data_row)

    @staticmethod
    def write_measurements_name(filename, measurements):

        if not os.path.exists(filename):
            fd = open(filename, mode="w")
            fd.close()

        with open(filename, 'wb') as _file:
            writer = csv.writer(_file)
            header = ['measurementName']
            writer.writerow(header)

            for measurement in measurements:
                temp = []
                temp.append(str(measurement))
                writer.writerow(temp)


