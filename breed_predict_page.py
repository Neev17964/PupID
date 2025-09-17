import streamlit as st
from PIL import Image
import numpy as np
import cv2
from keras.models import load_model
from labels import class_labels
from bread_dogs_data import breed_info
import os
import logging
import warnings
import time

# Suppress TensorFlow logs
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

# Suppress warnings
warnings.filterwarnings("ignore")
logging.getLogger("tensorflow").setLevel(logging.ERROR)

# Directory for uploaded images
SAVE_DIR = "uploaded_images"
os.makedirs(SAVE_DIR, exist_ok=True)

def save_uploaded_file(uploaded_file, max_age=300):
    """
    Save uploaded file & clean old files.
    max_age: in seconds (default: 5 min)
    """
    # Clean old files
    now = time.time()
    for fname in os.listdir(SAVE_DIR):
        fpath = os.path.join(SAVE_DIR, fname)
        if os.path.isfile(fpath):
            if now - os.path.getmtime(fpath) > max_age:
                os.remove(fpath)
    # Save new file
    file_path = os.path.join(SAVE_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

# Load your trained model
@st.cache_resource
def load_model_cached():
    return load_model("trained_model.keras", compile=False)

model = load_model_cached()

def predict_image(img_path):
    import tensorflow as tf
    img = tf.keras.preprocessing.image.load_img(img_path, target_size=(331, 331))
    img_array = tf.keras.preprocessing.image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions, axis=1)[0]
    confidence = np.max(predictions)
    return class_labels[predicted_class], confidence

