Weather Tracker App

The Weather Tracker App is an interactive Python web application built with Streamlit that allows users to:

Record daily weather observations.

Analyze weather trends and statistics.

Predict tomorrow’s weather using historical data.

Predict weather conditions from uploaded images using a pre-trained VGG19 deep learning model.

The app combines data processing, machine learning, and image classification to provide a comprehensive weather tracking solution.

Features

Record Observation

Input date, temperature, weather condition, humidity, and wind speed.

Save observations to a CSV file for persistent storage.

View Statistics

Calculate average, minimum, and maximum temperature.

Identify the most common weather condition.

Search and Filter

Search for weather observations by a specific date.

Filter data by month or season (Winter, Spring, Summer, Autumn).

Record-breaking Temperatures

Display the highest and lowest temperatures recorded in the dataset.

Predict Tomorrow

Predict next day’s weather based on last 7 days of historical data.

Predict from Image

Upload a weather image and predict the condition using a trained VGG19 model.

Supports conditions: cloudy, foggy, rainy, shine, sunrise.

View All Observations

Display all recorded weather data in a table.

Dataset

Generated CSV (weather_data.csv):
Contains a 1-year (2025) dataset with realistic seasonal temperatures, humidity, wind speed, and weather conditions.

Image Dataset:
vijaygiitk/multiclass-weather-dataset from Kaggle, used for training the VGG19 model.

CSV Columns:

Date (MM-DD-YYYY)

Temperature (°C)

Condition (Sunny, Cloudy, Rainy, Stormy, Windy, Foggy)

Humidity (%)

WindSpeed (km/h)

Requirements

Python 3.10+

Libraries:

streamlit
pandas
numpy
opencv-python
tensorflow
matplotlib
seaborn
mlxtend
pillow


Pre-trained VGG19 model (vgg19.h5) in the app folder.
Usage

Open the app in your browser.

Use the sidebar menu to navigate between features.

Record new observations or upload an image to predict weather.

Explore statistics, filters, and temperature records.

Tips:

Ensure uploaded images are clear and properly oriented for accurate predictions.

The app automatically generates weather data if weather_data.csv is missing.

Model

Architecture: VGG19 (pre-trained on ImageNet) + Flatten + Dense(5, softmax)

Classes: cloudy, foggy, rainy, shine, sunrise

Training:

Optimizer: Adam

Loss: Categorical Crossentropy

Epochs: 15

Batch Size: 32

EarlyStopping and ModelCheckpoint used
