import pika
from pytesseract import image_to_string
from PIL import Image
import json

RABBITMQ_HOST = 'rabbitmq'

def process_task(ch, method, properties, body):
    task = json.loads(body)
    file_path = task['file_path']

    # Perform OCR
    image = Image.open(file_path)
    text = image_to_string(image)
    print(f"Extracted Text: {text}")

    # Save result to a file (or database)
    with open('output.txt', 'w') as f:
        f.write(text)

    ch.basic_ack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()
channel.queue_declare(queue='ocr_tasks')
channel.basic_consume(queue='ocr_tasks', on_message_callback=process_task)

print("Waiting for tasks...")
channel.start_consuming()
