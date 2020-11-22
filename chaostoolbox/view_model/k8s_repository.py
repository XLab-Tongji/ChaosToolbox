

class K8sRepository:
    def __init__(self):
        pass

    
    @staticmethod
    def create_k8s_pods_view_model(result):
        success = []

        try:
            for each_host in result['success']:
                for each_resource in result['success'][each_host.encode('raw_unicode_escape')]['resources']:
                    temp = dict()
                    temp['creationTimestamp'] = each_resource['metadata']['creationTimestamp']
                    temp['labels'] = each_resource['metadata']['labels']
                    temp['name'] = each_resource['metadata']['name']
                    temp['namespace'] = each_resource['metadata']['namespace']
                    temp['nodeName'] = each_resource['spec']['nodeName']
                    temp['hostIP'] = each_resource['status']['hostIP']
                    temp['podIP'] = each_resource['status']['podIP']
                    success.append(temp)
        except:
            success = {}

        result['detail'] = result['success']
        result['success'] = success
        return result