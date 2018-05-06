# 1.声明一个队列，作为reply_to返回消息结果的队列
# 2.  发消息到队列，消息里带一个唯一标识符uid，reply_to
# 3.  监听reply_to 的队列，直到有结果

import queue
import pika
import uuid

class CMDRpcClient(object):
    def __int__(self):
        # 初始化用户凭证
        credentials = pika.PlainCredentials('tom', '123')
        parameters = pika.ConnectionParameters('192.168.121.128', credentials=credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        # 指定queue名字, rabbit会随机分配一个名字, exclusive = True会在使用此queue的消费者断开后, 自动将queue删除
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue   #命令的执行结果的queue

        # 声明要监听callback_queue
        self.channel.basic_consume(self.on_response, no_ack=True, queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        """
        收到服务器端命令结果后执行这个函数
        :param ch:
        :param method:
        :param props:
        :param body:
        :return:
        """
        if self.corr_id == props.correlation_id: # 如果当前队列id等于服务端发送消息队列的id，则获取消息，完成队列唯一性标识
            self.response = body.decode('gbk')  # 把执行结果赋值给Response

    def call(self, n):
        """响应消息给服务端"""
        self.response = None
        self.corr_id = str(uuid.uuid4())   #唯一标识符号
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue2', #
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                       correlation_id=self.corr_id,
                                   ),
                                   body=str(n)
                                   )
        while self.response is None:
            self.connection.process_data_events()   #检测监听的队列里有没有新消息，如果有，收，如果没有，返回None
        return self.response      #检测有没有要发送的新指令

cmd_rpc = CMDRpcClient()
response = cmd_rpc.call('ipconfig') # 消费端发送消息
print(response)















