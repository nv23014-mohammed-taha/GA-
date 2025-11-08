import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import load_weather_data, record_observation, weather_statistics, search_by_date, filter_by_month, filter_by_season, record_temperatures, predict_tomorrow
from weather_model import predict_weather_from_image

st.set_page_config(page_title="🌤️ Weather Tracker", layout="wide")
st.title("🌤️ Weather Tracker")

# Load dataset
year = st.sidebar.selectbox("Select Year", [2025, 2024])
df = load_weather_data(year)

# Sidebar menu
menu = ["Record Observation","View Statistics","Search by Date","View All Observations",
        "Temperature Trends","Monthly Filter","Season Filter","Record Temperatures",
        "Predict Tomorrow","Weather from Image"]
choice = st.sidebar.selectbox("Choose Option", menu)

if choice=="Record Observation":
    st.header("Add a New Observation")
    date = st.date_input("Date").strftime("%m-%d-%Y")
    temp = st.number_input("Temperature (°C)")
    condition = st.selectbox("Condition", ["Sunny","Cloudy","Rainy","Stormy","Windy","Foggy"])
    humidity = st.number_input("Humidity (%)", 0, 100)
    wind = st.number_input("Wind Speed (km/h)")
    if st.button("Add Observation"):
        df = record_observation(df, date, temp, condition, humidity, wind)
        st.success("Observation added successfully!")

elif choice=="View Statistics":
    st.header("Weather Statistics")
    avg, mn, mx, common = weather_statistics(df)
    st.write(f"Average Temp: {avg:.2f}°C")
    st.write(f"Min Temp: {mn}°C")
    st.write(f"Max Temp: {mx}°C")
    st.write(f"Most Common Condition: {common}")

elif choice=="Search by Date":
    st.header("Search Observations by Date")
    date = st.date_input("Select Date").strftime("%m-%d-%Y")
    res = search_by_date(df,date)
    st.dataframe(res if not res.empty else "No observations found.")

elif choice=="View All Observations":
    st.header("All Observations")
    st.dataframe(df)

elif choice=="Temperature Trends":
    st.header("Temperature Trends Over Year")
    plt.figure(figsize=(12,4))
    plt.plot(pd.to_datetime(df["Date"]), df["Temperature"], marker="o")
    plt.xlabel("Date"); plt.ylabel("Temperature (°C)")
    plt.title(f"Temperature Trend ({year})")
    st.pyplot(plt)

elif choice=="Monthly Filter":
    st.header("Filter by Month")
    month = st.slider("Month",1,12)
    filtered = filter_by_month(df, month)
    st.dataframe(filtered)

elif choice=="Season Filter":
    st.header("Filter by Season")
    season = st.selectbox("Select Season", ["Winter","Spring","Summer","Autumn"])
    filtered = filter_by_season(df, season)
    st.dataframe(filtered)

elif choice=="Record Temperatures":
    st.header("Record-Breaking Temperatures")
    max_row, min_row = record_temperatures(df)
    st.write("🌡️ Highest Temp:"); st.write(max_row)
    st.write("❄️ Lowest Temp:"); st.write(min_row)

elif choice=="Predict Tomorrow":
    st.header("Predict Tomorrow's Weather")
    temp, cond = predict_tomorrow(df)
    st.write(f"Predicted Temperature: {temp}°C")
    st.write(f"Predicted Condition: {cond}")

elif choice=="Weather from Image":
    st.header("Predict Weather from Uploaded Image")
    uploaded_file = st.file_uploader("Upload Image", type=["jpg","png","jpeg"])
    if uploaded_file is not None:
        with open("temp_img.jpg","wb") as f:
            f.write(uploaded_file.getbuffer())
        pred_class, prob = predict_weather_from_image("temp_img.jpg")
        st.image("temp_img.jpg", caption="Uploaded Image", use_column_width=True)
        st.write(f"Predicted Weather: {pred_class} ({prob*100:.1f}%)")
