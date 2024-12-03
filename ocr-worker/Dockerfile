FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install pika pillow pytesseract
CMD ["python", "worker.py"]
