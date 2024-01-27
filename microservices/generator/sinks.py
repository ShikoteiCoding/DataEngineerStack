import json

from confluent_kafka import Producer

from message import ProducerMessage
from config import Config


def acked(err, msg):
    if err is not None:
        print("failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("message delivered to topic = '{}' - partition = [{}]".format(msg.topic(), msg.partition()))


class Sink:
    def test_connection(self):
        ...

    def connect(self):
        print(f"connecting to default Sink...")

    def post(self, producer: ProducerMessage, **kwargs):
        ...


class KafkaSink(Sink):
    def __init__(self, config: Config):
        self.config = config

    def connect(self):
        conf = self.config.kafka_conf
        print(f"connecting to kafka with conf {conf}...")
        self.producer: Producer = Producer(conf)

    def post(self, producer: ProducerMessage, topic: str = "test"):
        msg = producer.generate_message()
        print(f"posting msg = {msg}")
        self.producer.produce(topic, json.dumps(msg), callback=acked)
        self.producer.poll(0)


class ConsoleSink(Sink):
    def __init__(self, config: Config):
        self.config = config

    def post(self, producer: ProducerMessage):
        print(producer.generate_message())