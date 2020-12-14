# -*- coding: utf-8 -*

import requests
import logging
import datetime

from utils.SockConfig import Config


class PerformanceDataPicker(object):
    def __init__(self):
        pass

    @staticmethod
    def build_entity_metrics(query_config):
        entity_metrics = []
        # conbine entityNames and entityMetrics
        type = query_config['entity_type']
        for entity in query_config['entity_list']:
            for metric in query_config['metric_list']:
                entity_metrics.append(type+'/'+entity+"/"+metric)
        return entity_metrics

    @staticmethod
    def build_entity_metrics(query_config, entity_list):
        entity_metrics = []
        # conbine entityNames and entityMetrics
        type = query_config['entity_type']
        for entity in entity_list:
            for metric in query_config['metric_list']:
                entity_metrics.append(type+'/'+entity+"/"+metric)
        return entity_metrics

    @staticmethod
    def query_entity_metric_values(query_config, resolution, end_time, start_time, null_value='null'):

        metricnames = PerformanceDataPicker.build_entity_metrics(query_config=query_config)

        query_list = query_config['query_list']
        prometheus_config = query_config['prometheus']
        csvset = dict()
        for index in range(len(metricnames)):
            list = metricnames[index].split('/')
            query = query_list[index % len(query_list)].replace("%s",list[1])
            response = requests.get(prometheus_config['url'] + prometheus_config['query_api'],
                                    params={
                                        'query': query, 'start': start_time,
                                        'end': end_time, 'step': resolution},
                                    auth=(prometheus_config['auth_user'], prometheus_config['auth_password']))
            # print(response.json())
            results = response.json()['data']['result']
            if results != []:
                for value in results[0]['values']:
                    datum = value[1]
                    if datum == 'NaN':
                        datum = null_value
                    if index == 0:
                        csvset[value[0]] = [datum]
                    else:
                        if value[0] in csvset:
                            csvset[value[0]].append(datum)
                        else:
                            # print(results)
                            csvset[value[0]] = []
                            for count in range(index):
                                csvset[value[0]].append(null_value)
                            csvset[value[0]].append(value[1])
                for timestamp in csvset.keys():
                    if len(csvset[timestamp]) <= index:
                        csvset[timestamp].append(null_value)
            else:
                for timestamp in csvset.keys():
                    csvset[timestamp].append(null_value)
            # 按竖列输出的数据！！！null代表没有该项数据
        return metricnames, csvset

    @staticmethod
    def query_entity_metric_values(prometheus, entity_list, query_config, resolution, end_time, start_time, null_value='null'):

        metricnames = PerformanceDataPicker.build_entity_metrics(query_config=query_config, entity_list=entity_list)

        query_list = query_config['query_list']
        prometheus_config = prometheus
        csvset = dict()
        for index in range(len(metricnames)):
            list = metricnames[index].split('/')
            query = query_list[index % len(query_list)].replace("%s",list[1])
            response = requests.get(prometheus_config['url'] + prometheus_config['query_api'],
                                    params={
                                        'query': query, 'start': start_time,
                                        'end': end_time, 'step': resolution},
                                    auth=(prometheus_config['auth_user'], prometheus_config['auth_password']))
            # print(response.json())
            results = response.json()['data']['result']
            if results != []:
                for value in results[0]['values']:
                    datum = value[1]
                    if datum == 'NaN':
                        datum = null_value
                    if index == 0:
                        csvset[value[0]] = [datum]
                    else:
                        if value[0] in csvset:
                            csvset[value[0]].append(datum)
                        else:
                            # print(results)
                            csvset[value[0]] = []
                            for count in range(index):
                                csvset[value[0]].append(null_value)
                            csvset[value[0]].append(value[1])
                for timestamp in csvset.keys():
                    if len(csvset[timestamp]) <= index:
                        csvset[timestamp].append(null_value)
            else:
                for timestamp in csvset.keys():
                    csvset[timestamp].append(null_value)
            # 按竖列输出的数据！！！null代表没有该项数据
        return metricnames, csvset

    @staticmethod
    def query_multi_entity_metric_values(queryconfiglist, resolution, end_time, start_time):
        metricnamelist = []
        csvsets = []

        for prometheus_config in queryconfiglist:
            # print(config)
            # metricnames, csvset = PerformanceDataPicker.query_entity_metric_values(query_config=config,
            #                                                           resolution=resolution,
            #                                                           end_time=end_time,
            #                                                           start_time=start_time)
            queries = prometheus_config['queries']
            for query in queries:
                metricnames, csvset = PerformanceDataPicker.query_entity_metric_values(
                                                                      prometheus=prometheus_config['prometheus'],
                                                                      entity_list=query['entity_list'],
                                                                      query_config=query['query_config'],
                                                                      resolution=resolution,
                                                                      end_time=end_time,
                                                                      start_time=start_time)
                metricnamelist.append(metricnames)
                csvsets.append(csvset)
        return metricnamelist, csvsets



