from pykafka import KafkaClient
#from kafka import KafkaConsumer, KafkaProducer

client = KafkaClient(hosts='localhost:9092')
print(str(client.topics))

def consume():
    topic = client.topics[b'test']
    consumer = topic.get_simple_consumer()
    for message in consumer:
        if message is not None:
           print(message)
    #consumer = KafkaConsumer('test',
    #    bootstrap_servers=['localhost:9092'],
    #    api_version=(0,10,1))
    #    #api_version=(0,8,0),
    #    #key_deserializer=lambda m: m.decode('utf-8'),
    #    #value_deserializer=lambda m: json.loads(m.decode('utf-8')))
    #for message in consumer.poll():
    #    print(str(message))

def produce():
    topic = client.topics[b'test']
    with topic.get_sync_producer() as producer:
      for i in range(4):
        producer.produce(b'test message')
    #producer = KafkaProducer(bootstrap_servers=['localhost:9092'],api_version=(0,10,1))
    #future = producer.send('test', key=b'key', value=message)
    #future.get(timeout=5)
