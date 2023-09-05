FROM python:3.9.10

WORKDIR /app
COPY . /app
RUN pip install -r /app/requirements.txt --no-cache-dir
RUN pip install gunicorn==20.1.0
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "foodgram.wsgi"]