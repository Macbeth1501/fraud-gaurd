from flask import Flask, request, render_template, jsonify
import librosa
import numpy as np
import tensorflow as tf

# Initialize the Flask application
app = Flask(__name__)

# Load the trained model
model = tf.keras.models.load_model('model_4.keras')  # Replace with your model path

# Define the class names
class_names = ['Ananya', 'Benjamin_Netanyau', 'Jens_Stoltenberg', 'Julia_Gillard', 'Magaret_Tarcher', 'Nelson_Mandela', 'Rochan_Awasthi', 'Sayali_Bambal']
# Function to preprocess audio
def preprocess_audio(file_path, sr=16000, duration=1.0):
    audio, _ = librosa.load(file_path, sr=sr, duration=duration)
    audio_fft = np.fft.fft(audio)
    audio_fft = np.real(audio_fft)
    return audio_fft

# Function to predict speaker
def predict_speaker(file_path):
    audio_fft = preprocess_audio(file_path)
    audio_input = np.expand_dims(audio_fft, axis=0)
    audio_input = np.expand_dims(audio_input, axis=-1)
    prediction = model.predict(audio_input)
    predicted_class = np.argmax(prediction, axis=-1)[0]
    return class_names[predicted_class]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Check if an audio file is provided
    if 'audio_file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['audio_file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Save the file to a temporary location
        file_path = 'uploads/' + file.filename
        file.save(file_path)
        
        # Predict speaker
        predicted_speaker = predict_speaker(file_path)
        
        return jsonify({'predicted_speaker': predicted_speaker})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
