# -*- coding: utf-8 -*

import requests
import time
import logging
import os

from view_model.prometheus_repository import PrometheusRepository
from utils.config import Config

from utils.SockConfig import SockConfig
from utils.utils import Utils
from controller.prometheus.PerformanceDataPicker import PerformanceDataPicker
from controller.prometheus.PerformanceDataWriter import PerformanceDataWriter


class PrometheusObserver(object):
    def __init__(self):
        pass

    @staticmethod
    def build_entity_metrics(queryConfig):
        entityMetrics = []
        #conbine entityNames and entityMetrics
        type = queryConfig['entity_type']
        for entity in queryConfig['entity_list']:
            for metric in queryConfig['metric_list']:
                entityMetrics.append(type+'/'+entity+"/"+metric)
        return entityMetrics

    @staticmethod
    def query_entity_metric_values(metricnames, querylist, prometheusConfig, resolution, end_time, start_time, timeout):
        csvset = dict()
        for index in range(len(metricnames)):
            list = metricnames[index].split('/')
            query = querylist[index % len(querylist)] % list[1]
            response = requests.get(prometheusConfig['url'] + prometheusConfig['query_api'],
                                    params={
                                        'query': query,
                                        'start': start_time,
                                        'end': end_time,
                                        'step': resolution,
                                        'timeout': timeout},
                                    auth=(prometheusConfig['auth_user'], prometheusConfig['auth_password']))

            results = response.json()['data']['result']
            print(results)
            if results != []:
                for value in results[0]['values']:
                    if index == 0:
                        csvset[value[0]] = [value[1]]
                    else:
                        if value[0] in csvset:
                            csvset[value[0]].append(value[1])
                        else:
                            # print(results)
                            csvset[value[0]] = []
                            for count in range(index):
                                csvset[value[0]].append('null')
                            csvset[value[0]].append(value[1])
                for timestamp in csvset.keys():
                    if len(csvset[timestamp]) <= index:
                        csvset[timestamp].append("null")
            else:
                for timestamp in csvset.keys():
                    csvset[timestamp].append("null")
            # 按竖列输出的数据！！！null代表没有该项数据
        return csvset

    @staticmethod
    def datetime_timestamp(dt):
        # dt为字符串
        # 中间过程，一般都需要将字符串转化为时间数组
        time.strptime(dt, '%Y-%m-%d %H:%M:%S')
        ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=-1)
        # 将"2012-03-28 06:53:40"转化为时间戳
        s = time.mktime(time.strptime(dt, '%Y-%m-%d %H:%M:%S'))
        return int(s)

    @staticmethod
    def run(dto):
        # 处理开始时间和结束时间
        end_time = PrometheusObserver.datetime_timestamp(dto['to'])
        start_time = PrometheusObserver.datetime_timestamp(dto['from'])

        metricnames1 = PrometheusObserver.build_entity_metrics(Config.QUERY_CONFIG1)
        csvset1 = PrometheusObserver.query_entity_metric_values(
            metricnames=metricnames1,
            querylist=Config.QUERY_CONFIG1['query_list'],
            prometheusConfig=Config.PROMETHEUS_CONFIG1,
            resolution=Config.PROMETHEUS_RESOLUTION,
            start_time=start_time,
            end_time=end_time,
            timeout=Config.PROMETHEUS_TIMEOUT
        )

        metricnames2 = PrometheusObserver.build_entity_metrics(Config.QUERY_CONFIG2)
        csvset2 = PrometheusObserver.query_entity_metric_values(
            metricnames=metricnames2,
            querylist=Config.QUERY_CONFIG2['query_list'],
            prometheusConfig=Config.PROMETHEUS_CONFIG2,
            resolution=Config.PROMETHEUS_RESOLUTION,
            start_time=start_time,
            end_time=end_time,
            timeout=Config.PROMETHEUS_TIMEOUT
        )

        datasetHeader = []
        datasetHeader += metricnames1
        datasetHeader += metricnames2

        # 生成数据集
        logging.info("Querying metric values succeeded, rows of data: %s", len(csvset1))
        return PrometheusRepository.create_prometheus_stream_view_model(datasetHeader, csvset1, csvset2)

    @staticmethod
    def sock_performance_picker(dto):
        # START_STR = "2019-12-18 14:00:00"
        # END_STR = "2019-12-18 14:00:08"
        START_STR = dto['start']
        END_STR = dto['end']
        RESOLUTION = SockConfig.PROMETHEUS_RESOLUTION

        end_time = Utils.datetime_timestamp(END_STR)
        start_time = Utils.datetime_timestamp(START_STR)

        headers, csvsets = PerformanceDataPicker.query_multi_entity_metric_values(
                                        queryconfiglist=SockConfig.QUERY_CONFIGS_HW,
                                        resolution=SockConfig.PROMETHEUS_RESOLUTION,
                                        start_time=start_time,
                                        end_time=end_time)

        path = os.path.abspath('./data/sock-results-HW_10-23.csv')

        PerformanceDataWriter.write2csv_merged(filename=path,
                                           metricsnameset=headers, datasets=csvsets)
        return 'success'


if __name__ == '__main__':
    dto = {
        'to': '2019-10-11 15:32:00',
        'from': '2019-10-11 15:22:30'
    }
    result = PrometheusObserver.run(dto)
