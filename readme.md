# 🚗 Smart Commute Assistant — Real-Road Navigation & Mobility Intelligence Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![OSRM Routing](https://img.shields.io/badge/OSRM-Real_Road_Engine-000000?style=for-the-badge&logo=openstreetmap&logoColor=white)](http://project-osrm.org/)
[![Folium Maps](https://img.shields.io/badge/Folium-Interactive_Maps-77B800?style=for-the-badge&logo=leaflet&logoColor=white)](https://python-visualization.github.io/folium/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

An **elite, real-road commute intelligence platform and departure recommendation engine** built with **Python**, **Streamlit**, **OSRM (Open Source Routing Machine)**, **Folium**, and **OpenStreetMap**.

Featuring a **minimalist luxury beige design system**, real highway/city road navigation, multi-modal transport comparison, peak-hour rush traffic estimation, turn-by-turn directions, and eco CO₂ footprint analytics.

🚀 **Live Developer Portfolio**: [https://diyaapoulkar-portfolio.vercel.app](https://diyaapoulkar-portfolio.vercel.app/)

---

## 👤 Developer Profile

**Diyaa Poulkar**  
*Computer Science Student • Developer • Problem Solver*  
🎓 **VIT Bhopal University** — B.Tech in Computer Science Engineering (CGPA: **9.31**)  
💼 Core Technical Team Member at **Linpack Club**  
🏆 2nd Runner Up in **AI AGENTS TRACK** for the SoCF 2.0 Hackathon

---

## ✨ Key Features

- 🎨 **Minimalist Luxury Beige Aesthetic**: High-contrast design system (`#F7F4EF`), pill badges (`#E7E2D7`), sleek rounded cards, and typography (`Outfit` / `Plus Jakarta Sans`).
- 🗺️ **OSRM Real Road Routing Engine**: Replaces straight-line distance math with real road geometry (GeoJSON polylines), turn-by-turn maneuvers, true driving distance (km), and exact road travel duration.
- 🚗 **Multi-Modal Transport Comparison**: Compare travel time, fuel costs, and carbon footprint across **Car 🚗**, **Motorcycle 🏍️**, **Public Transit 🚌**, **Bicycle 🚴**, and **Walking 🚶**.
- ⏱️ **Peak Traffic & Smart Departure Recommender**: Intelligent rush hour model (Morning 8-10 AM, Evening 5-8 PM) calculating exact recommended departure times based on desired target arrival schedules.
- 🌿 **Eco CO₂ Footprint Calculator**: Real-time carbon emission ($kg$ CO₂) and fuel cost estimates for selected transport modes vs green alternatives.
- 🌤️ **Live Weather Integration**: Origin and destination weather status with safety alerts.
- 📥 **1-Click Itinerary Export**: Export complete trip itineraries directly to **Markdown (.md)** or **JSON (.json)**.

---

## 🏗️ Architecture Overview

```mermaid
graph TD
    User([👤 User]) --> |Origin, Destination & Target Time| App[app.py - Streamlit Dashboard]
    App --> |Geocode Query| GeoEngine{Geocoding Engine}
    
    GeoEngine --> |1st Priority| OpenCage[OpenCage API]
    GeoEngine --> |Free Fallback| Nominatim[OpenStreetMap Nominatim]
    
    App --> |Coordinates| OSRM[OSRM Routing Machine API]
    OSRM --> |Real Road Polylines & Turn Steps| App
    
    App --> Weather[OpenWeather / Open-Meteo API]
    App --> Eco[CO2 Footprint & Traffic Model]
    
    App --> FoliumMap[Interactive Folium Map]
    App --> Export[Export Itinerary .md/.json]
```

---

## 🛠️ Tech Stack & Dependencies

| Layer | Technologies Used |
| :--- | :--- |
| **Language & Core** | Python 3.10+ |
| **UI Framework** | Streamlit, Custom Luxury Beige CSS Design System |
| **Real Road Routing** | OSRM (Open Source Routing Machine) |
| **Geocoding & Maps** | Nominatim OpenStreetMap, OpenCage API, Folium, Streamlit-Folium |
| **Weather & Data** | OpenWeatherMap, Open-Meteo, Pandas |

---

## 💻 Local Installation & Setup

### 1. Prerequisites
Ensure you have Python 3.10 or higher installed.

### 2. Clone the Repository
```bash
git clone https://github.com/diyaapoulkar-alt/smart-commute-assistant.git
cd smart-commute-assistant
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. (Optional) Configure API Keys
Create a `.env` file in the project root (or copy `.env.example`):
```bash
cp .env.example .env
```
Add optional keys:
```env
OPENCAGE_KEY=your_opencage_key
OPENWEATHER_KEY=your_openweather_key
```
> 💡 *Note: If no API keys are supplied, the application automatically defaults to free OpenStreetMap Nominatim and Open-Meteo APIs.*

---

## 🚀 Running the Application

1. Change directory to the repository folder:
   ```bash
   cd smart-commute-assistant
   ```
2. Launch the Streamlit Web Dashboard:
   ```bash
   streamlit run app.py
   ```
3. Open `http://localhost:8501` in your browser.

---

## 📂 Project Structure

```text
smart-commute-assistant/
├── app.py                     # Streamlit Luxury Beige Dashboard & OSRM Engine
├── requirements.txt           # Managed Python dependencies
├── .env.example               # Environment variables template
├── SMART COMMUTE ASSISTANT.pdf# Project documentation PDF
└── readme.md                  # Comprehensive repository documentation
```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/diyaapoulkar-alt/smart-commute-assistant/issues).

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for details.
