import streamlit as st
import requests
import math
from datetime import datetime, timedelta
import folium
from streamlit_folium import st_folium
import pandas as pd
import time

# ================== API KEYS ==================
OPENCAGE_KEY = "ff5da74a3813406eb539b7df97a9d72f"
OPENWEATHER_KEY = "7beb61cdd2ceae85227c9d7135e6867d"
# =============================================

# --------- Functions ---------

def get_coordinates(place):
    url = f"https://api.opencagedata.com/geocode/v1/json?q={place}&key={OPENCAGE_KEY}"
    data = requests.get(url).json()
    if data['results']:
        lat = data['results'][0]['geometry']['lat']
        lon = data['results'][0]['geometry']['lng']
        return lat, lon
    return None, None

def get_weather(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_KEY}&units=metric"
    data = requests.get(url).json()
    if 'weather' in data:
        return data['weather'][0]['main'], data['main']['temp']
    return "Unknown", 0

def get_distance(c1, c2):
    lat1, lon1 = c1
    lat2, lon2 = c2

    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return R * c

def predict_time(distance):
    return distance * 2

def traffic_level(time):
    if time > 600:
        return "High"
    elif time > 300:
        return "Medium"
    return "Low"

def traffic_color(level):
    if level == "High":
        return "red"
    elif level == "Medium":
        return "orange"
    return "green"

# --------- PAGE ---------
st.set_page_config(page_title="🚗 Smart Commute Assistant", layout="wide")

# --------- CSS ---------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #FFF176, #FFD54F);
    font-family: 'Segoe UI', sans-serif;
}

@keyframes fadeIn {
    from {opacity: 0; transform: translateY(20px);}
    to {opacity: 1; transform: translateY(0);}
}

h1 {
    text-align: center;
    color: #0D47A1;
}

.stButton>button {
    background-color: #0D47A1;
    color: white;
    border-radius: 10px;
    height: 50px;
    font-size: 18px;
    font-weight: bold;
}

.card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.25);
    margin: 10px 0;
    animation: fadeIn 0.8s ease-in-out;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>🚗 Smart Commute Assistant</h1>", unsafe_allow_html=True)

# --------- INPUT ---------
col1, col2 = st.columns(2)

with col1:
    start = st.text_input("📍 Current Location", "Nashik")

with col2:
    end = st.text_input("🎯 Destination", "Mumbai")

reach = st.text_input("⏰ Arrival Time (HH:MM)")

if "result" not in st.session_state:
    st.session_state.result = None

# --------- BUTTON ---------
if st.button("🚀 Calculate Route"):

    progress = st.progress(0)
    status = st.empty()

    status.text("📍 Getting coordinates...")
    progress.progress(20)
    time.sleep(0.4)

    start_c = get_coordinates(start)
    end_c = get_coordinates(end)

    if not start_c[0] or not end_c[0]:
        st.error("❌ Location error")
    else:
        status.text("🌦 Fetching weather...")
        progress.progress(50)
        time.sleep(0.4)

        weather1, temp1 = get_weather(*start_c)
        weather2, temp2 = get_weather(*end_c)

        status.text("🧠 Calculating smart route...")
        progress.progress(80)
        time.sleep(0.4)

        distance = get_distance(start_c, end_c)
        time_minutes = predict_time(distance)
        traffic = traffic_level(time_minutes)

        now = datetime.now()
        arrival_now = now + timedelta(minutes=time_minutes)

        progress.progress(100)
        status.text("✅ Done!")
        time.sleep(0.4)

        progress.empty()
        status.empty()

        st.session_state.result = {
            "distance": distance,
            "time": time_minutes,
            "traffic": traffic,
            "weather1": weather1,
            "temp1": temp1,
            "weather2": weather2,
            "temp2": temp2,
            "arrival_now": arrival_now,
            "start_c": start_c,
            "end_c": end_c
        }

# --------- DISPLAY ---------
if st.session_state.result:
    r = st.session_state.result
    color = traffic_color(r["traffic"])

    st.markdown("## 📊 Trip Summary")

    st.markdown(f"""
    <div class="card">
    🚗 <b>Distance:</b> {r['distance']:.2f} km<br><br>
    ⏱ <b>Estimated Travel Time:</b> {r['time']/60:.2f} hours<br><br>
    🚦 <b>Traffic Level:</b> 
    <span style='color:{color}; font-weight:bold; font-size:18px;'>{r['traffic']}</span><br><br>
    🌦 <b>Weather:</b><br>
    Start → {r['weather1']} ({r['temp1']}°C)<br>
    End → {r['weather2']} ({r['temp2']}°C)<br><br>
    🟢 <b>If you leave NOW:</b><br>
    Reach by <b>{r['arrival_now'].strftime('%H:%M')}</b>
    </div>
    """, unsafe_allow_html=True)

    # Leave Time
    if reach:
        try:
            if ":" not in reach:
                reach += ":00"

            target = datetime.strptime(reach, "%H:%M")
            now = datetime.now()
            target = target.replace(year=now.year, month=now.month, day=now.day)

            if target < now:
                target += timedelta(days=1)

            leave = target - timedelta(minutes=r['time'])

            st.markdown(f"""
            <div class="card">
            🔵 <b>Planned Journey</b><br><br>
            🎯 Target Arrival: <b>{target.strftime('%H:%M')}</b><br>
            🚀 Recommended Departure: <b>{leave.strftime('%H:%M')}</b><br><br>
            ⚡ Plan your trip accordingly!
            </div>
            """, unsafe_allow_html=True)

        except:
            st.error("❌ Invalid time")

    # --------- GRAPH ---------
    st.markdown("## 📈 Travel Analysis")

    col1, col2 = st.columns(2)
    col1.metric("🚗 Distance (km)", f"{r['distance']:.2f}")
    col2.metric("⏱ Time (hrs)", f"{r['time']/60:.2f}")

    chart_data = pd.DataFrame({
        "Value": [r['distance'], r['time']/60]
    }, index=["Distance (km)", "Time (hrs)"])

    st.bar_chart(chart_data)

    # --------- MAP ---------
    st.markdown("## 🗺 Route Map")

    m = folium.Map(location=r['start_c'], zoom_start=6)
    folium.Marker(r['start_c'], tooltip="Start").add_to(m)
    folium.Marker(r['end_c'], tooltip="End").add_to(m)
    folium.PolyLine([r['start_c'], r['end_c']], color=color).add_to(m)

    st_folium(m, width=800, height=400)