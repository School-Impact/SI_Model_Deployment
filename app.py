from flask import Flask, request, jsonify
from google.cloud import storage
import pickle
import os
import tensorflow as tf
from keras.models import load_model
import numpy as np
from dotenv import load_dotenv
from flask_cors import CORS


app = Flask(__name__)

# Google Cloud Storage Configuration
BUCKET_NAME = "si_model"
MODEL_PATH = "tfjs_model/"
LOCAL_MODEL_DIR = "/tmp/model"

# Ensure the local model directory exists
os.makedirs(LOCAL_MODEL_DIR, exist_ok=True)

def download_from_gcs(file_name, local_file_name):
   
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(MODEL_PATH + file_name)
    local_path = os.path.join(LOCAL_MODEL_DIR, local_file_name)
    blob.download_to_filename(local_path)
    return local_path

def load_model_and_encoder():
   
    # Download model.json and shards
    download_from_gcs("model.json", "model.json")
    download_from_gcs("group1-shard1of2.bin", "group1-shard1of2.bin")
    download_from_gcs("group1-shard2of2.bin", "group1-shard2of2.bin")
    
    # Load TensorFlow/Keras model
    model = tf.keras.models.load_model(LOCAL_MODEL_DIR)

    # Download and load label encoder
    label_encoder_path = download_from_gcs("label_encoder.pkl", "label_encoder.pkl")
    with open(label_encoder_path, "rb") as f:
        label_encoder = pickle.load(f)

    return model, label_encoder

# Load model and encoder during startup
model, label_encoder = load_model_and_encoder()

def preprocess_input_text(text):
 
    # Modify this function based on how you preprocess data in your Jupyter Notebook
    return text.lower().strip()

@app.route("/predict", methods=["POST"])
def predict():
    
    try:
        data = request.json
        if "interest" not in data:
            return jsonify({"error": "Missing 'interest' in request body"}), 400
        
        input_text = data["interest"]
        preprocessed_text = preprocess_input_text(input_text)

        # Transform input into TF-IDF vector (assuming TF-IDF was used)
        tfidf = tf.keras.layers.TextVectorization(output_mode="tf-idf")  # Update if needed
        input_vector = tfidf([preprocessed_text]).numpy()

        # Predict with the model
        predicted_class = model.predict(input_vector)
        predicted_label = label_encoder.inverse_transform([np.argmax(predicted_class)])[0]

        return jsonify({
            "input": input_text,
            "predicted_label": predicted_label
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
