import  pika
import sys

credentials = pika.PlainCredentials('tom', '123')
parameters = pika.ConnectionParameters(host='192.168.121.128', credentials=credentials)
connection = pika.BlockingConnection(parameters)

channel = connection.channel()    # 队列连接到通道
# 声明通道类型为广播，exchange名称为logs
channel.exchange_declare(exchange='logs', exchange_type='fanout')  # 消息转发， 类型为广播模式

message = ''.join(sys.argv[1:]) or 'info:Hellow World!' # 组装消息
channel.basic_publish(exchange='logs', routing_key='', body=message) # 发送消息

print(" [x] Sent %r" % message)
connection.close()  # 关闭连接



























