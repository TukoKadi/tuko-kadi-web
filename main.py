import streamlit as st
import json
import pandas as pd
import pydeck as pdk
import plotly.express as px
from datetime import datetime
import base64
from streamlit.components.v1 import html
import requests
from urllib.parse import quote
import io

# ============================================
# ⚡ THE ULTIMATE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="TUKO KADI PRO | Kenya Voter Intelligence",
    page_icon="🇰🇪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# 🎨 GOD-TIER CSS (Glassmorphism & Animations)
# ============================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    :root {
        --primary: #00FF87;
        --secondary: #60EFFF;
        --bg-dark: #0E1117;
        --card-bg: rgba(255, 255, 255, 0.05);
    }

    * { font-family: 'Outfit', sans-serif; }

    /* Main Container Styling */
    .stApp {
        background: radial-gradient(circle at top right, #1a2a6c, #b21f1f, #fdbb2d);
        background-attachment: fixed;
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 20px;
        transition: transform 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        border: 1px solid rgba(0, 255, 135, 0.4);
    }

    .main-title {
        font-size: 5rem;
        font-weight: 800;
        background: linear-gradient(to right, #00FF87, #60EFFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0;
        filter: drop-shadow(0 5px 15px rgba(0,0,0,0.3));
    }

    .stat-val {
        font-size: 2.5rem;
        font-weight: 800;
        color: white;
        display: block;
    }

    .stat-label {
        font-size: 0.8rem;
        color: #00FF87;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    /* Animated Badge */
    .status-badge {
        padding: 5px 15px;
        border-radius: 50px;
        font-size: 0.7rem;
        font-weight: 700;
        background: rgba(0, 255, 135, 0.2);
        color: #00FF87;
        border: 1px solid #00FF87;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }

    /* Hidden Streamlit UI Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ============================================
# 📊 SMART DATA ENGINE
# ============================================
@st.cache_data(ttl=3600)
def get_advanced_data():
    # In a real scenario, this would fetch from a live API/Database
    # Expanded mockup data for full functionality demonstration
    data = {
        "Nairobi": {
            "Starehe": {"name": "Starehe IEBC Office", "address": "Anniversary Towers", "coords": [-1.2864, 36.8172], "phone": "020 2222152", "load": "Low"},
            "Westlands": {"name": "Westlands Town Hall", "address": "Waiyaki Way", "coords": [-1.2633, 36.8028], "phone": "020 4441234", "load": "High"},
            "Kasarani": {"name": "Kasarani Sports Complex", "address": "Thika Road", "coords": [-1.2327, 36.8953], "phone": "020 8889990", "load": "Medium"}
        },
        "Mombasa": {
            "Mvita": {"name": "Mombasa City Hall", "address": "Treasury Square", "coords": [-4.0667, 39.6667], "phone": "041 2221234", "load": "Low"},
            "Nyali": {"name": "Nyali Primary", "address": "Links Road", "coords": [-4.0283, 39.7117], "phone": "041 5556667", "load": "Medium"}
        },
        "Kisumu": {
            "Kisumu Central": {"name": "Kisumu Huduma Center", "address": "Prosperity House", "coords": [-0.1022, 34.7508], "phone": "057 1112223", "load": "High"}
        }
    }
    return data

centers_data = get_advanced_data()

# Flatten data for global search and analytics
flat_list = []
for county, consts in centers_data.items():
    for const, info in consts.items():
        flat_list.append({
            "County": county,
            "Constituency": const,
            "Center": info['name'],
            "Address": info['address'],
            "Lat": info['coords'][0],
            "Lon": info['coords'][1],
            "Load": info['load']
        })
df_centers = pd.DataFrame(flat_list)

# ============================================
# 🚀 SIDEBAR NAVIGATION & TOOLS
# ============================================
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/4/49/Flag_of_Kenya.svg", width=100)
    st.markdown("## 🛠️ CONTROL PANEL")
    
    app_mode = st.radio("Navigation", ["Locator", "Analytics Dashboard", "Resources"])
    
    st.divider()
    st.markdown("### 📥 EXPORT DATA")
    if st.button("Generate CSV Report"):
        csv = df_centers.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", data=csv, file_name="iebc_centers.csv", mime="text/csv")
    
    st.markdown("---")
    st.caption("v2.0.4-PRO-BUILD")

# ============================================
# 🏠 MODE 1: THE LOCATOR (CORE ENGINE)
# ============================================
if app_mode == "Locator":
    # Header Section
    st.markdown('<h1 class="main-title">TUKO KADI PRO</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:white; opacity:0.8;">The Ultimate Kenya Voter Registration Intelligence Engine</p>', unsafe_allow_html=True)
    
    # Global Search
    search_query = st.text_input("🔍 GLOBAL SEARCH", placeholder="Search by Center Name, County, or Constituency...", help="Type anything to find it instantly.")
    
    if search_query:
        filtered_df = df_centers[df_centers.apply(lambda row: search_query.lower() in row.astype(str).str.lower().values, axis=1)]
    else:
        filtered_df = df_centers

    # Dynamic Stats
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f'<div class="glass-card"><span class="stat-label">Counties</span><span class="stat-val">{len(df_centers["County"].unique())}</span></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="glass-card"><span class="stat-label">Centers</span><span class="stat-val">{len(df_centers)}</span></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="glass-card"><span class="stat-label">Wait Time</span><span class="stat-val">~15m</span></div>', unsafe_allow_html=True)
    with c4: st.markdown(f'<div class="glass-card"><span class="stat-label">Status</span><span class="status-badge">LIVE</span></div>', unsafe_allow_html=True)

    # Main Interaction
    col_map, col_info = st.columns([2, 1])

    with col_map:
        st.markdown("### 🗺️ INTERACTIVE SPATIAL INTELLIGENCE")
        
        # Map styling and logic
        view_state = pdk.ViewState(
            latitude=filtered_df["Lat"].mean() if not filtered_df.empty else -1.2864,
            longitude=filtered_df["Lon"].mean() if not filtered_df.empty else 36.8172,
            zoom=6, pitch=45
        )
        
        layer = pdk.Layer(
            "ColumnLayer",
            data=filtered_df,
            get_position="[Lon, Lat]",
            get_elevation=1000,
            elevation_scale=100,
            radius=2000,
            get_fill_color="[0, 255, 135, 140]",
            pickable=True,
            auto_highlight=True,
        )

        st.pydeck_chart(pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            map_style="mapbox://styles/mapbox/dark-v10",
            tooltip={"html": "<b>Center:</b> {Center}<br><b>County:</b> {County}"}
        ))

    with col_info:
        st.markdown("### 📍 SELECTED TARGET")
        
        selected_county = st.selectbox("Filter County", ["All"] + list(df_centers["County"].unique()))
        
        display_data = filtered_df if selected_county == "All" else filtered_df[filtered_df["County"] == selected_county]
        
        for _, row in display_data.iterrows():
            with st.expander(f"🏢 {row['Center']}"):
                st.markdown(f"""
                **Constituency:** {row['Constituency']}  
                **Address:** {row['Address']}  
                **Traffic Level:** `{row['Load']}`  
                """)
                
                # Dynamic WhatsApp Link
                wa_msg = f"Hey! I found this IEBC center on Tuko Kadi: {row['Center']} in {row['County']}. Don't forget your ID!"
                st.markdown(f'[📢 Share on WhatsApp](https://wa.me/?text={quote(wa_msg)})')

# ============================================
# 📈 MODE 2: ANALYTICS DASHBOARD
# ============================================
elif app_mode == "Analytics Dashboard":
    st.markdown('<h1 class="main-title">DATA INSIGHTS</h1>', unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("### Centers per County")
        fig = px.bar(df_centers['County'].value_counts().reset_index(), x='County', y='count', 
                     color='count', color_continuous_scale='Viridis', template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
        
    with col_b:
        st.markdown("### Crowd Density Distribution")
        fig2 = px.pie(df_centers, names='Load', hole=0.4, 
                      color_discrete_sequence=px.colors.sequential.RdBu, template="plotly_dark")
        st.plotly_chart(fig2, use_container_width=True)

# ============================================
# 📚 MODE 3: RESOURCES
# ============================================
else:
    st.markdown('<h1 class="main-title">REQUIREMENTS</h1>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown("""
        <div class="glass-card">
            <h3>⚠️ MANDATORY CHECKLIST</h3>
            <ul style="color: white; font-size: 1.2rem;">
                <li><b>Original National ID:</b> No photocopies allowed.</li>
                <li><b>Age:</b> Must be 18 years or older.</li>
                <li><b>Presence:</b> Biometrics must be captured in person.</li>
                <li><b>Cost:</b> 100% FREE OF CHARGE.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# 🦶 FOOTER 2.0
# ============================================
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #888; padding: 20px;">
    <strong>TUKO KADI PRO</strong> | Built for the 2027 General Election Roadmap<br>
    Citizen-Led Digital Sovereignty 🇰🇪 | Last Sync: {datetime.now().strftime('%Y-%m-%d %H:%M')}
</div>
""", unsafe_allow_html=True)