def show_breed_predict_page():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
            .stApp {
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 25%, #0f3460 60%, #1a237e 100%);
                background-attachment: fixed;
                min-height: 100vh;
                color: white;
            }
            .block-container {
                background: transparent !important;
                padding: 2rem !important;
                max-width: 1400px !important;
            }
            
            /* File Uploader Styling - Comprehensive targeting */
            .stFileUploader {
                background: transparent !important;
            }
            
            /* Target all possible file uploader containers */
            .stFileUploader > div,
            .stFileUploader > div > div,
            .stFileUploader > div > div > div,
            .stFileUploader div[data-testid="stFileUploaderDropzone"],
            .stFileUploader div[data-baseweb="file-uploader"],
            section[data-testid="stFileUploader"] > div > div > div {
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 25%, #0f3460 60%, #1a237e 100%) !important;
                border: 2px dashed rgba(255,255,255,0.3) !important;
                border-radius: 20px !important;
                padding: 2rem !important;
                transition: all 0.3s ease !important;
            }
            
            /* Hover effects */
            .stFileUploader > div:hover,
            .stFileUploader > div > div:hover,
            .stFileUploader > div > div > div:hover,
            .stFileUploader div[data-testid="stFileUploaderDropzone"]:hover,
            .stFileUploader div[data-baseweb="file-uploader"]:hover,
            section[data-testid="stFileUploader"] > div > div > div:hover {
                border-color: rgba(255,255,255,0.6) !important;
                transform: translateY(-2px) !important;
                box-shadow: 0 10px 25px rgba(0,0,0,0.3) !important;
            }
            
            /* Text styling */
            .stFileUploader div[data-testid="stFileUploaderDropzoneInstructions"] > div > span,
            .stFileUploader span,
            .stFileUploader div > span,
            .stFileUploader label {
                color: white !important;
                font-family: Inter, sans-serif !important;
                font-weight: 600 !important;
            }
            
            .stFileUploader div[data-testid="stFileUploaderDropzoneInstructions"] > div > small,
            .stFileUploader small,
            .stFileUploader p {
                color: rgba(255,255,255,0.8) !important;
                font-family: Inter, sans-serif !important;
            }
            
            /* Icon styling */
            .stFileUploader svg,
            .stFileUploader div[data-testid="stFileUploaderDropzone"] svg {
                fill: rgba(255,255,255,0.6) !important;
            }
            
            /* Force override for stubborn white backgrounds */
            .stFileUploader * {
                background-color: transparent !important;
            }
            
            .stFileUploader > div > div > div[style*="background"] {
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 25%, #0f3460 60%, #1a237e 100%) !important;
            }
            
            /* Button Styling */
            .stButton > button {
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 25%, #0f3460 60%, #1a237e 100%) !important;
                border: 2px solid rgba(255,255,255,0.2) !important;
                border-radius: 16px !important;
                padding: 1rem 2.5rem !important;
                color: white !important;
                font-family: Inter, sans-serif !important;
                font-weight: 600 !important;
                font-size: 1.1rem !important;
                cursor: pointer !important;
                transition: all 0.3s ease !important;
                box-shadow: 0 8px 25px rgba(26, 26, 46, 0.4) !important;
                display: inline-block !important;
                margin: 1.5rem 0 !important;
                width: 100% !important;
                backdrop-filter: blur(10px) !important;
            }
            .stButton > button:hover {
                transform: translateY(-3px) !important;
                box-shadow: 0 15px 35px rgba(26, 26, 46, 0.6) !important;
                border-color: rgba(255,255,255,0.4) !important;
                background: linear-gradient(135deg, #2a2a4e 0%, #26315e 25%, #1f4480 60%, #2a359e 100%) !important;
            }
            .stButton > button:active {
                transform: translateY(-1px) !important;
            }
            
            @keyframes fadeInUp {
                from {opacity: 0; transform: translateY(20px);}
                to {opacity: 1; transform: translateY(0);}
            }
            .fade-in { animation: fadeInUp 1s ease forwards; }
            .fade-section { opacity: 0; animation: fadeInUp 1s ease forwards; }
            .upload-container {
                background: rgba(255,255,255,0.08);
                backdrop-filter: blur(30px);
                border-radius: 24px;
                border: 1px solid rgba(255,255,255,0.15);
                padding: 3rem 2rem;
                margin: 2rem 0;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2), inset 0 1px 0 rgba(255,255,255,0.1);
                text-align: center;
                position: relative;
                overflow: hidden;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }
            .upload-container:hover {
                transform: translateY(-5px);
                box-shadow: 0 30px 60px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.1);
            }
            .info-strip {
                width: 100%;
                margin-top: 0.5rem;
                margin-bottom: 2rem;
                background: rgba(255,255,255,0.10);
                box-shadow: 0 6px 24px rgba(0,0,0,0.14), 0 1px 2px rgba(255,255,255,0.14) inset;
                border-radius: 18px;
                display: flex;
                flex-direction: row;
                align-items: center;
                justify-content: space-around;
                padding: 1.3rem 1.5rem;
                gap: 2rem;
                backdrop-filter: blur(12px);
                font-family: Inter, sans-serif;
                animation: fadeInUp 1s ease;
            }
            .info-step {
                display: flex;
                flex-direction: column;
                align-items: center;
                min-width: 140px;
            }
            .info-icon {
                font-size: 2.2rem;
                margin-bottom: 0.3rem;
                background-clip: text;
            }
            .info-title {
                font-weight: 700;
                color: #fff;
                font-size: 1.1rem;
                margin-bottom: 0.2rem;
                letter-spacing: 0.01em;
            }
            .info-desc {
                font-weight: 400;
                color: rgba(255,255,255,0.83);
                font-size: 0.98rem;
                text-align: center;
                margin-bottom: 0;
            }
            .image-preview img {
                border-radius: 16px;
                max-width: 300px;
                border: 2px solid rgba(255, 255, 255, 0.1);
                transition: transform 0.4s ease, box-shadow 0.4s ease;
            }
            .image-preview img:hover {
                transform: scale(1.05);
                box-shadow: 0 15px 35px rgba(0,0,0,0.4);
            }
            .result-card {
                background: rgba(255,255,255,0.08);
                backdrop-filter: blur(25px);
                border-radius: 20px;
                border: 1px solid rgba(255,255,255,0.12);
                padding: 2.5rem;
                margin: 2rem 0;
                box-shadow: 0 15px 35px rgba(0, 0, 0, 0.25), inset 0 1px 0 rgba(255,255,255,0.1);
                text-align: center;
                opacity: 0;
                transform: translateY(20px);
                animation: fadeInUp 0.8s ease forwards;
            }
            .predict-button {
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 25%, #0f3460 60%, #1a237e 100%);
                border: 2px solid rgba(255,255,255,0.2);
                border-radius: 16px;
                padding: 1rem 2.5rem;
                color: white !important;
                font-family: Inter, sans-serif;
                font-weight: 600;
                font-size: 1.1rem;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 8px 25px rgba(26, 26, 46, 0.4);
                display: inline-block;
                margin: 1.5rem 0;
                backdrop-filter: blur(10px);
            }
            .predict-button:hover {
                transform: translateY(-3px);
                box-shadow: 0 15px 35px rgba(26, 26, 46, 0.6);
                border-color: rgba(255,255,255,0.4);
                background: linear-gradient(135deg, #2a2a4e 0%, #26315e 25%, #1f4480 60%, #2a359e 100%);
            }
            .animated-icon {
                display: inline-block;
                font-size: 2.5rem;
                margin-bottom: 1rem;
                animation: bounce 1.5s infinite;
            }
            @keyframes bounce {
                0%, 100% {transform: translateY(0);}
                50% {transform: translateY(-10px);}
            }
            @media (max-width: 768px) {
                .info-strip {
                    flex-direction: column;
                    gap: 0.7rem;
                }
            }
                
            
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style="text-align:center; margin:2rem 0 1.2rem 0;" class="fade-in">
            <h1 style="font-family: Inter, sans-serif; font-size: 3.2rem; font-weight: 800;">
                <span style="background: linear-gradient(135deg, #fff, #90caf9, #42a5f5, #1976d2);
                             -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                    Breed Predictor
                </span>
            </h1>
            <p style="font-family: Inter, sans-serif; font-size:1.3rem; color: rgba(255,255,255,0.8);
                     max-width:600px; margin: 0 auto; line-height:1.6;">
                Upload your dog's photo and let our AI reveal its breed with scientific precision
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="info-strip fade-in">
            <div class="info-step">
                <span class="info-icon">📷</span>
                <span class="info-title">Step 1</span>
                <span class="info-desc">Upload a clear photo of your dog</span>
            </div>
            <div class="info-step">
                <span class="info-icon">🤖</span>
                <span class="info-title">Step 2</span>
                <span class="info-desc">Let our AI analyze and recognize the breed</span>
            </div>
            <div class="info-step">
                <span class="info-icon">🎉</span>
                <span class="info-title">Step 3</span>
                <span class="info-desc">Get instant, accurate results & insights</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(" ", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    if uploaded_file:
        img = Image.open(uploaded_file)

        st.markdown("""
            <div class="image-preview fade-in" style="text-align:center;">
        """, unsafe_allow_html=True)
        st.image(img, caption="Your furry friend", width=280)
        st.markdown("</div>", unsafe_allow_html=True)

        # Predict button
        if st.button("🔮 Predict Breed"):
            file_path = save_uploaded_file(uploaded_file)
            breed, confidence = predict_image(file_path)
            st.markdown(f"""
                <div class="result-card fade-in">
                    <div class="animated-icon">🎯</div>
                    <h2 style="font-family: Inter, sans-serif; font-size: 2rem; font-weight:700;">Prediction Results</h2>
                    <p style="font-size:1.2rem; color:#4CAF50; font-weight:600;">
                        {breed}
                    </p>
                    <p style="color: rgba(255,255,255,0.8); margin-top:0.5rem; font-style: italic;">
                        {breed_info.get(breed, "No description available for this breed.")}
                    </p>
                    <p style="color: rgba(255,255,255,0.8); margin-top:0.5rem;">
                        Our AI has analyzed your dog's features and identified the breed with high accuracy.
                    </p>
                </div>

                <div class="result-card fade-in" style="margin-top:1.5rem;">
                    <div class="animated-icon">📊</div>
                    <h2 style="font-family: Inter, sans-serif; font-size: 1.8rem; font-weight:700;">
                        Confidence Score
                    </h2>
                    <p style="font-size:1.2rem; color:#2196F3; font-weight:600;">
                        {confidence*100:.2f}%
                    </p>
                    <p style="color: rgba(255,255,255,0.8); margin-top:0.5rem;">
                        This indicates how confident our AI is about the prediction.
                    </p>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("""
        <div class="upload-container fade-section" style="margin-top:3rem;">
            <h2 style="text-align:center; font-size:1.8rem; font-weight:700; margin-bottom:1.5rem;">
                How It Works
            </h2>
            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(250px,1fr)); gap:1.5rem;">
                <div style="text-align:center;" class="fade-in">
                    <div class="animated-icon">📤</div>
                    <h3>Upload Image</h3>
                    <p>Select a clear photo of your dog</p>
                </div>
                <div style="text-align:center;" class="fade-in">
                    <div class="animated-icon">🤖</div>
                    <h3>AI Analysis</h3>
                    <p>Our neural network processes the image</p>
                </div>
                <div style="text-align:center;" class="fade-in">
                    <div class="animated-icon">📊</div>
                    <h3>Get Results</h3>
                    <p>Receive breed identification with confidence score</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)