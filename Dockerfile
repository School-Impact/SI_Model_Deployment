FROM python:3.10-slim

ENV PYTHONBUFFERED True

ENV APP_HOME /app

WORKDIR $APP_HOME

COPY . ./  

RUN pip install -r requirements.txt

# Membuka port 8080
EXPOSE 8080

# Menjalankan aplikasi Flask pada port 8080
CMD ["python", "app.py"]
