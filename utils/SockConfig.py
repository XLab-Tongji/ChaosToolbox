# -*- coding: utf-8 -*


class SockConfig(object):
    def __init__(self):
        pass

    # prometheus config
    PROMETHEUS_RESOLUTION = '10'  # default: 10s

    PROMETHEUS_HW_CONFIG = {
        'url': 'http://10.60.38.181:31003',
        'auth_user': 'admin',
        'auth_password': 'admin',
        'query_api': '/api/v1/query_range'
    }

    PROMETHEUS_VM_CONFIG = {
        'url': 'http://10.60.38.181:30003',
        'auth_user': 'admin',
        'auth_password': 'admin',
        'query_api': '/api/v1/query_range'
    }

    ENTITY_LIST_SERVICE = ['carts', 'catalogue', 'front-end', 'orders', 'payment', 'shipping', 'user']

    ENTITY_LIST_SERVICE_ERROR = ['front-end']

    ENTITY_LIST_CONTAINER = ['carts', 'carts-db', 'catalogue', 'catalogue-db', 'front-end', 'orders', 'orders-db',
                             'payment', 'shipping', 'user', 'user-db', 'rabbitmq', 'queue-master']

    ENTITY_LIST_NODE_HW = ['192.168.199.31:9100', '192.168.199.32:9100', '192.168.199.33:9100',
                           '192.168.199.34:9100', '192.168.199.35:9100']

    ENTITY_LIST_NODE_VM = ['192.168.199.21:9100', '192.168.199.22:9100', '192.168.199.23:9100',
                           '192.168.199.24:9100', '192.168.199.25:9100']

    QUERY_CONFIG_SERVICE_200 = {
        'entity_type': 'service',
        'metric_list': [
            'qps(2xx)',
            'latency'
        ],
        'query_list': [
            'sum(rate(request_duration_seconds_count{service="%s",status_code=~"2..",route!="metrics"}[1m]))',
            'sum(rate(request_duration_seconds_sum{service="%s"}[1m])) / sum(rate(request_duration_seconds_count{service="%s"}[1m]))'
        ]
    }

    QUERY_CONFIG_SERVICE_400 = {
        'entity_type': 'service',
        'entity_list': ['front-end', 'catalogue'],
        'metric_list': [
            'qps(4xx/5xx)'
        ],
        'query_list': [
            'sum(rate(request_duration_seconds_count{service="%s",status_code=~"4.+|5.+"}[1m]))'
        ]
    }

    QUERY_CONFIG_CONTAINER = {
        'entity_type': 'container',
        'metric_list': [
            'CPU Usage',
            'MEM Usage',
            'FS Reads Bytes',
            'FS Writes Bytes',
            'Network Input Bytes',
            'Network Output Bytes',
            'Network Input Packets',
            'Network Output Packets'
        ],
        'query_list': [
            'avg(rate (container_cpu_usage_seconds_total{image!="",container_name!="POD",namespace=~"sock-shop",pod_name=~"%s-[0-9A-Za-z]{3,}.+"}[5m]))',
            'avg(container_memory_usage_bytes{image!="",container_name!="POD",namespace=~"sock-shop",pod_name=~"%s-[0-9A-Za-z]{3,}.+"})',
            'sum (rate (container_fs_reads_bytes_total{image!="",namespace=~"sock-shop",pod_name=~"%s-[0-9A-Za-z]{3,}.+"}[5m]))',
            'sum (rate (container_fs_writes_bytes_total{image!="",namespace=~"sock-shop",pod_name=~"%s-[0-9A-Za-z]{3,}.+"}[5m]))',
            'sum (rate (container_network_receive_bytes_total{image!="",namespace=~"sock-shop",pod_name=~"%s-[0-9A-Za-z]{3,}.+"}[5m]))',
            'sum (rate (container_network_transmit_bytes_total{image!="",namespace=~"sock-shop",pod_name=~"%s-[0-9A-Za-z]{3,}.+"}[5m]))',
            'sum (rate (container_network_receive_packets_total{image!="",namespace=~"sock-shop",pod_name=~"%s-[0-9A-Za-z]{3,}.+"}[5m]))',
            'sum (rate (container_network_transmit_packets_total{image!="",namespace=~"sock-shop",pod_name=~"%s-[0-9A-Za-z]{3,}.+"}[5m]))'
        ]
    }

    QUERY_CONFIG_NODE = {
        'entity_type': 'node',
        'metric_list': [
            'System Load',
            'CPU Usage',
            'Memory Usage',
            'Disk Write',
            'Disk Read',
            'Network Received',
            'Network Transmitted'
        ],
        'query_list': [
            'node_load1{instance="%s"}',
            'max (sum by (cpu) (irate(node_cpu_seconds_total{mode!="idle", instance="%s"}[2m])) ) * 100',
            'node_memory_MemTotal_bytes{instance="%s"} - node_memory_MemFree_bytes{instance="%s"} - node_memory_Buffers_bytes{instance="%s"} - node_memory_Cached_bytes{instance="%s"}',
            'sum by (instance) (rate(node_disk_written_bytes_total{instance="%s"}[2m]))',
            'sum by (instance) (rate(node_disk_read_bytes_total{instance="%s"}[2m]))',
            'sum by (instance) (rate(node_network_receive_bytes_total{instance="%s",device!~"lo"}[5m]))',
            'sum by (instance) (rate(node_network_transmit_bytes_total{instance="%s",device!~"lo"}[5m]))'
        ]
    }

    QUERY_CONFIGS_VM = [
        {
            'prometheus': PROMETHEUS_VM_CONFIG,
            'queries': [
                {
                    'entity_list': ENTITY_LIST_SERVICE,
                    'query_config': QUERY_CONFIG_SERVICE_200
                },
                {
                    'entity_list': ENTITY_LIST_SERVICE_ERROR,
                    'query_config': QUERY_CONFIG_SERVICE_400
                },
                {
                    'entity_list': ENTITY_LIST_CONTAINER,
                    'query_config': QUERY_CONFIG_CONTAINER
                },{
                    'entity_list': ENTITY_LIST_NODE_VM,
                    'query_config': QUERY_CONFIG_NODE
                }
            ]
        }
    ]

    QUERY_CONFIGS_HW = [
        {
            'prometheus': PROMETHEUS_HW_CONFIG,
            'queries': [
                {
                    'entity_list': ENTITY_LIST_SERVICE,
                    'query_config': QUERY_CONFIG_SERVICE_200
                },
                {
                    'entity_list': ENTITY_LIST_SERVICE_ERROR,
                    'query_config': QUERY_CONFIG_SERVICE_400
                },
                {
                    'entity_list': ENTITY_LIST_CONTAINER,
                    'query_config': QUERY_CONFIG_CONTAINER
                }, {
                    'entity_list': ENTITY_LIST_NODE_HW,
                    'query_config': QUERY_CONFIG_NODE
                }
            ]
        }
    ]

    OUTPUTFILE = 'sock-results.csv'  # default: result.csv
    PERIOD = 1440  # unit: miniute, default 60, Resolution=10s
