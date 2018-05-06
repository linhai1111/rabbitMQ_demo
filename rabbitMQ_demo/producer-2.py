import pika
credentials = pika.PlainCredentials('tom', '123')   # 用户凭证
parameters = pika.ConnectionParameters(host='192.168.121.128',credentials=credentials) # 建立连接
connection = pika.BlockingConnection(parameters)

channel = connection.channel() #队列连接通道

#声明queue
channel.queue_declare(queue='task123',durable=True) # 创建队列名为task123,durable=True表示队列持久化，不会因为rabbitmq关闭导致队列消失


channel.basic_publish(exchange='',
                      routing_key='task123', #路由
                      properties=pika.BasicProperties(
                          delivery_mode=2,  # 2表示消息持久化 make message persistent，用于接收端无法完成接收时，消息队列还能保留在通道中
                      ),
                      body='Hello World!')

print(" [x] Sent 'Hello World!'")
connection.close()
