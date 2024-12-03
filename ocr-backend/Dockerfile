FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install flask pika pillow pytesseract
CMD ["python", "app.py"]
