# Gunakan base image Python
FROM python:3.9-slim

# Set Working Directory
WORKDIR /app

# Salin semua file ke container
COPY . .

# Instal library yang dibutuhkan
RUN pip install --no-cache-dir -r requirements.txt

# Ekspose port untuk Flask
EXPOSE 8080

# Jalankan aplikasi Flask
CMD ["python", "app.py"]
