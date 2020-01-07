import pika

control_result = []
result_message = []


class RabbitMq:

    def __init__(self):
        pass

    @staticmethod
    def connect(the_inject_info):
        username = 'guest'
        pwd = 'guest'
        user_pwd = pika.PlainCredentials(username, pwd)
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='127.0.0.1', credentials=user_pwd
        ))
        channel = connection.channel()
        channel.queue_declare(queue='blade_mq')
        channel.basic_publish(exchange='', routing_key="blade_mq",
                              body="SUCCESS - " + str(the_inject_info))
        connection.close()

    @staticmethod
    def mq_control(dto):
        control_result.append(dto)
        length = len(control_result)
        return "now the rabbitMQ is opened:"+control_result[length-1]

    @staticmethod
    def control():
        length = len(control_result)
        if control_result:
            return control_result[length-1]
        else:
            return 'false'

    @staticmethod
    def clear_all_messages(queue):
        username = 'guest'
        pwd = 'guest'
        user_pwd = pika.PlainCredentials(username, pwd)
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='127.0.0.1', credentials=user_pwd
        ))
        channel = connection.channel()
        channel.queue_declare(queue=queue)
        channel.queue_delete(queue=queue)
        return "success"

    @staticmethod
    def consumer():
        result_message = []
        username = 'guest'
        pwd = 'guest'
        user_pwd = pika.PlainCredentials(username, pwd)
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='127.0.0.1', credentials=user_pwd))
        channel = connection.channel()
        channel.queue_declare(queue='blade_mq')
        i = 0
        while channel.basic_consume('blade_mq', RabbitMq.callback, False):
            channel.connection.process_data_events(time_limit=1)
            i = i + 1
            if i == 1:
                break
        return result_message

    @staticmethod
    def callback(channel, methos, property, body):
        result_message.append(body)

        print(body)


