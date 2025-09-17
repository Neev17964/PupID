import streamlit as st
from urllib.parse import quote
from products_data import products
import base64, os

import os
import logging
import warnings

# Suppress TensorFlow logs
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

# Suppress warnings
warnings.filterwarnings("ignore")
logging.getLogger("tensorflow").setLevel(logging.ERROR)

def show_Dog_products_page():
    st.set_page_config(
        page_title="PupID - Dog Breed Classifier",
        page_icon="🐶",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    # ---------- SIDEBAR: Search and Filters ----------
    st.sidebar.title("Search & Filter 🛒")
    
    # Flatten all products for rating range
    all_products = [prod for prods in products.values() for prod in prods]

    # Extract numeric ratings safely
    ratings = []
    for p in all_products:
        try:
            ratings.append(int(float(p.get('rating', 0))))
        except (TypeError, ValueError):
            ratings.append(0)

    min_rating, max_rating = min(1, min(ratings)), max(5, max(ratings))

    search_query = st.sidebar.text_input("🔍 Search products")

    # --- Rating Filter (integer step) ---
    rating_range = st.sidebar.slider(
        "⭐️ Rating range",
        min_value=int(min_rating), max_value=int(max_rating),
        value=(int(min_rating), int(max_rating)),
        step=1
    )

    # ---- Sort Option ----
    sort_option = st.sidebar.radio(
        "📊 Sort products",
        ("None", "Price: Low → High", "Price: High → Low", "Rating: High → Low"),
        index=0
    )

    # ---------- CUSTOM CSS ----------
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        .stApp {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 25%, #0f3460 60%, #1a237e 100%);
            color: #e2e8f0;
        }
        section[data-testid="stSidebar"] {
            background: linear-gradient(135deg, #16213e 0%, #1a237e 100%) !important;
        }
        /* Make all sidebar text white */
        section[data-testid="stSidebar"] * {
            color: #fff !important;
        }
        .hero-container {
            background: rgba(30, 41, 59, 0.45);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(148, 163, 184, 0.25);
            border-radius: 28px;
            padding: 70px 40px;
            text-align: center;
            margin: 30px 0 50px 0;
            box-shadow: 0 25px 60px rgba(0, 0, 0, 0.3);
            animation: fadeIn 1.2s ease-out;
        }
        .hero-title {
            font-size: 3.8rem;
            font-weight: 700;
            background: linear-gradient(135deg, #60a5fa, #8b5cf6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 20px;
            text-shadow: 0 4px 20px rgba(0,0,0,0.35);
        }
        .hero-subtitle {
            font-size: 1.3rem;
            font-weight: 500;
            color: #cbd5e1;
            margin-bottom: 15px;
            line-height: 1.7;
        }
        .hero-description {
            font-size: 1.15rem;
            font-weight: 400;
            color: #94a3b8;
            margin: 0 auto 35px auto;
            max-width: 700px;
            line-height: 1.6;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .stats-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 30px;
            margin-top: 40px;
        }
        .stat-item {
            text-align: center;
            animation: slideUp 0.8s ease-out;
        }
        @keyframes slideUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .stat-number {
            font-size: 2.5rem;
            font-weight: 700;
            color: #60a5fa;
            margin-bottom: 5px;
        }
        .stat-label {
            font-size: 0.9rem;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .search-section {
            background: rgba(30, 41, 59, 0.4);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(148, 163, 184, 0.2);
            border-radius: 20px;
            padding: 30px;
            text-align: center;
            margin: 40px 0;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
        }
        .search-text {
            font-size: 1.3rem;
            color: #cbd5e1;
            margin: 0;
        }
        .category-title {
            font-size: 2rem;
            color: #e2e8f0;
            text-align: center;
            margin: 40px 0;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
        }
        .product-card {
            background: rgba(30, 41, 59, 0.4);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(148, 163, 184, 0.2);
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            margin-bottom: 25px;
            position: relative;
            overflow: hidden;
            animation: cardAppear 0.6s ease-out;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        @keyframes cardAppear {
            from { opacity: 0; transform: translateY(40px) scale(0.95); }
            to { opacity: 1; transform: translateY(0) scale(1); }
        }
        .product-card:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.35);
            border-color: rgba(96, 165, 250, 0.4);
            background: rgba(30, 41, 59, 0.6);
        }
        .product-image {
            width: 100%;
            max-width: 220px;
            height: 220px;
            object-fit: cover;
            border-radius: 15px;
            margin-bottom: 20px;
            transition: transform 0.4s ease;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
        }
        .product-card:hover .product-image {
            transform: scale(1.05);
        }
        .product-title {
            font-size: 1.4rem;
            font-weight: 600;
            color: #e2e8f0;
            margin-bottom: 12px;
            text-align: center;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        }
        .product-description {
            color: #94a3b8;
            line-height: 1.6;
            margin-bottom: 25px;
            font-size: 0.95rem;
            text-align: center;
        }
        .buy-button {
            background: linear-gradient(135deg, #3b82f6, #1d4ed8) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 14px 20px !important;
            font-size: 1rem !important;
            font-weight: 600 !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4) !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
            width: 100% !important;
            text-decoration: none !important;
            display: inline-block !important;
            text-align: center !important;
            margin-bottom: 6px !important;
        }
        .buy-button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 12px 30px rgba(59, 130, 246, 0.6) !important;
            background: linear-gradient(135deg, #1d4ed8, #3b82f6) !important;
            color: white !important;
            text-decoration: none !important;
        }
        .stButton > button {
            background: linear-gradient(135deg, #3b82f6, #1d4ed8) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 14px 20px !important;
            font-size: 1rem !important;
            font-weight: 600 !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4) !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
            width: 100% !important;
            height: 50px !important;
        }
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 12px 30px rgba(59, 130, 246, 0.6) !important;
            background: linear-gradient(135deg, #1d4ed8, #3b82f6) !important;
            color: white !important;
        }
        @media (max-width: 768px) {
            .hero-title { font-size: 2.5rem; }
            .stats-container { grid-template-columns: repeat(2, 1fr); gap: 20px; }
            .hero-container { padding: 40px 20px; }
            .category-title { font-size: 1.5rem; }
            .product-image { max-width: 100%; height: 160px; }
            .product-card { padding: 16px; }
        }
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: rgba(30, 41, 59, 0.3);
        }
        ::-webkit-scrollbar-thumb {
            background: rgba(96, 165, 250, 0.5);
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(96, 165, 250, 0.7);
        }
    </style>
    """, unsafe_allow_html=True)

    # ---------- HERO SECTION ----------
    st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">PawMarket</h1>
        <p class="hero-subtitle">Premium products for your beloved furry friends. Curated with love, delivered with care.</p>
        <p class="hero-subtitle">Transform your dog's life with our handpicked essentials.</p>
        <div class="stats-container">
            <div class="stat-item"><div class="stat-number">30+</div><div class="stat-label">PRODUCTS</div></div>
            <div class="stat-item"><div class="stat-number">4.7★</div><div class="stat-label">AVG RATING</div></div>
            <div class="stat-item"><div class="stat-number">10K+</div><div class="stat-label">HAPPY DOGS</div></div>
            <div class="stat-item"><div class="stat-number">24/7</div><div class="stat-label">SUPPORT</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ---------- SEARCH SECTION ----------
    st.markdown("""
    <div class="search-section">
        <p class="search-text">Here's a tail-wagging selection curated just for your dog – pick something special!</p>
    </div>
    """, unsafe_allow_html=True)

    # ---------- PRODUCT CARD FUNCTION ----------
    def create_product_card(product):
        # Removed "new" badge completely
        product_image = ''
        try:
            if product.get("image", ""):
                image_path = os.path.join("Images", product["image"])
                with open(image_path, "rb") as f:
                    img_base64 = base64.b64encode(f.read()).decode("utf-8")
                product_image = f'<img src="data:image/png;base64,{img_base64}" class="product-image" alt="{product["name"]}" style="max-width:140px; height:140px;">'
        except Exception:
            product_image = '<div style="color:#fa5;margin-bottom:8px;">Image not found</div>'
        
        amazon_url = product.get("amazon_url") or f"https://amazon.com/s?k={quote(product.get('search_query', product.get('name', 'dog product')))}"
        price = product.get('price', "N/A")
        rating = product.get('rating', "N/A")

        card_html = f"""
        <div class="product-card">
            {product_image}
            <h3 class="product-title">{product['name']}</h3>
            <p class="product-description">{product['description']}</p>
            <p style="color:#60a5fa;font-weight:600;margin-bottom:8px;">💰 Price: ₹{price}</p>
            <p style="color:#facc15;font-weight:500;margin-bottom:20px;">⭐ Rating: {rating}/5</p>
            <a href="{amazon_url}" target="_blank" class="buy-button">🛒 Buy Now</a>
        </div>
        """
        return card_html

    # ---------- DISPLAY FILTERED PRODUCTS ----------
    for category, product_list in products.items():
        filtered_products = []
        for p in product_list:
            pname = p.get('name', '').lower()
            pdesc = p.get('description', '').lower()

            try:
                prating = int(float(p.get('rating', min_rating)))
            except (TypeError, ValueError):
                prating = min_rating

            matches_search = (search_query.lower() in pname or search_query.lower() in pdesc) if search_query else True
            matches_rating = rating_range[0] <= prating <= rating_range[1]

            if matches_search and matches_rating:
                filtered_products.append(p)

        # ---- Apply Sorting ----
        if sort_option == "Price: Low → High":
            filtered_products.sort(key=lambda x: float(x.get("price", 0)) if str(x.get("price", "")).replace(".", "", 1).isdigit() else 0)
        elif sort_option == "Price: High → Low":
            filtered_products.sort(key=lambda x: float(x.get("price", 0)) if str(x.get("price", "")).replace(".", "", 1).isdigit() else 0, reverse=True)
        elif sort_option == "Rating: High → Low":
            filtered_products.sort(key=lambda x: float(x.get("rating", 0)) if str(x.get("rating", "")).replace(".", "", 1).isdigit() else 0, reverse=True)

        if filtered_products:
            st.markdown(f'<h2 class="category-title">{category}</h2>', unsafe_allow_html=True)
            cols = st.columns(3)
            for idx, product in enumerate(filtered_products):
                with cols[idx % 3]:
                    st.markdown(create_product_card(product), unsafe_allow_html=True)

    # ---------- FOOTER ----------
    st.markdown("""
    <div style="text-align:center; margin-top:60px; padding:40px; 
                background: rgba(30, 41, 59, 0.4); backdrop-filter: blur(20px);
                border: 1px solid rgba(148, 163, 184, 0.2); border-radius: 20px;">
        <h3 style="color:#e2e8f0; margin-bottom:20px;">🐕 Thank you for choosing PawMarket!</h3>
        <p style="color:#94a3b8; font-size:1.1rem;">Your furry friend deserves the best. We're here to help you provide it.</p>
    </div>
    """, unsafe_allow_html=True)
