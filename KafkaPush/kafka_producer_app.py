from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from confluent_kafka import Producer
import json

app = FastAPI()

# Kafka producer configuration
producer_conf = {
    'bootstrap.servers': 'localhost:9092'
}
producer = Producer(producer_conf)

# Callback function
def delivery_report(err, msg):
    if err is not None:
        print(f" Delivery failed for record {msg.key()}: {err}")
    else:
        print(f" Record {msg.key()} successfully produced to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

# Common Kafka producer logic
async def produce_to_topic(request: Request, topic: str):
    print(f" Kafka producer route for topic `{topic}` is active")
    try:
        data = await request.json()
        key = data.get("transactionId", "default-key")
        producer.produce(
            topic=topic,
            key=key,
            value=json.dumps(data),
            callback=delivery_report
        )
        producer.flush()
        return {"message": f"Message produced successfully on topic: {topic}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint for A1_FeatureEvents
@app.post("/produce/a1-feature-events")
async def produce_a1_feature_events(request: Request):
    return await produce_to_topic(request, "FeatureEvents")

# Endpoint for ActivationEvents
@app.post("/produce/activation-events")
async def produce_activation_events(request: Request):
    return await produce_to_topic(request, "ActivationEvents")

# Endpoint for aq_test1
@app.post("/produce/cdr")
async def produce_aq_test1(request: Request):
    print("Incoming request to /produce/cdr")
    return await produce_to_topic(request, "aq_test1")