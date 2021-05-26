import pg_channels
import pika
import os

pgc = pg_channels.connect(host=os.environ.get('POSTGRES-HOST'),
                          database=os.environ.get('POSTGRES-DB'),
                          user=os.environ.get('POSTGRES-USER'),
                          password = os.environ.get('POSTGRES-PASSWORD'))
mq = pika.BlockingConnection(pika.ConnectionParameters(host=os.environ.get('RABBITMQ-HOST') or 'localhost'))

mq_channel = mq.channel()
mq_queue_name = os.environ.get('RABBITMQ-QUEUE') or 'test'
mq_channel.queue_declare(queue=mq_queue_name)
pgc.listen(os.environ.get('POSTGRES-NOTIFY-CHANNEL'))

for event in pgc.events():
    print(" [x] Received %r" % event.payload)
    mq_channel.basic_publish(exchange='', routing_key=mq_queue_name, body=event.payload)
