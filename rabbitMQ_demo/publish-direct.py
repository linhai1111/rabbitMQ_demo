__author__ = 'Administrator'
import pika
import sys

credentials = pika.PlainCredentials('tom', '123')

parameters = pika.ConnectionParameters(host='192.168.121.128',credentials=credentials)
connection = pika.BlockingConnection(parameters)

channel = connection.channel() #队列连接通道

channel.exchange_declare(exchange='direct_log',exchange_type='direct')

log_level =  sys.argv[1] if len(sys.argv) > 1 else 'info'   # sys.argv[1]代表从命令行接收的参数，作为关键字

message = ' '.join(sys.argv[1:]) or "info: Hello World!"

channel.basic_publish(exchange='direct_log',
                      routing_key=log_level, # 关键字
                      body=message)
print(" [x] Sent %r" % message)
connection.close()