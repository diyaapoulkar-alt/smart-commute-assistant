# 🚗 Smart Commute Assistant (with Machine Learning)

## 👩‍💻 Author
**Diya Annasaheb Poulkar**

---

## ⭐ Notes
- Developed for academic purposes  
- Requires internet for API access  
- API keys are necessary to run the app  
## 📌 Project Overview
The **Smart Commute Assistant** is a Python-based web application that helps users plan their daily travel efficiently. It calculates distance, predicts travel time using a **Machine Learning model**, analyzes traffic conditions, and fetches real-time weather data.

The application is built using **Streamlit** and integrates multiple APIs to provide a complete commute analysis in a simple and interactive interface.

---

## 🎯 Objectives
- To provide accurate commute insights based on user input  
- To integrate Machine Learning for travel time prediction  
- To enhance decision-making using weather and traffic data  
- To create a user-friendly and interactive web application  

---

## ⚙️ Features
- 📍 Source & Destination input  
- 🌍 Location to coordinates conversion (Geocoding API)  
- 📏 Distance calculation using Haversine Formula  
- 🤖 Travel time prediction using Linear Regression (ML Model)  
- 🚦 Traffic level estimation (Low / Medium / High)  
- 🌦️ Real-time weather data integration  
- 🗺️ Interactive map visualization using Folium  
- 📊 Data visualization and trip summary  

---

## 🧠 Machine Learning Integration
This project uses a **Linear Regression model** to predict travel time based on distance.

- Input: Distance  
- Output: Travel Time  
- Library Used: Scikit-learn  

---

## 🏗️ System Workflow
User Input → Geocoding → Distance Calculation → ML Model → Time Prediction → Traffic Analysis → Weather Fetch → Output Display  
<img width="1536" height="1024" alt="c48c7969-c0c8-4a1b-a014-8eafebfbfa3a" src="https://github.com/user-attachments/assets/8c6fd889-ce11-4cac-82a2-129d1400430a" />

---

## 🧪 Testing
- Functional Testing (input, APIs, calculations)  
- Reliability Testing (API failure handling)  
- Performance Testing (response time)  
- Usability Testing (UI and experience)  

---

## ⚠️ Challenges Faced
- API reliability and rate limits  
- Accuracy of prediction  
- Handling invalid inputs  
- Map integration in Streamlit  
- Performance optimization  

---
## 🚀 Future Enhancements
- Advanced ML models  
- Real-time traffic APIs  
- Route optimization  
- Save user preferences  
- Mobile-friendly UI  

---

## 🛠️ Technologies Used
- Python  
- Streamlit  
- Scikit-learn  
- Pandas  
- Requests  
- Folium  
- Streamlit-Folium  
- OpenCage API  
- OpenWeather API  

---

## 📂 Project Structure
Smart-Commute-Assistant/
│── app.py
│── README.md
│── requirements.txt
│
├── docs/
│ └── Project_Report.pdf


---

## ⚙️ Setup Instructions

### 1. Clone Repository
git clone https://github.com/diyaapoulkar-alt/smart-commute-assistant
cd smart-commute-assistant
### 2. Install Dependencies
pip install -r requirements.txt

### 3. Add API Keys
Create your own API keys from:
- OpenCage Geocoding API  
- OpenWeather API  

Then replace in the code:
OPENCAGE_API_KEY = "your_opencage_api_key"
WEATHER_API_KEY = "your_openweather_api_key"

### 4. Run Application
streamlit run app.py

## 📚 References
- Python Documentation  
- Scikit-learn Documentation  
- Streamlit Documentation  
- OpenCage API Docs  
- OpenWeather API Docs  
---

## ⭐ Notes
- Developed for academic purposes  
- Requires internet for API access  
- API keys are necessary to run the app  
