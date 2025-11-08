import pandas as pd
import random
from datetime import datetime, timedelta
from collections import Counter

CSV_FILE = "weather_data.csv"

# Generate 1-year dataset (2025) with seasonal variation
def generate_weather_data():
    conditions = ["Sunny", "Cloudy", "Rainy", "Stormy", "Windy", "Foggy"]
    start_date = datetime(2025, 1, 1)
    rows = []
    for i in range(365):
        dt = start_date + timedelta(days=i)
        month = dt.month
        # Seasonal temperature
        if month in (12,1,2): temp = random.randint(8,20)
        elif month in (3,4,5): temp = random.randint(15,26)
        elif month in (6,7,8): temp = random.randint(25,40)
        else: temp = random.randint(18,30)
        temp += int(random.gauss(0,2))
        cond = random.choices(conditions, weights=[40,25,20,5,6,4], k=1)[0]
        if cond=="Rainy": humidity=random.randint(70,95)
        elif cond=="Stormy": humidity=random.randint(75,98)
        elif cond=="Foggy": humidity=random.randint(80,95)
        else: humidity=random.randint(35,80)
        wind=random.randint(3,30)
        rows.append({"Date": dt.strftime("%m-%d-%Y"), "Temperature": temp, "Condition": cond,
                     "Humidity": humidity, "WindSpeed": wind})
    df = pd.DataFrame(rows)
    df.to_csv(CSV_FILE, index=False)
    return df

# Load existing CSV
def load_weather_data():
    try:
        return pd.read_csv(CSV_FILE)
    except FileNotFoundError:
        return generate_weather_data()

# Record new observation
def record_observation(date, temp, condition, humidity, wind):
    df = load_weather_data()
    new_row = {"Date": date, "Temperature": temp, "Condition": condition,
               "Humidity": humidity, "WindSpeed": wind}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

# Basic statistics
def weather_statistics(df):
    avg_temp = df["Temperature"].mean()
    min_temp = df["Temperature"].min()
    max_temp = df["Temperature"].max()
    most_common_condition = Counter(df["Condition"]).most_common(1)[0][0]
    return avg_temp, min_temp, max_temp, most_common_condition

# Filter by date
def search_by_date(df, date):
    return df[df["Date"]==date]

# Filter by month
def filter_by_month(df, month):
    return df[pd.to_datetime(df["Date"]).dt.month==month]

# Record-breaking temperatures
def record_temperatures(df):
    return df.loc[df["Temperature"].idxmax()], df.loc[df["Temperature"].idxmin()]
