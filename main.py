import streamlit as st
import json
import pandas as pd
import pydeck as pdk
from datetime import datetime
import base64
from streamlit.components.v1 import html
import requests
from urllib.parse import quote

# ============================================
# ⚡ CONFIGURATION - MAX POWER
# ============================================
st.set_page_config(
    page_title="TUKO KADI | IEBC Registration Centers",
    page_icon="🇰🇪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS - Because we're not playing games
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #000000 0%, #2d2d2d 100%);
        padding: 2rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .main-title {
        font-size: 4rem;
        font-weight: 900;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #FFFFFF 0%, #CCCCCC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    
    .subtitle {
        color: #888;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.2em;
    }
    
    .center-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #0a0a0a 100%);
        border-radius: 1rem;
        padding: 2rem;
        margin-top: 1rem;
        border: 1px solid #333;
    }
    
    .center-name {
        font-size: 1.8rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        color: white;
    }
    
    .center-address {
        color: #aaa;
        margin-bottom: 1rem;
        font-size: 0.9rem;
    }
    
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 2rem;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-right: 0.5rem;
    }
    
    .badge-hours {
        background: #2c5f2d;
        color: white;
    }
    
    .badge-id {
        background: #d32f2f;
        color: white;
    }
    
    .badge-phone {
        background: #1976d2;
        color: white;
    }
    
    .stats-box {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
        border: 1px solid #e0e0e0;
    }
    
    .stats-number {
        font-size: 2rem;
        font-weight: 800;
        color: #1a1a1a;
    }
    
    .share-button {
        background: #25D366;
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 2rem;
        text-align: center;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.3s;
        border: none;
        width: 100%;
    }
    
    .share-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(37,211,102,0.3);
    }
    
    .copy-button {
        background: #333;
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 2rem;
        text-align: center;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.3s;
        width: 100%;
    }
    
    .footer {
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        border-top: 1px solid #e0e0e0;
        font-size: 0.7rem;
        color: #888;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# 📊 DATA LOADING - POWER MODE
# ============================================
@st.cache_data(ttl=3600)
def load_centers():
    try:
        with open('centers.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        # Fallback data if file missing
        return {
            "Nairobi": {
                "Starehe": {
                    "name": "Starehe IEBC Constituency Office",
                    "address": "Anniversary Towers, Kenyatta Avenue",
                    "coords": [-1.2864, 36.8172],
                    "phone": "020 2222152",
                    "hours": "8am-5pm",
                    "wheelchair": True
                }
            }
        }

centers = load_centers()

# ============================================
# 🎨 HEADER - KILLER DESIGN
# ============================================
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div class="main-header">
        <div class="main-title">🇰🇪 TUKO KADI</div>
        <div class="subtitle">CITIZEN LED • OPEN SOURCE • FOR KENYA</div>
    </div>
    """, unsafe_allow_html=True)

# Stats row
total_counties = len(centers)
total_constituencies = sum(len(v) for v in centers.values())

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f'<div class="stats-box"><div class="stats-number">{total_counties}</div><div>COUNTIES</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="stats-box"><div class="stats-number">{total_constituencies}</div><div>CONSTITUENCIES</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="stats-box"><div class="stats-number">100%</div><div>FREE</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="stats-box"><div class="stats-number">⚡</div><div>NO CREDIT CARD</div></div>', unsafe_allow_html=True)

# ============================================
# 🔍 SEARCH & FILTERS
# ============================================
st.markdown("---")

col_search, col_empty = st.columns([2, 1])
with col_search:
    search_term = st.text_input("🔍 SEARCH COUNTY", placeholder="Type county name...", label_visibility="collapsed")

# Filter counties
counties_list = list(centers.keys())
if search_term:
    counties_list = [c for c in counties_list if search_term.lower() in c.lower()]

# ============================================
# 🎯 MAIN SELECTION INTERFACE
# ============================================
col_left, col_right = st.columns([1, 1])

with col_left:
    county = st.selectbox(
        "🏛️ SELECT COUNTY",
        options=[""] + counties_list,
        format_func=lambda x: "Choose county..." if x == "" else x
    )
    
    if county:
        constituencies_list = list(centers[county].keys())
        constituency = st.selectbox(
            "📍 SELECT CONSTITUENCY",
            options=[""] + constituencies_list,
            format_func=lambda x: "Choose constituency..." if x == "" else x
        )

# ============================================
# 💥 DISPLAY RESULTS - EPIC MODE
# ============================================
if county and constituency:
    center = centers[county][constituency]
    
    with col_right:
        # Center Card
        st.markdown(f"""
        <div class="center-card">
            <div class="center-name">{center['name']}</div>
            <div class="center-address">📍 {center.get('address', 'Address not available')}</div>
            <div style="margin-top: 1rem;">
                <span class="badge badge-hours">🕒 {center.get('hours', '8am-5pm')}</span>
                <span class="badge badge-id">⚠️ BRING ORIGINAL ID</span>
                {f'<span class="badge badge-phone">📞 {center["phone"]}</span>' if center.get('phone') else ''}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Share buttons
        col_share1, col_share2 = st.columns(2)
        share_text = f"📍 TUKO KADI: {center['name']}\n\n📬 {center.get('address', '')}\n\n🏛️ {county} - {constituency}\n\n🕒 {center.get('hours', '8am-5pm')}\n\n⚠️ Bring your original ID!\n\nPowered by Tuko Kadi - Citizen Led 🇰🇪"
        
        with col_share1:
            whatsapp_url = f"https://wa.me/?text={quote(share_text)}"
            st.markdown(f'<a href="{whatsapp_url}" target="_blank"><div class="share-button">📢 SHARE ON WHATSAPP</div></a>', unsafe_allow_html=True)
        
        with col_share2:
            if st.button("📋 COPY DETAILS", use_container_width=True):
                st.write(f"📝 {center['name']} - Copied!")
                st.code(share_text, language="text")
    
    # ============================================
    # 🗺️ MAP - BEAST MODE ACTIVATED
    # ============================================
    if 'coords' in center and center['coords']:
        st.markdown("---")
        st.subheader("🗺️ LOCATION MAP")
        
        # Create map data
        map_data = pd.DataFrame({
            'lat': [center['coords'][0]],
            'lon': [center['coords'][1]],
            'name': [center['name']]
        })
        
        # PyDeck Map - Professional grade
        view_state = pdk.ViewState(
            latitude=center['coords'][0],
            longitude=center['coords'][1],
            zoom=15,
            pitch=0
        )
        
        layer = pdk.Layer(
            'ScatterplotLayer',
            data=map_data,
            get_position='[lon, lat]',
            get_color='[255, 68, 68, 160]',
            get_radius=200,
            pickable=True,
            auto_highlight=True
        )
        
        tooltip = {"html": "<b>{name}</b>", "style": {"color": "white"}}
        
        st.pydeck_chart(pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip=tooltip,
            map_style='mapbox://styles/mapbox/light-v10'
        ))
        
        # Google Maps link
        maps_url = f"https://www.google.com/maps/search/{quote(center['name'] + ' ' + center.get('address', ''))}"
        st.markdown(f'<div style="text-align: center; margin-top: 1rem;"><a href="{maps_url}" target="_blank" style="color: #1976d2; text-decoration: none;">🔍 Open in Google Maps →</a></div>', unsafe_allow_html=True)

# ============================================
# 📈 ANALYTICS SECTION
# ============================================
st.markdown("---")
st.markdown("### 📊 KENYA VOTER REGISTRATION 2027")
st.info("⚡ **IMPORTANT:** IEBC registration centers are open Monday-Friday, 8am-5pm. Bring your original National ID card. Registration is FREE.")

# ============================================
# 🚀 CONTRIBUTION SECTION
# ============================================
st.markdown("---")
col_contribute, col_github = st.columns([2, 1])

with col_contribute:
    st.markdown("### ✨ HELP IMPROVE TUKO KADI")
    st.markdown("Missing a center? Wrong address? **You can help!**")
    st.markdown("1. Edit `centers.json` with correct information")
    st.markdown("2. Submit a pull request on GitHub")
    st.markdown("3. Your changes go live instantly")

with col_github:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('[![GitHub](https://img.shields.io/badge/GitHub-Contribute-black?style=for-the-badge&logo=github)](https://github.com/TukoKadi/tuko-kadi-web)', unsafe_allow_html=True)

# ============================================
# 🦶 FOOTER
# ============================================
st.markdown("""
<div class="footer">
    🇰🇪 TUKO KADI - CITIZEN LED VOTER REGISTRATION LOCATOR<br>
    Data sourced from IEBC • Open Source • Privacy First • 2027 Elections<br>
    No credit card required • 100% Free • Built with ❤️ for Kenya
</div>
""", unsafe_allow_html=True)

# ============================================
# ⚡ SESSION STATE FOR ANALYTICS
# ============================================
if 'views' not in st.session_state:
    st.session_state.views = 1
else:
    st.session_state.views += 1

# Invisible counter for fun
if county and constituency:
    st.session_state.last_search = f"{county} - {constituency}"
