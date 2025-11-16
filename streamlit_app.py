#!/usr/bin/env python3
"""
Weather Tracker — single-file Python application

Features:
- Record new observations to a CSV
- View statistics (avg/min/max temperature, most common condition)
- Search observations by date
- View all observations in a formatted table
Stretch features:
- ASCII temperature trend
- Filter by month or season
- Naive prediction for tomorrow's temperature
- Compare current year vs previous year averages
- Identify record-breaking temperatures
Usage:
    python weather_tracker.py
The interactive menu will guide you through options.
"""

import pandas as pd
from collections import Counter
from datetime import datetime, timedelta
import os

DATE_FORMAT = '%m-%d-%Y'  # MM-DD-YYYY as requested
DEFAULT_CSV = 'weather_data.csv'

def ensure_csv(path):
    if not os.path.exists(path):
        cols = ['date','temperature_c','condition','humidity_pct','wind_kmh']
        pd.DataFrame(columns=cols).to_csv(path, index=False)

def load_data(path=DEFAULT_CSV):
    ensure_csv(path)
    df = pd.read_csv(path, parse_dates=['date'], dayfirst=False)
    return df

def save_data(df, path=DEFAULT_CSV):
    df.to_csv(path, index=False)

def add_observation(date_str, temperature_c, condition, humidity_pct, wind_kmh, path=DEFAULT_CSV):
    df = load_data(path)
    try:
        date = datetime.strptime(date_str, DATE_FORMAT)
    except ValueError:
        raise ValueError(f"Date must be in {DATE_FORMAT}")
    new = {'date': date, 'temperature_c': float(temperature_c), 'condition': condition,
           'humidity_pct': float(humidity_pct), 'wind_kmh': float(wind_kmh)}
    df = pd.concat([df, pd.DataFrame([new])], ignore_index=True)
    save_data(df, path)
    return df

def view_stats(path=DEFAULT_CSV):
    df = load_data(path)
    if df.empty:
        return None
    temps = df['temperature_c'].astype(float)
    return {
        'avg_temperature_c': temps.mean(),
        'min_temperature_c': temps.min(),
        'max_temperature_c': temps.max(),
        'most_common_condition': Counter(df['condition']).most_common(1)[0][0] if not df['condition'].empty else None
    }

def search_by_date(date_str, path=DEFAULT_CSV):
    df = load_data(path)
    try:
        date = datetime.strptime(date_str, DATE_FORMAT)
    except ValueError:
        raise ValueError(f"Date must be in {DATE_FORMAT}")
    results = df[df['date'] == pd.Timestamp(date)]
    return results

def view_all(path=DEFAULT_CSV):
    return load_data(path).sort_values('date')

# ---------- Stretch features ----------

def ascii_temp_trend(days=14, path=DEFAULT_CSV):
    """
    Simple text-based temperature trend (recent `days` entries).
    Produces short sparkline-like lines: 'MM-DD |   █ 27.3°C'
    """
    df = load_data(path)
    if df.empty:
        return "No data to display."
    cutoff = pd.Timestamp(datetime.now() - timedelta(days=days))
    recent = df[df['date'] >= cutoff].sort_values('date')
    if recent.empty:
        recent = df.sort_values('date').tail(days)
    temps = recent['temperature_c'].astype(float).tolist()
    if not temps:
        return "No temps available."
    min_t, max_t = min(temps), max(temps)
    width = 30
    lines = []
    for d,t in zip(recent['date'].dt.strftime('%m-%d'), temps):
        pos = 0 if max_t==min_t else int((t - min_t) / (max_t - min_t) * (width-1))
        bar = ' ' * pos + '█'
        lines.append(f"{d} |{bar} {t:.1f}°C")
    return "\n".join(lines)

def filter_by_month(month, path=DEFAULT_CSV):
    df = load_data(path)
    return df[df['date'].dt.month == int(month)]

def filter_by_season(season, path=DEFAULT_CSV):
    season_map = {
        'winter': [12,1,2],
        'spring': [3,4,5],
        'summer': [6,7,8],
        'autumn': [9,10,11],
        'fall': [9,10,11]
    }
    months = season_map.get(season.lower())
    if not months:
        raise ValueError('Unknown season. Use winter/spring/summer/autumn.')
    df = load_data(path)
    return df[df['date'].dt.month.isin(months)]

