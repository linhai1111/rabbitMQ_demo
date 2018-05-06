import  pika
import time
credentials = pika.PlainCredentials('tom', '123') # 凭证
paramenters = pika.ConnectionParameters('192.168.121.128', credentials = credentials)
connection = pika.BlockingConnection(paramenters)

channel = connection.channel() # 队列连接到通道

def callback(ch, method, properties, body): # 回调函数
    # time.sleep(5)  # 用于模拟接收端未完成消息接收的状况
    print(" [x] Received %r" % body)
    ch.basic_ack(delivery_tag=method.delivery_tag)  # 手动确认，向发送方发送已接收消息，让发送方将消息丢弃，与 no_ack=True形成对应关系

channel.basic_consume(callback, # 消费端取到消息后，调用callback 函数
                      queue='task123',)
                      #no_ack=True ) # no_ack=True表示消息处理后，不向rabbit-server确认消息已消费完毕

channel.basic_qos(prefetch_count=1) # 公平分发
channel.start_consuming()   # 阻塞模式





