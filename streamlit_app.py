# streamlit_app.py

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from collections import Counter
from tensorflow.keras.models import load_model
from PIL import Image
import os

# ------------------------
# CSV / Weather functions
# ------------------------
CSV_FILE = "weather_data.csv"

def generate_weather_data():
    """Generate 1-year (2025) dataset with seasonal variation"""
    conditions = ["Sunny", "Cloudy", "Rainy", "Stormy", "Windy", "Foggy"]
    start_date = datetime(2025, 1, 1)
    rows = []
    for i in range(365):
        dt = start_date + timedelta(days=i)
        month = dt.month
        if month in (12,1,2):
            temp = np.random.randint(8,20)
        elif month in (3,4,5):
            temp = np.random.randint(15,26)
        elif month in (6,7,8):
            temp = np.random.randint(25,40)
        else:
            temp = np.random.randint(18,30)
        temp += int(np.random.normal(0,2))
        cond = np.random.choice(conditions, p=[0.4,0.25,0.2,0.05,0.06,0.04])
        if cond=="Rainy":
            humidity = np.random.randint(70,95)
        elif cond=="Stormy":
            humidity = np.random.randint(75,98)
        elif cond=="Foggy":
            humidity = np.random.randint(80,95)
        else:
            humidity = np.random.randint(35,80)
        wind = np.random.randint(3,30)
        rows.append({
            "Date": dt.strftime("%m-%d-%Y"),
            "Temperature": temp,
            "Condition": cond,
            "Humidity": humidity,
            "WindSpeed": wind
        })
    df = pd.DataFrame(rows)
    df.to_csv(CSV_FILE, index=False)
    return df

def load_weather_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return generate_weather_data()

def record_observation(date, temp, condition, humidity, wind):
    df = load_weather_data()
    new_row = {"Date": date, "Temperature": temp, "Condition": condition,
               "Humidity": humidity, "WindSpeed": wind}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)
    return df

def weather_statistics(df):
    avg_temp = df["Temperature"].mean()
    min_temp = df["Temperature"].min()
    max_temp = df["Temperature"].max()
    most_common_condition = Counter(df["Condition"]).most_common(1)[0][0]
    return avg_temp, min_temp, max_temp, most_common_condition

def search_by_date(df, date):
    return df[df["Date"]==date]

def filter_by_month(df, month):
    return df[pd.to_datetime(df["Date"]).dt.month==month]

def filter_by_season(df, season):
    month_map = {"Winter":[12,1,2], "Spring":[3,4,5], "Summer":[6,7,8], "Autumn":[9,10,11]}
    months = month_map.get(season, [])
    return df[pd.to_datetime(df["Date"]).dt.month.isin(months)]

def record_temperatures(df):
    return df.loc[df["Temperature"].idxmax()], df.loc[df["Temperature"].idxmin()]

def predict_tomorrow(df):
    df_dates = pd.to_datetime(df["Date"])
    last_week = df[df_dates >= df_dates.max() - pd.Timedelta(days=7)]
    avg_temp = last_week["Temperature"].mean()
    most_common_condition = Counter(last_week["Condition"]).most_common(1)[0][0]
    return round(avg_temp,1), most_common_condition

# ------------------------
# Image-based prediction
# ------------------------
MODEL_PATH = "vgg19.h5"
CLASSES = ["cloudy","foggy","rainy","shine","sunrise"]

try:
    model = load_model(MODEL_PATH)
except Exception:
    model = None

def predict_weather_from_image(img_file):
    if model is None:
        return None, None
    img = Image.open(img_file).resize((150,150))
    img = np.array(img)/255.0
    img = np.expand_dims(img, axis=0)
    pred = model.predict(img)
    class_idx = np.argmax(pred)
    return CLASSES[class_idx], float(pred[0][class_idx])

# ------------------------
# Streamlit UI
# ------------------------
st.title("🌤 Weather Tracker App")
df = load_weather_data()

menu = st.sidebar.selectbox("Menu", [
    "Record Observation",
    "View Statistics",
    "Search by Date",
    "Filter by Month/Season",
    "Record-breaking Temps",
    "Predict Tomorrow",
    "Predict from Image",
    "View All Observations"
])

# 1️⃣ Record Observation
if menu=="Record Observation":
    st.header("Record a New Weather Observation")
    date_input = st.date_input("Date")
    date_str = date_input.strftime("%m-%d-%Y")
    temp = st.number_input("Temperature (°C)", min_value=-50, max_value=60)
    condition = st.selectbox("Condition", ["Sunny","Cloudy","Rainy","Stormy","Windy","Foggy"])
    humidity = st.number_input("Humidity (%)", min_value=0, max_value=100)
    wind = st.number_input("Wind Speed (km/h)", min_value=0, max_value=200)
    if st.button("Record Observation"):
        df = record_observation(date_str, temp, condition, humidity, wind)
        st.success(f"Observation for {date_str} recorded!")

# 2️⃣ View Statistics
elif menu=="View Statistics":
    st.header("Weather Statistics")
    avg_temp, min_temp, max_temp, most_common = weather_statistics(df)
    st.write(f"Average Temperature: {avg_temp:.1f}°C")
    st.write(f"Minimum Temperature: {min_temp}°C")
    st.write(f"Maximum Temperature: {max_temp}°C")
    st.write(f"Most Common Condition: {most_common}")

# 3️⃣ Search by Date
elif menu=="Search by Date":
    st.header("Search Observations by Date")
    date_input = st.date_input("Select Date")
    date_str = date_input.strftime("%m-%d-%Y")
    res = search_by_date(df, date_str)
    if not res.empty:
        st.dataframe(res)
    else:
        st.write("No observations found.")

# 4️⃣ Filter by Month/Season
elif menu=="Filter by Month/Season":
    st.header("Filter Observations")
    filter_type = st.radio("Filter by:", ["Month","Season"])
    if filter_type=="Month":
        month = st.number_input("Enter month (1-12)",1,12)
        res = filter_by_month(df, month)
    else:
        season = st.selectbox("Select season", ["Winter","Spring","Summer","Autumn"])
        res = filter_by_season(df, season)
    if not res.empty:
        st.dataframe(res)
    else:
        st.write("No observations found.")

# 5️⃣ Record-breaking Temperatures
elif menu=="Record-breaking Temps":
    st.header("Record-breaking Temperatures")
    max_row, min_row = record_temperatures(df)
    st.write("🔥 Highest Temperature:")
    st.dataframe(max_row.to_frame().T)
    st.write("❄️ Lowest Temperature:")
    st.dataframe(min_row.to_frame().T)

# 6️⃣ Predict Tomorrow
elif menu=="Predict Tomorrow":
    st.header("Predict Tomorrow's Weather")
    temp, cond = predict_tomorrow(df)
    st.write(f"Predicted Temperature: {temp}°C")
    st.write(f"Predicted Condition: {cond}")

# 7️⃣ Predict from Image
elif menu == "Predict from Image":
    st.header("Predict Today's Weather from Image")
    img_file = st.file_uploader("Upload an image", type=["jpg","png","jpeg"])
    
    if img_file is not None:
        if model is None:
            st.error("⚠️ Model not loaded. Make sure 'vgg19.h5' is in your app folder or correct path is set.")
        else:
            pred_class, prob = predict_weather_from_image(img_file)
            st.success(f"Predicted Condition: {pred_class}")
            st.info(f"Confidence: {prob*100:.1f}%")
            st.image(img_file, caption="Uploaded Image", use_column_width=True)


# 8️⃣ View All Observations
elif menu=="View All Observations":
    st.header("All Recorded Weather Observations")
    st.dataframe(df)