def predict_tomorrow(path=DEFAULT_CSV):
    """
    Naive predictor:
      1) If historical records exist for the same calendar day (any year), use their mean.
      2) Otherwise use the mean of the most recent 7 records.
      3) Otherwise global mean.
    """
    df = load_data(path)
    if df.empty:
        return None
    today = pd.Timestamp(datetime.now().date())
    same_day = df[df['date'].dt.day == today.day]
    if not same_day.empty:
        return same_day['temperature_c'].astype(float).mean()
    recent = df.sort_values('date').tail(7)
    if not recent.empty:
        return recent['temperature_c'].astype(float).mean()
    return df['temperature_c'].astype(float).mean()

def compare_years(year, path=DEFAULT_CSV):
    df = load_data(path)
    df['year'] = df['date'].dt.year
    this = df[df['year'] == int(year)]
    prev = df[df['year'] == int(year)-1]
    return {
        'year': int(year),
        'avg_this_year': this['temperature_c'].astype(float).mean() if not this.empty else None,
        'avg_prev_year': prev['temperature_c'].astype(float).mean() if not prev.empty else None
    }

def record_breakers(path=DEFAULT_CSV):
    df = load_data(path)
    if df.empty:
        return {'highest': None, 'lowest': None}
    highest = df.loc[df['temperature_c'].astype(float).idxmax()].to_dict()
    lowest = df.loc[df['temperature_c'].astype(float).idxmin()].to_dict()
    return {'highest': highest, 'lowest': lowest}

# ---------- Simple CLI (non-GUI) ----------
def menu_loop(path=DEFAULT_CSV):
    ensure_csv(path)
    while True:
        print("\nWeather Tracker")
        print("1. Record a new weather observation")
        print("2. View weather statistics")
        print("3. Search observations by date")
        print("4. View all observations")
        print("5. ASCII temperature trend (14 days)")
        print("6. Filter by month")
        print("7. Predict tomorrow (naive)")
        print("8. Show record breakers")
        print("9. Exit")
        choice = input("Choose an option (1-9): ").strip()
        if choice == '1':
            d = input("Date (MM-DD-YYYY): ").strip()
            temp = input("Temperature (°C): ").strip()
            cond = input("Condition (Sunny/Cloudy/Rainy/etc.): ").strip()
            hum = input("Humidity %: ").strip()
            wind = input("Wind km/h: ").strip()
            try:
                add_observation(d, temp, cond, hum, wind, path=path)
                print("Observation recorded.")
            except Exception as e:
                print("Error:", e)
        elif choice == '2':
            s = view_stats(path=path)
            if not s:
                print("No data.")
            else:
                print(f"Average: {s['avg_temperature_c']:.2f}°C, Min: {s['min_temperature_c']:.2f}°C, Max: {s['max_temperature_c']:.2f}°C, Most common: {s['most_common_condition']}")
        elif choice == '3':
            d = input("Date to search (MM-DD-YYYY): ").strip()
            try:
                res = search_by_date(d, path=path)
                print(res.to_string(index=False) if not res.empty else "No observations for that date.")
            except Exception as e:
                print("Error:", e)
        elif choice == '4':
            print(view_all(path=path).to_string(index=False))
        elif choice == '5':
            print(ascii_temp_trend(days=14, path=path))
        elif choice == '6':
            m = input("Month number (1-12) or season name (e.g. winter): ").strip()
            if m.isdigit():
                print(filter_by_month(int(m), path=path).to_string(index=False))
            else:
                try:
                    print(filter_by_season(m, path=path).to_string(index=False))
                except Exception as e:
                    print("Error:", e)
        elif choice == '7':
            pred = predict_tomorrow(path=path)
            print("Predicted temperature for tomorrow (°C):", f"{pred:.1f}" if pred is not None else "No data")
        elif choice == '8':
            print(record_breakers(path=path))
        elif choice == '9':
            print("Goodbye.")
            break
        else:
            print("Invalid choice.")

if __name__ == '__main__':
    menu_loop()
