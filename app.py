import streamlit as st
import requests
import matplotlib.pyplot as plt
from datetime import datetime

# Title and description
st.title("🌤️ Weather Forecasting App")
st.write("Get the current weather and forecast for your city!")

# User input for city name
city_name = st.text_input("Enter City Name", "")

# OpenWeatherMap API details
#api_key = ""  
base_url = "https://api.openweathermap.org/data/2.5/"

# Fetch current weather data
def get_weather(city):
    url = f"{base_url}weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Fetch forecast data
def get_forecast(city):
    url = f"{base_url}forecast?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Display current weather
if city_name:
    weather_data = get_weather(city_name)
    if weather_data is None:
        st.error("City not found or API error! Please check the city name and try again.")
    else:
        st.subheader(f"🌍 Current Weather in {city_name}")
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']
        description = weather_data['weather'][0]['description'].title()

        st.write(f"**Temperature:** {temp} °C")
        st.write(f"**Humidity:** {humidity} %")
        st.write(f"**Wind Speed:** {wind_speed} m/s")
        st.write(f"**Condition:** {description}")

        # Display weather icon
        icon_code = weather_data['weather'][0]['icon']
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}.png"
        st.image(icon_url, width=100)

        # Display forecast
        forecast_data = get_forecast(city_name)
        if forecast_data:
            dates = []
            temps = []
            humidities = []
            wind_speeds = []

            for forecast in forecast_data['list'][:10]:  # Get data for the next 10 periods (3-hour intervals)
                dt = datetime.utcfromtimestamp(forecast['dt']).strftime('%Y-%m-%d %H:%M:%S')
                dates.append(dt)
                temps.append(forecast['main']['temp'])
                humidities.append(forecast['main']['humidity'])
                wind_speeds.append(forecast['wind']['speed'])

            # Plotting the data
            fig, ax = plt.subplots(3, 1, figsize=(8, 12))

            ax[0].plot(dates, temps, marker='o', linestyle='-', color='blue', label='Temperature (°C)')
            ax[0].set_title('Temperature Trend')
            ax[0].set_xticks(range(len(dates)))
            ax[0].set_xticklabels(dates, rotation=45)
            ax[0].legend()

            ax[1].plot(dates, humidities, marker='o', linestyle='-', color='green', label='Humidity (%)')
            ax[1].set_title('Humidity Trend')
            ax[1].set_xticks(range(len(dates)))
            ax[1].set_xticklabels(dates, rotation=45)
            ax[1].legend()

            ax[2].plot(dates, wind_speeds, marker='o', linestyle='-', color='purple', label='Wind Speed (m/s)')
            ax[2].set_title('Wind Speed Trend')
            ax[2].set_xticks(range(len(dates)))
            ax[2].set_xticklabels(dates, rotation=45)
            ax[2].legend()

            st.pyplot(fig)
        else:
            st.error("Could not retrieve forecast data. Please try again later.")
