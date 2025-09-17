import streamlit as st

def show_about_us_page():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        
        .stApp {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 25%, #0f3460 60%, #1a237e 100%);
            background-attachment: fixed;
            min-height: 100vh;
            color: #fff !important;
        }
        
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown(
        """
        ### 🐶 About PupID

## Welcome to PupID – Your Dog’s Identity Made Simple! 🎯

PupID is an AI-powered dog breed classification website built with love for pets and technology. Our mission is to make identifying, understanding, and caring for your dog easier, faster, and more fun.

## 🌟 What PupID Offers

🏠 Home Page – A warm introduction to PupID and everything it brings for dog enthusiasts.

🐕 Breed Predictor – Powered by a CNN model trained on thousands of dog images, PupID achieves 90%+ accuracy and recognizes 150+ breeds. Just upload a photo of your pup, and let AI do the rest!

🛍️ PawMarket – Your one-stop shop for dog essentials. From nutritious food and grooming items to fun toys and accessories, PawMarket helps you find products that keep your pup happy and healthy.

⚙️ Behind the Technology

Built using Streamlit for an interactive and smooth user experience.

Powered by Deep Learning (CNNs) for reliable and accurate breed prediction.

Integrated with APIs to fetch additional breed details and make learning easy.

## ❤️ Why PupID?

✔️ Accurate & Reliable – 150+ breeds covered with 90%+ accuracy.

✔️ User-Friendly – Simple, clean, and intuitive interface.

✔️ More Than Just AI – Alongside breed prediction, we help you with product recommendations and breed information.

✔️ For Dog Lovers, By Dog Lovers – Designed with care for both tech and pets.

## 🚀 Our Vision

At PupID, we aim to go beyond breed prediction. In the future, we plan to add:

📊 Health & Fitness insights based on your dog’s breed.

🐾 Personalized care tips and product suggestions.

PupID is not just an app—it’s your digital partner in caring for your furry best friend. 🐾💙

---

## 👨‍💻 About the Programmer

Hi! I’m **Neev Sharma**, a Machine Learning and Deep Learning enthusiast.  
I build AI-powered projects and love combining technology with creativity.  

🔗 GitHub: [https://github.com/Neev17964](https://github.com/Neev17964)  
📸 Instagram: [https://www.instagram.com/its_neevs/](https://www.instagram.com/its_neevs/)  
💼 LinkedIn: [https://www.linkedin.com/in/neevsharma](https://www.linkedin.com/in/neevsharma)
        """
    )
