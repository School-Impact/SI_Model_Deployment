# Gunakan base image Python
FROM python:3.9.17-bookworm

# Set Working Directory
WORKDIR /app

# Salin semua file ke container
COPY . .

# Instal library yang dibutuhkan
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && apt-get clean


# Ekspose port untuk Flask
EXPOSE 8080

# Jalankan aplikasi Flask
CMD ["python", "app.py"]
