from influxdb import InfluxDBClient
import time
import csv

client = InfluxDBClient('10.60.38.173', '8086')


class InfluxdbObserver(object):
    def __init__(self):
        pass

    @staticmethod
    def select_measurements(database):
        find = 0
        result_ = []
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
        start_ = InfluxdbObserver.datetime_timestamp(start_time)
        end_ = InfluxdbObserver.datetime_timestamp(end_time)
        aim_client = InfluxDBClient('10.60.38.173', '8086', '', '', database)
        response_values = aim_client.query('select * from ' +
                                           measurements_name + ' where time>' + start_ + ' and time<' + end_)
        if response_values:
            for set_ in response_values:
                for dict_ in set_:
                    csvset.append(dict_)
            return csvset
        else:
            "response error , please check the param"

    @staticmethod
    def write_to_csv(filename, measurements, values, print_data_time):

        with open(filename, 'wb') as file:
            writer = csv.writer(file)

