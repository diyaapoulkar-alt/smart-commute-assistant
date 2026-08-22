"""
===================================================================
🚗 SMART COMMUTE ASSISTANT — Cuberto-Inspired Elite Commute Dashboard
===================================================================
Author: Diyaa Poulkar
Repository: https://github.com/diyaapoulkar-alt/smart-commute-assistant
Description: Real-road OSRM routing, multi-modal transport comparison,
             peak-hour traffic estimation, eco CO2 calculator, and
             turn-by-turn navigation engine.
"""

import os
import re
import json
import math
import time
from datetime import datetime, timedelta
import requests
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OPENCAGE_KEY = os.getenv("OPENCAGE_KEY", "ff5da74a3813406eb539b7df97a9d72f")
OPENWEATHER_KEY = os.getenv("OPENWEATHER_KEY", "7beb61cdd2ceae85227c9d7135e6867d")

# Page Configuration
st.set_page_config(
    page_title="Smart Commute Assistant — Elite Routing Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Cuberto-Inspired Luxury Beige Design System CSS
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Outfit', 'Plus Jakarta Sans', sans-serif;
        background-color: #F7F4EF !important;
        color: #1C1917;
    }

    .stApp {
        background-color: #F7F4EF !important;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Cuberto Header Hero Card */
    .cuberto-hero {
        background: #EFECE6;
        border: 1px solid rgba(28, 25, 23, 0.08);
        border-radius: 2rem;
        padding: 2.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px -15px rgba(28, 25, 23, 0.05);
    }

    .cuberto-title {
        font-size: 2.75rem;
        font-weight: 900;
        letter-spacing: -0.04em;
        color: #1C1917;
        margin: 0;
        line-height: 1.1;
    }

    .cuberto-subtitle {
        font-size: 1.1rem;
        font-weight: 500;
        color: #57534E;
        margin-top: 0.5rem;
        letter-spacing: -0.01em;
    }

    /* Cuberto Pill Badge */
    .cuberto-badge {
        background-color: #E7E2D7;
        color: #292524;
        border: 1px solid rgba(28, 25, 23, 0.1);
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        padding: 0.35rem 0.85rem;
        border-radius: 9999px;
        display: inline-block;
        margin-bottom: 0.75rem;
    }

    /* Cards */
    .cuberto-card {
        background: #FFFFFF;
        border: 1px solid rgba(28, 25, 23, 0.08);
        border-radius: 1.75rem;
        padding: 1.75rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 10px 30px -10px rgba(28, 25, 23, 0.04);
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .cuberto-card:hover {
        border-color: rgba(28, 25, 23, 0.2);
        box-shadow: 0 15px 35px -10px rgba(28, 25, 23, 0.08);
        transform: translateY(-2px);
    }

    /* Custom Metric Styling */
    .metric-value {
        font-size: 2rem;
        font-weight: 900;
        color: #1C1917;
        letter-spacing: -0.03em;
    }

    .metric-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: #78716C;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Buttons */
    .stButton>button {
        background-color: #1C1917 !important;
        color: #F7F4EF !important;
        border-radius: 9999px !important;
        height: 3.25rem !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.01em !important;
        border: none !important;
        box-shadow: 0 10px 20px -5px rgba(28, 25, 23, 0.2) !important;
        transition: all 0.3s ease !important;
    }

    .stButton>button:hover {
        background-color: #292524 !important;
        transform: scale(1.02) !important;
    }

    /* Direction Step Card */
    .direction-step {
        background-color: #FDFBF7;
        border-left: 3px solid #1C1917;
        padding: 0.75rem 1rem;
        margin-top: 0.5rem;
        border-radius: 0 0.75rem 0.75rem 0;
        font-size: 0.95rem;
        color: #292524;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Helper Functions
def get_coordinates(place: str):
    """Geocode place name to (lat, lon) using OpenCage, fallback to Nominatim."""
    # 1. Try OpenCage if key available
    if OPENCAGE_KEY:
        try:
            url = f"https://api.opencagedata.com/geocode/v1/json?q={urllib.parse.quote(place)}&key={OPENCAGE_KEY}"
            res = requests.get(url, timeout=5).json()
            if res.get("results"):
                lat = res["results"][0]["geometry"]["lat"]
                lon = res["results"][0]["geometry"]["lng"]
                formatted = res["results"][0].get("formatted", place)
                return lat, lon, formatted
        except Exception:
            pass

    # 2. Fallback to OpenStreetMap Nominatim (Free)
    try:
        headers = {"User-Agent": "SmartCommuteAssistant/2.0"}
        url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(place)}&format=json&limit=1"
        res = requests.get(url, headers=headers, timeout=5).json()
        if res:
            return float(res[0]["lat"]), float(res[0]["lon"]), res[0].get("display_name", place)
    except Exception:
        pass

    return None, None, place


def get_weather(lat: float, lon: float):
    """Fetch weather at (lat, lon) using OpenWeatherMap, fallback to Open-Meteo."""
    # 1. Try OpenWeatherMap
    if OPENWEATHER_KEY:
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_KEY}&units=metric"
            res = requests.get(url, timeout=5).json()
            if "weather" in res:
                return res["weather"][0]["main"], res["main"]["temp"], res["weather"][0].get("icon", "")
        except Exception:
            pass

    # 2. Fallback to Open-Meteo (Free)
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        res = requests.get(url, timeout=5).json()
        if "current_weather" in res:
            weather_code = res["current_weather"].get("weathercode", 0)
            temp = res["current_weather"].get("temperature", 20.0)
            # Weather code mapping
            weather_desc = "Clear" if weather_code == 0 else ("Rainy" if weather_code > 50 else "Cloudy")
            return weather_desc, temp, ""
    except Exception:
        pass

    return "Fair", 22.0, ""


def get_osrm_route(start_coords, end_coords, mode="driving"):
    """Query OSRM for real road geometries, turn-by-turn steps, distance, and duration."""
    mode_map = {
        "driving": "driving",
        "bike": "bike",
        "foot": "foot"
    }
    osrm_profile = mode_map.get(mode, "driving")
    
    lat1, lon1 = start_coords
    lat2, lon2 = end_coords

    url = f"http://router.project-osrm.org/route/v1/{osrm_profile}/{lon1},{lat1};{lon2},{lat2}?overview=full&geometries=geojson&steps=true"
    try:
        res = requests.get(url, timeout=6).json()
        if res.get("code") == "Ok" and res.get("routes"):
            route = res["routes"][0]
            distance_km = route["distance"] / 1000.0
            duration_min = route["duration"] / 60.0
            geometry = route["geometry"]["coordinates"]  # [[lon, lat], ...]
            # Convert geometry to [[lat, lon], ...] for Folium
            poly_latlon = [[pt[1], pt[0]] for pt in geometry]
            
            # Extract turn steps
            steps = []
            if "legs" in route and route["legs"]:
                for leg in route["legs"]:
                    for step in leg.get("steps", []):
                        maneuver = step.get("maneuver", {}).get("type", "turn")
                        name = step.get("name", "road")
                        dist = step.get("distance", 0)
                        if dist > 30:
                            steps.append(f"{maneuver.capitalize()} onto {name if name else 'connecting road'} ({int(dist)}m)")
            return distance_km, duration_min, poly_latlon, steps
    except Exception:
        pass

    # Straight-line Fallback if OSRM is unreachable
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance_km = R * c
    duration_min = (distance_km / 50.0) * 60.0
    poly_latlon = [[lat1, lon1], [lat2, lon2]]
    return distance_km, duration_min, poly_latlon, ["Head straight towards destination."]


def calculate_traffic_and_rush(duration_min: float):
    """Calculate peak-hour rush factor based on current time of day."""
    current_hour = datetime.now().hour
    is_morning_rush = 8 <= current_hour <= 10
    is_evening_rush = 17 <= current_hour <= 20

    if is_morning_rush or is_evening_rush:
        traffic_level = "Heavy Rush Hour"
        delay_factor = 1.35
        color = "#DC2626"  # Red
        badge_bg = "background-color: #FEE2E2; color: #991B1B;"
    elif 11 <= current_hour <= 16:
        traffic_level = "Moderate Traffic"
        delay_factor = 1.15
        color = "#D97706"  # Amber
        badge_bg = "background-color: #FEF3C7; color: #92400E;"
    else:
        traffic_level = "Smooth Flow"
        delay_factor = 1.0
        color = "#16A34A"  # Green
        badge_bg = "background-color: #DCFCE7; color: #166534;"

    adjusted_duration = duration_min * delay_factor
    return traffic_level, adjusted_duration, color, badge_bg, delay_factor


def calculate_eco_impact(distance_km: float, mode: str):
    """Calculate CO2 emissions in kg and fuel cost estimates."""
    rates = {
        "Car 🚗": {"co2_per_km": 0.192, "cost_per_km": 7.5},      # 192g CO2/km
        "Motorcycle 🏍️": {"co2_per_km": 0.090, "cost_per_km": 3.0}, # 90g CO2/km
        "Transit 🚌": {"co2_per_km": 0.050, "cost_per_km": 1.5},    # 50g CO2/km
        "Bicycle 🚴": {"co2_per_km": 0.0, "cost_per_km": 0.0},
        "Walking 🚶": {"co2_per_km": 0.0, "cost_per_km": 0.0},
    }
    cfg = rates.get(mode, rates["Car 🚗"])
    co2_kg = distance_km * cfg["co2_per_km"]
    cost_inr = distance_km * cfg["cost_per_km"]
    return co2_kg, cost_inr


# ===================================================================
# HEADER HERO SECTION (CUBERTO MINIMALIST STYLE)
# ===================================================================

st.markdown(
    """
    <div class="cuberto-hero">
        <span class="cuberto-badge">Intelligent Mobility Engine</span>
        <h1 class="cuberto-title">Smart Commute Assistant</h1>
        <p class="cuberto-subtitle">
            Real-road OSRM Navigation • Multi-Modal Transit Comparison • Peak Traffic & Eco CO₂ Analytics
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ===================================================================
# SIDEBAR INPUT CONTROLS
# ===================================================================

st.sidebar.markdown("### 📍 Route Selection")
start_loc = st.sidebar.text_input("Current Location", value="Nashik", help="e.g. Nashik, Mumbai, Pune, Delhi")
end_loc = st.sidebar.text_input("Destination", value="Mumbai", help="e.g. Bandra, CST, Airport, Pune")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🚗 Transport Mode")
transport_mode = st.sidebar.selectbox(
    "Choose Mode",
    ["Car 🚗", "Motorcycle 🏍️", "Transit 🚌", "Bicycle 🚴", "Walking 🚶"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown("### ⏰ Target Arrival Time")
target_time_input = st.sidebar.text_input("Target Arrival (HH:MM)", value="09:30", help="24-hour format e.g. 09:30 or 18:45")

calc_button = st.sidebar.button("🚀 Calculate Smart Route")

# Session State Storage
if "trip_data" not in st.session_state:
    st.session_state.trip_data = None

if calc_button or st.session_state.trip_data is None:
    with st.spinner("Calculating real-road OSRM navigation route & weather..."):
        s_lat, s_lon, s_fmt = get_coordinates(start_loc)
        e_lat, e_lon, e_fmt = get_coordinates(end_loc)

        if not s_lat or not e_lat:
            st.error("❌ Could not resolve coordinates for one of the locations. Please check city names.")
        else:
            mode_code = "driving"
            if "Bicycle" in transport_mode:
                mode_code = "bike"
            elif "Walking" in transport_mode:
                mode_code = "foot"

            dist_km, dur_min, polyline, turn_steps = get_osrm_route((s_lat, s_lon), (e_lat, e_lon), mode=mode_code)
            w1_desc, w1_temp, _ = get_weather(s_lat, s_lon)
            w2_desc, w2_temp, _ = get_weather(e_lat, e_lon)

            traffic_lbl, adj_dur_min, traffic_color, traffic_bg, delay_fact = calculate_traffic_and_rush(dur_min)
            co2_kg, cost_est = calculate_eco_impact(dist_km, transport_mode)

            st.session_state.trip_data = {
                "start": start_loc,
                "end": end_loc,
                "start_fmt": s_fmt,
                "end_fmt": e_fmt,
                "start_coords": [s_lat, s_lon],
                "end_coords": [e_lat, e_lon],
                "distance_km": dist_km,
                "duration_min": dur_min,
                "adj_duration_min": adj_dur_min,
                "traffic_label": traffic_lbl,
                "traffic_color": traffic_color,
                "traffic_bg": traffic_bg,
                "delay_factor": delay_fact,
                "weather_start": f"{w1_desc} ({w1_temp:.1f}°C)",
                "weather_end": f"{w2_desc} ({w2_temp:.1f}°C)",
                "polyline": polyline,
                "turn_steps": turn_steps,
                "co2_kg": co2_kg,
                "cost_est": cost_est,
                "mode": transport_mode,
            }

# ===================================================================
# MAIN DISPLAY & TABS
# ===================================================================

trip = st.session_state.trip_data

if trip:
    # TOP TRIP METRICS ROW
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f'<div class="metric-label">Road Distance</div><div class="metric-value">{trip["distance_km"]:.1f} km</div>', unsafe_allow_html=True)
    with m2:
        hours = trip["adj_duration_min"] / 60.0
        st.markdown(f'<div class="metric-label">Estimated Travel Time</div><div class="metric-value">{hours:.1f} hrs</div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="metric-label">Traffic Status</div><div style="font-size:1.25rem; font-weight:800; color:{trip["traffic_color"]}; margin-top:0.25rem;">{trip["traffic_label"]}</div>', unsafe_allow_html=True)
    with m4:
        st.markdown(f'<div class="metric-label">CO₂ Footprint</div><div class="metric-value">{trip["co2_kg"]:.2f} kg</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # TABS
    tab_overview, tab_nav, tab_compare, tab_export = st.tabs([
        "🚀 Route Overview & Timing",
        "🗺️ Turn-by-Turn Map & Directions",
        "⚖️ Multi-Modal Transport Comparison",
        "📥 Export Trip Itinerary"
    ])

    # TAB 1: OVERVIEW & DEPARTURE RECOMMENDER
    with tab_overview:
        col_left, col_right = st.columns(2)

        with col_left:
            st.markdown(
                f"""
                <div class="cuberto-card">
                    <span class="cuberto-badge">Immediate Departure</span>
                    <h3 style="margin:0.25rem 0 0.75rem 0; font-size:1.5rem; font-weight:800;">If You Leave Right Now</h3>
                    <p style="color:#57534E; font-size:1rem;">
                        📍 <b>Origin:</b> {trip['start']} ({trip['weather_start']})<br>
                        🎯 <b>Destination:</b> {trip['end']} ({trip['weather_end']})<br><br>
                        ⏱ <b>Base Drive Time:</b> {trip['duration_min']:.0f} mins<br>
                        🚦 <b>Rush Factor:</b> {trip['delay_factor']:.2f}x multiplier<br><br>
                        🟢 <b>Estimated Arrival:</b> 
                        <b style="font-size:1.2rem; color:#1C1917;">
                            {(datetime.now() + timedelta(minutes=trip['adj_duration_min'])).strftime('%I:%M %p')}
                        </b>
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_right:
            # Target Arrival & Recommended Departure Time Calculation
            target_time_clean = target_time_input.strip()
            try:
                if ":" not in target_time_clean:
                    target_time_clean += ":00"
                t_dt = datetime.strptime(target_time_clean, "%H:%M")
                now_dt = datetime.now()
                t_dt = t_dt.replace(year=now_dt.year, month=now_dt.month, day=now_dt.day)
                if t_dt < now_dt:
                    t_dt += timedelta(days=1)

                rec_depart = t_dt - timedelta(minutes=trip['adj_duration_min'])

                st.markdown(
                    f"""
                    <div class="cuberto-card">
                        <span class="cuberto-badge">Target Arrival Planner</span>
                        <h3 style="margin:0.25rem 0 0.75rem 0; font-size:1.5rem; font-weight:800;">Recommended Departure</h3>
                        <p style="color:#57534E; font-size:1rem;">
                            🎯 <b>Target Arrival:</b> {t_dt.strftime('%I:%M %p')}<br>
                            🚦 <b>Traffic Condition:</b> <span style="font-weight:700; color:{trip['traffic_color']}">{trip['traffic_label']}</span><br><br>
                            🚀 <b>YOU SHOULD LEAVE BY:</b><br>
                            <span style="font-size:2rem; font-weight:900; color:#1C1917;">
                                {rec_depart.strftime('%I:%M %p')}
                            </span>
                            <br><small style="color:#78716C;">Includes safety buffer for peak hour traffic</small>
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            except Exception:
                st.warning("Please enter a valid target arrival time e.g. 09:30 or 18:45")

    # TAB 2: TURN-BY-TURN MAP & DIRECTIONS
    with tab_nav:
        col_map, col_steps = st.columns([7, 5])

        with col_map:
            st.markdown("### 🗺️ OSRM Real Road Polyline Map")
            m = folium.Map(location=trip["start_coords"], zoom_start=8, tiles="cartodbpositron")

            # Markers
            folium.Marker(
                trip["start_coords"],
                popup=f"Start: {trip['start']}",
                tooltip="Start Location",
                icon=folium.Icon(color="green", icon="play")
            ).add_to(m)

            folium.Marker(
                trip["end_coords"],
                popup=f"End: {trip['end']}",
                tooltip="Destination",
                icon=folium.Icon(color="red", icon="stop")
            ).add_to(m)

            # Polyline of actual road
            folium.PolyLine(
                trip["polyline"],
                color="#1C1917",
                weight=5,
                opacity=0.85,
                tooltip="OSRM Driving Route"
            ).add_to(m)

            st_folium(m, width="100%", height=420)

        with col_steps:
            st.markdown("### 🧭 Step-by-Step Navigation")
            if trip["turn_steps"]:
                for idx, step in enumerate(trip["turn_steps"][:8], start=1):
                    st.markdown(f'<div class="direction-step"><b>{idx}.</b> {step}</div>', unsafe_allow_html=True)
            else:
                st.info("Follow main highways towards destination.")

    # TAB 3: MULTI-MODAL COMPARISON
    with tab_compare:
        st.markdown("### ⚖️ Multi-Modal Travel & Eco Footprint Comparison")

        modes_list = ["Car 🚗", "Motorcycle 🏍️", "Transit 🚌", "Bicycle 🚴", "Walking 🚶"]
        comparison_data = []

        for m_name in modes_list:
            speed_kmh = 50.0 if "Car" in m_name else (45.0 if "Motorcycle" in m_name else (35.0 if "Transit" in m_name else (15.0 if "Bicycle" in m_name else 4.5)))
            est_hrs = trip["distance_km"] / speed_kmh
            co2, cost = calculate_eco_impact(trip["distance_km"], m_name)
            comparison_data.append({
                "Transport Mode": m_name,
                "Estimated Time (hrs)": round(est_hrs, 2),
                "Est. Cost (₹)": round(cost, 1),
                "CO₂ Emissions (kg)": round(co2, 2),
            })

        df_compare = pd.DataFrame(comparison_data)
        st.dataframe(df_compare, use_container_width=True)

        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.markdown("#### Travel Time Comparison (hours)")
            st.bar_chart(df_compare.set_index("Transport Mode")["Estimated Time (hrs)"])
        with col_c2:
            st.markdown("#### Carbon Footprint (kg CO₂)")
            st.bar_chart(df_compare.set_index("Transport Mode")["CO₂ Emissions (kg)"])

    # TAB 4: EXPORT ITINERARY
    with tab_export:
        st.markdown("### 📥 Download Trip Itinerary")

        md_itinerary = f"""# 🚗 Smart Commute Itinerary: {trip['start']} → {trip['end']}
**Date Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Transport Mode**: {trip['mode']}

---

### 📊 Summary Metrics
- **Road Distance**: {trip['distance_km']:.2f} km
- **Estimated Travel Time**: {trip['adj_duration_min']/60.0:.2f} hours
- **Traffic Level**: {trip['traffic_label']}
- **CO₂ Footprint**: {trip['co2_kg']:.2f} kg CO₂
- **Weather at Origin**: {trip['weather_start']}
- **Weather at Destination**: {trip['weather_end']}

---

### 🧭 Navigation Directions
"""
        for idx, step in enumerate(trip["turn_steps"][:10], start=1):
            md_itinerary += f"{idx}. {step}\n"

        st.download_button(
            label="📄 Download Trip Itinerary as Markdown (.md)",
            data=md_itinerary,
            file_name=f"commute_{trip['start'].lower()}_to_{trip['end'].lower()}.md",
            mime="text/markdown"
        )

        st.download_button(
            label="📦 Download Raw Trip Data as JSON (.json)",
            data=json.dumps(trip, indent=2),
            file_name=f"commute_data_{trip['start'].lower()}_to_{trip['end'].lower()}.json",
            mime="application/json"
        )