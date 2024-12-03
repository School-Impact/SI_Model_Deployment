import os
from flask import Flask, request, jsonify
import tensorflow as tf
import pandas as pd
from keras.models import load_model
import json
import numpy as np
import joblib  # Untuk memuat TF-IDF Vectorizer
os.environ["TF_USE_LEGACY_KERAS"] = "1"

app = Flask(__name__)

# Memuat model TensorFlow (H5 file)
model = load_model('school_impact.h5')

# Memuat TF-IDF Vectorizer yang sudah dilatih dan disimpan
tfidf_vectorizer = joblib.load('tfidf_vectorizer.pkl')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Ambil data input dari request
        data = request.get_json()
        text = data.get('text')
        if not text:
            return jsonify({"error": "Text input required"}), 400

        # Preprocess text (sesuaikan dengan preprocessing yang digunakan untuk pelatihan model)
        preprocessed_text = preprocess_input_text(text)
        
        # Transformasi teks menjadi vektor TF-IDF (menggunakan TF-IDF Vectorizer yang sudah dilatih)
        tfidf_vector = tfidf_vectorizer.transform([preprocessed_text]).toarray()

        # Melakukan prediksi
        predictions = model.predict(tfidf_vector)

        # Mendapatkan label dari prediksi
        predicted_class = np.argmax(predictions, axis=1)[0]

        # Daftar label sesuai model
        # labels = ["SMK Teknologi dan Rekayasa", "SMK Seni dan Industri Kreatif", "SMK Energi dan Pertambangan", "SMK Teknologi Informasi dan Komunikasi", "SMK Kesehatan dan Pekerjaan Sosial", "SMK Bisnis dan Manajemen", "SMK Pariwisata", "SMA IPA", "SMA IPS", "SMK Kemaritiman","SMK Agribisnis dan Agroteknologi"]

        labels = ["SMA IPA", "SMA IPS", "SMK Agribisnis dan Agroteknologi", "SMK Bisnis dan Manajemen", "SMK Energi dan Pertambangan", "SMK Kemaritiman", "SMK Kesehatan dan Pekerjaan Sosial", "SMK Pariwisata", "SMK Seni dan Industri Kreatif", "SMK Teknologi Informasi dan Komunikasi", "SMK Teknologi dan Rekayasa"]
        predicted_label = labels[predicted_class]

        return jsonify({"text": text, "predicted_label": predicted_label})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def preprocess_input_text(text):
    # Implementasikan preprocessing teks yang digunakan pada model
    # (misalnya lowercase, tokenisasi, stopwords removal, dll)
    return text.lower()

if __name__ == '__main__':
    app.run(debug=True)
