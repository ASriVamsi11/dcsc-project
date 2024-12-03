from flask import Flask, request, jsonify
import pika
import json

app = Flask(__name__)

RABBITMQ_HOST = 'rabbitmq'  # Kubernetes service name for RabbitMQ

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file_path = f'/tmp/{file.filename}'
    file.save(file_path)

    # Send task to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue='ocr_tasks')

    message = json.dumps({'file_path': file_path})
    channel.basic_publish(exchange='', routing_key='ocr_tasks', body=message)
    connection.close()

    return jsonify({'message': 'Task added to queue'})

@app.route('/output', methods=['GET'])
def get_output():
    try:
        with open('output.txt', 'r') as f:
            text = f.read()
        return jsonify({'text': text})
    except FileNotFoundError:
        return jsonify({'text': 'No output available yet.'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
