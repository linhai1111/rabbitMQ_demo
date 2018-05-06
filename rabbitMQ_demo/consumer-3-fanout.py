import pika

credentials = pika.PlainCredentials('tom', '123')
parameters = pika.ConnectionParameters(host='192.168.121.128', credentials=credentials)
connection = pika.BlockingConnection(parameters)

channel = connection.channel()
# 声明exchange，以防止报错
channel.exchange_declare(exchange='logs', exchange_type='fanout')
# 声明queue队列
queue_obj = channel.queue_declare(exclusive=True)#不指定queue名字,rabbit会随机分配一个名字,exclusive=True会在使用此queue的消费者断开后,自动将queue删除
queue_name = queue_obj.method.queue # 获得队列名
print('queue name',queue_name,queue_obj)

channel.queue_bind(exchange='logs', queue=queue_name)   # 队列绑定到exchange

def callback(ch, method, properties, body):
    print('[x]%r'%body)

channel.basic_consume(callback, queue=queue_name, no_ack=True)  # 接收消息

channel.start_consuming() # 阻塞状态







