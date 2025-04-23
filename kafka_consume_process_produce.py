from confluent_kafka import Consumer, KafkaError, Producer
from llm_processing import load_model, process_message
from config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_PROMPT_TOPIC, KAFKA_GROUP_ID, KAFKA_RESPONSE_TOPIC


def start_consume_process_produce():
    # Load the LLM model and tokenizer once
    tokenizer, model = load_model()

    # Initialize Kafka producer
    producer = Producer({"bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS})

    # Create a Kafka consumer
    consumer  = Consumer({
        "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
        "group.id": KAFKA_GROUP_ID,
        "auto.offset.reset": "earliest"
    })

    consumer.subscribe([KAFKA_PROMPT_TOPIC])

    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(msg.error())
                    break

            decoded_message = msg.value().decode("utf-8")
            print(f"Received prompt message: {decoded_message}")

            # Process the message with the LLM
            llm_response = process_message(decoded_message, tokenizer, model)
            # print(f"LLM Response: {llm_response}")

            # Produce the response for the Kafka response-topic
            producer.produce(KAFKA_RESPONSE_TOPIC, value=llm_response)
            producer.flush()
    finally:
        consumer.close()
