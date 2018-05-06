import pika
import subprocess
#1 。 定义fib函数
#2. 声明接收指令的队列名rpc_queue
#3. 开始监听队列，收到消息后 调用fib函数
#4 把fib执行结果，发送回客户端指定的reply_to 队列


# 声明用户凭证
credentials = pika.PlainCredentials('tom', '123')
parameters = pika.ConnectionParameters('192.168.121.128', credentials=credentials)
connection = pika.BlockingConnection(parameters)

channel = connection.channel()  # 队列连接到通道

channel.queue_declare(queue='rpc_queue2')   # 声明队列


def run_cmd(cmd):
    """
    执行指令
    :param cmd:
    :return:
    """
    # 开启子进程执行服务器上的命令
    cmd_obj = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result = cmd_obj.stdout.read()+cmd_obj.stderr.read() # 读取命令结果
    return result


def on_request(ch, method, props, body):
    """
    接收消息后的回调函数
    :return:
    """
    cmd = body.decode('utf-8')    # 获得消费端发送回来的消息指令
    print("[.]run (%s)"%cmd)
    response = run_cmd(cmd)
    # 生产方发送数据
    ch.basic_publish(exchange='', routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=response
                     )
    ch.basic_ack(delivery_tag=method.delivery_tag)  # 通知消费方发送的队列标识



channel.basic_consume(on_request, queue='rpc_queue2')   # 接收消费方响应回来的消息

print(" [x] Awaiting RPC requests")
channel.start_consuming()   # 开始阻塞式接收


