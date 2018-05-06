import pika
credentials = pika.PlainCredentials('tom', '123')   # 用户凭证
parameters = pika.ConnectionParameters(host='192.168.121.128',credentials=credentials) # 建立连接
connection = pika.BlockingConnection(parameters)

channel = connection.channel() #队列连接通道

#声明queue
channel.queue_declare(queue='task123',durable=True) # 创建队列名为task123


channel.basic_publish(exchange='',  # 生产端发送消息
                      routing_key='task123', # 路由，数据发送到task123队列
                      body='Hello World!' )# 发送的内容

print(" [x] Sent 'Hello World!'")
connection.close()
