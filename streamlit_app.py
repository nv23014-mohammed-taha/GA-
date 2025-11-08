import streamlit as st
import pandas as pd
from utils import load_weather_data, record_observation, weather_statistics, search_by_date, filter_by_month, record_temperatures
import matplotlib.pyplot as plt

st.set_page_config(page_title="🌤️ Weather Tracker", layout="wide")
st.title("🌤️ Weather Tracker")

# Load dataset
df = load_weather_data()

# Sidebar menu
menu = ["Record Observation", "View Statistics", "Search by Date", "View All Observations", "Temperature Trends", "Monthly Filter", "Record Temperatures"]
choice = st.sidebar.selectbox("Choose Option", menu)

if choice=="Record Observation":
    st.header("Add a New Observation")
    date = st.date_input("Date").strftime("%m-%d-%Y")
    temp = st.number_input("Temperature (°C)")
    condition = st.selectbox("Condition", ["Sunny","Cloudy","Rainy","Stormy","Windy","Foggy"])
    humidity = st.number_input("Humidity (%)", 0, 100)
    wind = st.number_input("Wind Speed (km/h)")
    if st.button("Add Observation"):
        record_observation(date, temp, condition, humidity, wind)
        st.success("Observation added successfully!")

elif choice=="View Statistics":
    st.header("Weather Statistics")
    avg, mn, mx, common = weather_statistics(df)
    st.write(f"Average Temperature: {avg:.2f}°C")
    st.write(f"Minimum Temperature: {mn}°C")
    st.write(f"Maximum Temperature: {mx}°C")
    st.write(f"Most Common Condition: {common}")

elif choice=="Search by Date":
    st.header("Search Observations by Date")
    date = st.date_input("Select Date").strftime("%m-%d-%Y")
    result = search_by_date(df, date)
    st.dataframe(result if not result.empty else "No observations found.")

elif choice=="View All Observations":
    st.header("All Observations")
    st.dataframe(df)

elif choice=="Temperature Trends":
    st.header("Temperature Trends Over Year")
    plt.figure(figsize=(12,4))
    plt.plot(pd.to_datetime(df["Date"]), df["Temperature"], marker="o", linestyle="-")
    plt.title("Temperature Trend (2025)")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    st.pyplot(plt)

elif choice=="Monthly Filter":
    st.header("Filter Observations by Month")
    month = st.slider("Select Month", 1, 12)
    filtered = filter_by_month(df, month)
    st.dataframe(filtered)

elif choice=="Record Temperatures":
    st.header("Record-Breaking Temperatures")
    max_row, min_row = record_temperatures(df)
    st.write("🌡️ Highest Temperature:")
    st.write(max_row)
    st.write("❄️ Lowest Temperature:")
    st.write(min_row)
