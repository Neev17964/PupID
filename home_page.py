import streamlit as st

import os
import logging
import warnings

# Suppress TensorFlow logs
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

# Suppress warnings
warnings.filterwarnings("ignore")
logging.getLogger("tensorflow").setLevel(logging.ERROR)

st.set_page_config(page_title="Dog Breed Predictor", page_icon="🐕", layout="wide")

def show_home_page():
    # Enhanced glassmorphism styling with darker background and modern effects
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
            
            .stApp {
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 25%, #0f3460 60%, #1a237e 100%);
                background-attachment: fixed;
                min-height: 100vh;
            }
            
            .block-container {
                background: transparent !important;
                padding: 1rem !important;
                max-width: 1400px !important;
            }
                
            .hero-heading {
                font-family: Inter, sans-serif;
                font-size: 3.2rem;
                font-weight: 900;
                text-align: center;
                margin-top: 2rem;
                margin-bottom: 1rem;
                background: linear-gradient(135deg, #fff, #90caf9, #42a5f5, #1976d2);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                filter: drop-shadow(0 0 12px rgba(66,165,245,0.6));
                animation: glow 3s ease-in-out infinite;
            }
                
            .hero-subheading {
                font-family: Inter, sans-serif;
                font-size: 3.2rem;
                font-weight: 900;
                text-align: center;
                margin-top: 2rem;
                margin-bottom: 1rem;
                background: linear-gradient(135deg, #fff, #90caf9, #42a5f5, #1976d2);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                filter: drop-shadow(0 0 12px rgba(66,165,245,0.6));
                animation: glow 3s ease-in-out infinite;
            }
            
            /* Enhanced glassmorphism cards */
            .glass-hero {
                background: rgba(255, 255, 255, 0.08);
                backdrop-filter: blur(30px);
                border-radius: 32px;
                border: 1px solid rgba(255, 255, 255, 0.15);
                padding: 1rem 1rem;
                margin: 2rem 0;
                box-shadow: 
                    0 25px 50px rgba(0, 0, 0, 0.3),
                    inset 0 1px 0 rgba(255, 255, 255, 0.2);
                position: relative;
                overflow: hidden;
            }
            
            
            .glass-hero::after {
                content: '';
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: radial-gradient(circle, rgba(139, 69, 219, 0.1) 0%, transparent 50%);
                animation: rotate 20s linear infinite;
            }
            
            @keyframes rotate {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            .glass-card {
                background: rgba(255, 255, 255, 0.05);
                backdrop-filter: blur(25px);
                border-radius: 24px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                padding: 2.5rem 2rem;
                margin: 1.5rem 0;
                box-shadow: 
                    0 20px 40px rgba(0, 0, 0, 0.2),
                    inset 0 1px 0 rgba(255, 255, 255, 0.15);
                transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                position: relative;
            }
            
            .glass-card:hover {
                transform: translateY(-8px);
                background: rgba(255, 255, 255, 0.1);
                box-shadow: 
                    0 30px 60px rgba(0, 0, 0, 0.35),
                    inset 0 1px 0 rgba(255, 255, 255, 0.25);
            }
            
            /* Feature cards with advanced glassmorphism */
            .feature-card {
                background: rgba(255, 255, 255, 0.04);
                backdrop-filter: blur(20px);
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.08);
                padding: 2rem;
                text-align: center;
                transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                height: 350px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                position: relative;
                overflow: hidden;
            }
            
            .feature-card::before {
                content: '';
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: radial-gradient(circle, rgba(255,255,255,0.03) 0%, transparent 70%);
                opacity: 0;
                transition: opacity 0.3s ease;
            }
            
            .feature-card:hover::before {
                opacity: 1;
            }
            
            .feature-card:hover {
                transform: translateY(-12px) scale(1.02);
                background: rgba(255, 255, 255, 0.08);
                box-shadow: 
                    0 25px 50px rgba(0, 0, 0, 0.3),
                    inset 0 1px 0 rgba(255, 255, 255, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.15);
            }
            
            /* Breed showcase cards */
            .breed-showcase {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(18px);
            border-radius: 18px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 2rem;
            text-align: center;
            transition: all 0.3s ease;
            margin: 0.8rem 0;
            position: relative;
            overflow: hidden;
            height: 220px;  /* ⬅️ Increased from 160px */
            display: flex;
            flex-direction: column;
            justify-content: center;
            }
            
            .breed-showcase::after {
                content: '';
                position: absolute;
                bottom: 0;
                left: 0;
                right: 0;
                height: 3px;
                background: linear-gradient(90deg, #8b45db, #3f51b5, #2196f3, #00bcd4);
                transform: scaleX(0);
                transition: transform 0.3s ease;
            }
            
            .breed-showcase:hover::after {
                transform: scaleX(1);
            }
            
            .breed-showcase:hover {
                background: rgba(255, 255, 255, 0.1);
                transform: translateY(-8px) scale(1.03);
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.25);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            
            /* Enhanced stats cards */
            .stat-card {
                background: rgba(255, 255, 255, 0.06);
                backdrop-filter: blur(25px);
                border-radius: 22px;
                border: 1px solid rgba(255, 255, 255, 0.12);
                padding: 2.5rem 1.5rem;
                text-align: center;
                transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                position: relative;
                overflow: hidden;
                height: 270px;
                display: flex;
                flex-direction: column;
                justify-content: center;
            }
            
            .stat-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
                transition: left 0.5s ease;
            }
            
            .stat-card:hover::before {
                left: 100%;
            }
            
            .stat-card:hover {
                background: rgba(255, 255, 255, 0.12);
                transform: translateY(-10px);
                box-shadow: 
                    0 30px 60px rgba(0, 0, 0, 0.35),
                    inset 0 2px 0 rgba(255, 255, 255, 0.25);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            
            /* CTA Button styling */
            .cta-button {
                background: linear-gradient(135deg, #8b45db 0%, #3f51b5 50%, #2196f3 100%);
                border: none;
                border-radius: 18px;
                padding: 1.2rem 3.5rem;
                color: white !important;
                font-family: Inter, sans-serif;
                font-weight: 700;
                font-size: 1.1rem;
                cursor: pointer;
                transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                box-shadow: 0 10px 30px rgba(139, 69, 219, 0.4);
                text-decoration: none;
                display: inline-block;
                position: relative;
                overflow: hidden;
            }
            
            .cta-button::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
                transition: left 0.5s ease;
            }
            
            .cta-button:hover::before {
                left: 100%;
            }
            
            .cta-button:hover {
                transform: translateY(-3px) scale(1.05);
                box-shadow: 0 20px 40px rgba(139, 69, 219, 0.6);
                color: white !important;
            }
            
            /* Floating elements animation */
            @keyframes float {
                0%, 100% { transform: translateY(0px); }
                50% { transform: translateY(-12px); }
            }
            
            @keyframes glow {
                0%, 100% { text-shadow: 0 0 20px rgba(255,255,255,0.3); }
                50% { text-shadow: 0 0 30px rgba(255,255,255,0.5); }
            }
            
            .floating {
                animation: float 4s ease-in-out infinite;
            }
            
            .glowing {
                animation: glow 3s ease-in-out infinite;
            }
            
            /* Enhanced gradient text effects */
            .gradient-text {
                background: linear-gradient(135deg, #fff 0%, #e3f2fd 30%, #bbdefb 70%, #fff 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                filter: drop-shadow(0 0 10px rgba(255,255,255,0.3));
            }
            
            .accent-gradient {
                background: linear-gradient(135deg, #8b45db, #3f51b5, #2196f3, #00bcd4);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            
            .accent-gradient-stats {
                background: linear-gradient(135deg, #64b5f6, #42a5f5, #2196f3, #1976d2);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            
            /* Particle effect */
            .particles {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                pointer-events: none;
                z-index: -1;
            }
            
            .particle {
                position: absolute;
                background: rgba(255,255,255,0.1);
                border-radius: 50%;
                animation: particleFloat 15s infinite linear;
            }
            
            @keyframes particleFloat {
                0% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
                10% { opacity: 1; }
                90% { opacity: 1; }
                100% { transform: translateY(-10vh) rotate(360deg); opacity: 0; }
            }
            
            /* Responsive design */
            @media (max-width: 768px) {
                .glass-hero {
                    padding: 1.5rem 1rem;
                    text-align: center; /* center content on mobile */
                }

                .feature-card {
                    min-height: 220px;  /* flexible instead of fixed */
                    padding: 1.2rem;
                    font-size: 0.95rem;
                }

                .stat-card {
                    min-height: 150px;  /* allow auto growth if text wraps */
                    padding: 1.5rem 1rem;
                    font-size: 0.9rem;
                }

                .breed-showcase {
                    min-height: 180px; /* give enough space for images/text */
                    padding: 1rem;
                }

                /* Optional: stack cards vertically */
                .features-grid, .stats-grid {
                    grid-template-columns: 1fr; 
                    gap: 1rem; 
                }

                /* Make text/images scale nicely */
                .feature-card h3, 
                .stat-card h3 {
                    font-size: 1.1rem;
                }

                .feature-card p, 
                .stat-card p {
                    font-size: 0.85rem;
                    line-height: 1.4;
                }
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <h1 class="hero-heading">🐾 PupID 🐾</h1>
                
                
        <h2 class="hero-heading">Dog Breed Predictor</h3>
        <p class="hero-subheading">
            Upload a picture of your dog and let our AI predict its breed with unmatched accuracy and insights.
        </p>
    """, unsafe_allow_html=True)
    
    # Why Choose PupID Section
    st.markdown("""
        <div style="text-align: center; margin: 4rem 0 3rem 0;">
            <h2 style="font-family: Inter, sans-serif; font-size: 2.8rem; font-weight: 800; 
                       margin-bottom: 1.5rem;">
                <span class="gradient-text">Why Choose PupID?</span>
            </h2>
            <p style="font-family: Inter, sans-serif; font-size: 1.2rem; 
                      color: rgba(255,255,255,0.8); max-width: 650px; margin: 0 auto; line-height: 1.6;">
                Advanced AI technology meets veterinary expertise for the most accurate breed identification
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    features = [
        ("🧠", "Neural Recognition", "Advanced convolutional neural networks trained on over 2 million dog images with veterinary-grade accuracy and precision.", "#8b45db"),
        ("⚡", "Instant Analysis", "Get comprehensive breed analysis in under 2 seconds with confidence scores, personality traits, and health insights.", "#3f51b5"),
        ("🌍", "Global Database", "Recognizes 10 breeds including rare, mixed breeds, and designer dogs with detailed breed profiles and characteristics.", "#2196f3")
    ]
    
    fcols = st.columns(3, gap="large")
    for i, (emoji, title, desc, color) in enumerate(features):
        with fcols[i]:
            st.markdown(f"""
                <div class="feature-card">
                    <div class="floating" style="font-size: 4rem; margin-bottom: 1.5rem; 
                                                animation-delay: {i * 0.3}s;">{emoji}</div>
                    <h3 style="font-family: Inter, sans-serif; font-size: 1.5rem; 
                               font-weight: 700; color: white; margin-bottom: 1.2rem;">{title}</h3>
                    <p style="font-family: Inter, sans-serif; color: rgba(255,255,255,0.8); 
                              font-size: 1rem; line-height: 1.6; font-weight: 400;">{desc}</p>
                    <div style="width: 50px; height: 4px; background: {color}; 
                               border-radius: 3px; margin: 1.5rem auto 0 auto;"></div>
                </div>
            """, unsafe_allow_html=True)
    
    # Popular Breeds Showcase
    st.markdown("""
        <div style="text-align: center; margin: 4rem 0 3rem 0;">
            <h2 style="font-family: Inter, sans-serif; font-size: 2.8rem; font-weight: 800; 
                       margin-bottom: 1.5rem;">
                <span class="gradient-text">Breed Recognition Gallery</span>
            </h2>
            <p style="font-family: Inter, sans-serif; color: rgba(255,255,255,0.8); 
                      font-size: 1.2rem; margin-bottom: 3rem; line-height: 1.6;">
                From loyal companions to majestic guardians - we recognize them all
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    breeds = [
        ("🐕‍🦺", "Golden Retriever", "Friendly & Intelligent", "Perfect family companion"),
        ("🐕", "Labrador", "Active & Outgoing", "Most popular breed worldwide"),
        ("🦮", "German Shepherd", "Confident & Courageous", "Excellent working dog"),
        ("🐩", "Poodle", "Active & Proud", "Highly intelligent & trainable"),
        ("🐕", "Boxer", "Bright & Fun-Loving", "Strong working and guarding breed"),
        ("🐕", "Bulldog", "Adaptable & Playful", "Urban companion")
    ]
    
    # Create two rows of breed cards
    for row in range(2):
        bcols = st.columns(3, gap="large")
        for col in range(3):
            idx = row * 3 + col
            if idx < len(breeds):
                emoji, name, trait, desc = breeds[idx]
                with bcols[col]:
                    st.markdown(f"""
                        <div class="breed-showcase">
                            <div style="font-size: 3.2rem; margin-bottom: 0.8rem;">{emoji}</div>
                            <h4 style="font-family: Inter, sans-serif; color: white; 
                                       font-weight: 700; font-size: 1.2rem; margin-bottom: 0.5rem;">{name}</h4>
                            <div style="font-family: Inter, sans-serif; color: rgba(139, 195, 245, 0.9); 
                                       font-size: 0.9rem; font-weight: 600; margin-bottom: 0.5rem;">{trait}</div>
                            <p style="font-family: Inter, sans-serif; color: rgba(255,255,255,0.7); 
                                      font-size: 0.85rem; line-height: 1.4;">{desc}</p>
                        </div>
                    """, unsafe_allow_html=True)
    
    # Enhanced Statistics Section
    st.markdown("""
        <div style="text-align: center; margin: 4rem 0 3rem 0;">
            <h2 style="font-family: Inter, sans-serif; font-size: 2.8rem; font-weight: 800; 
                       margin-bottom: 1.5rem;">
                <span class="gradient-text">Trusted Worldwide</span>
            </h2>
            <p style="font-family: Inter, sans-serif; color: rgba(255,255,255,0.8); 
                      font-size: 1.2rem; margin-bottom: 3rem; line-height: 1.6;">
                Join thousands of dog owners who trust PupID for accurate breed identification
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    stats = [
        ("150+", "Breeds Recognized", "🎯", "Including rare & mixed breeds"),
        ("90%+", "Accuracy Rate", "🏆", "Veterinary-grade precision"),
        ("24/7", "Available", "🌟", "Instant analysis anytime"),
        ("100%", "Trust", "🤝", "Trusted by many")
    ]
    
    scols = st.columns(4, gap="large")
    for idx, (big, small, icon, desc) in enumerate(stats):
        with scols[idx]:
            st.markdown(f"""
                <div class="stat-card">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">{icon}</div>
                    <div style="font-family: Inter, sans-serif; font-size: 3rem; font-weight: 900; 
                               margin-bottom: 0.8rem;">
                        <span class="accent-gradient-stats">{big}</span>
                    </div>
                    <div style="font-family: Inter, sans-serif; font-size: 1.2rem; 
                               color: white; font-weight: 700; margin-bottom: 0.8rem;">{small}</div>
                    <p style="font-family: Inter, sans-serif; font-size: 0.9rem; 
                              color: rgba(255,255,255,0.7); font-weight: 400; line-height: 1.4;">{desc}</p>
                </div>
            """, unsafe_allow_html=True)
    
    # Enhanced Footer CTA
    st.markdown("""
        <div style="text-align: center; padding: 4rem 0 3rem 0;">
            <div class="glass-card" style="max-width: 750px; margin: 0 auto;">
                <h3 style="font-family: Inter, sans-serif; font-size: 2.5rem; font-weight: 800; 
                           color: white; margin-bottom: 1.5rem;">
                    <span class="gradient-text">Ready to Discover Your Dog's Story?</span>
                </h3>
                <p style="font-family: Inter, sans-serif; color: rgba(255,255,255,0.85); 
                          font-size: 1.2rem; margin-bottom: 2.5rem; line-height: 1.7;">
                    Navigate to the prediction page to upload your dog's photo and unlock the genetic 
                    secrets with our advanced AI technology. Get breed percentages, personality traits, 
                    and comprehensive health insights in seconds.
                </p>
                <div style="display: flex; justify-content: center; gap: 3rem; margin-bottom: 2.5rem; flex-wrap: wrap;">
                    <div style="text-align: center;">
                        <div style="font-size: 2rem; margin-bottom: 0.8rem;">📱</div>
                        <div style="font-size: 1rem; color: rgba(255,255,255,0.8); font-weight: 500;">Mobile Friendly</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 2rem; margin-bottom: 0.8rem;">🔒</div>
                        <div style="font-size: 1rem; color: rgba(255,255,255,0.8); font-weight: 500;">Privacy Protected</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 2rem; margin-bottom: 0.8rem;">⚡</div>
                        <div style="font-size: 1rem; color: rgba(255,255,255,0.8); font-weight: 500;">Instant Results</div>
                    </div>
                </div>
                <div style="font-size: 1rem; color: rgba(255,255,255,0.7); font-style: italic;">
                    🛡️ Your photos are processed securely and never stored on our servers
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

