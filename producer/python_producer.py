from confluent_kafka import Producer
import sys
import random
import time
import uuid
import copy
import json

state = {}  # estado actual: id -> row

def random_row(row_id=None):
    return {
        "id": row_id or str(uuid.uuid4()),
        "name": random.choice(["Jose", "Caroline", "Martin", "Dave"]),
        "balance": random.randint(0, 1000)
    }

def generate_cdc_event():
    global state

    op = random.choices(
        ["c", "u", "d"],
        weights=[0.4, 0.4, 0.2],
        k=1
    )[0]

    ts = int(time.time() * 1000)

    # INSERT
    if op == "c" or not state:
        row = random_row()
        state[row["id"]] = row
        return {
            "op": "c",
            "ts_ms": ts,
            "before": None,
            "after": row
        }

    # UPDATE
    if op == "u":
        row_id = random.choice(list(state.keys()))
        before = copy.deepcopy(state[row_id])
        state[row_id]["balance"] += random.randint(-50, 50)
        after = state[row_id]
        return {
            "op": "u",
            "ts_ms": ts,
            "before": before,
            "after": after
        }

    # DELETE
    if op == "d":
        row_id = random.choice(list(state.keys()))
        before = state.pop(row_id)
        return {
            "op": "d",
            "ts_ms": ts,
            "before": before,
            "after": None
        }
    return None


def send_message(arguments):

    # Arguments
    broker = arguments[2]
    topic = arguments[1]
    conf = {
        'bootstrap.servers': broker,
        'security.protocol': 'SASL_PLAINTEXT',
        'sasl.mechanism': 'SCRAM-SHA-256',
        'sasl.username': 'myuser',
        'sasl.password': 'mypass'
    }

    producer = Producer(conf)

    print(topic)

    while True:
        event = generate_cdc_event()
        print(json.dumps(event))
        producer.produce(topic, value=json.dumps(event))
        producer.flush()

        time.sleep(1)


if __name__ == "__main__":
    send_message(sys.argv)
