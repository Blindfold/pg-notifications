import pg_channels
import pika
import os

pgc = pg_channels.connect(host='localhost', database='postgres', password="password", user="postgres")
mq = pika.BlockingConnection(pika.ConnectionParameters(os.environ.get('RABBITMQ-HOST')))

mq_channel = mq.channel()
mq_channel.queue_declare(queue='test')
pgc.listen('test')

for event in pgc.events():
    print(" [x] Received %r" % event.payload)
    mq_channel.basic_publish(exchange='', routing_key='test', body=event.payload)
    pgc.notify(event.channel + '_reply', event.payload)
