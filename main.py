import requests
import tkinter as tk
from tkinter import messagebox
import os
import sys
from dotenv import load_dotenv


# Load variables from the .env file into the system environment
load_dotenv()

# Retrieve the hidden API key 
api_key = os.getenv("API_KEY")

# Main Colors
BG_COLOR = "#0F172A"          # Window background
CARD_COLOR = "#1E293B"        # Weather card

# Text Colors
TEXT_COLOR = "#F8FAFC"        # Main text
SECONDARY_TEXT = "#CBD5E1"    # Description & labels

# Accent Colors
BUTTON_COLOR = "#3B82F6"      # Search button
BUTTON_HOVER = "#60A5FA"      # Hover effect

# Borders
BORDER_COLOR = "#334155"      # Subtle card borders


def get_weather_data(city, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?"

    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    try:
        response = requests.get(url, params=params, timeout=15)

        match response.status_code:
            case 200:
                data = response.json()

            case 404:
                return None, "City not found."

            case 401:
                return None, "Invalid API key."

            case 429:
                return None, "Too many requests."

            case status if status >= 500:
                return None, "Weather service is temporarily unavailable."
            
            case _:
                return None, f"Unexpected error ({response.status_code})"

        weather_data = {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temperature": data["main"]["temp"],
            # "feels_like": data["main"]["feels_like"],
            "condition": data["weather"][0]["main"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "pressure": data["main"]["pressure"],
            # "visibility": data["visibility"] / 1000
        }

        return weather_data, None
    
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None, "Request failed."


def get_weather_icon(description):
    description = description.lower()

    if "clear" in description:
        return "☀️"
    elif "cloud" in description:
        return "☁️"
    elif "rain" in description:
        return "🌧️"
    elif "thunder" in description:
        return "⛈️"
    elif "snow" in description:
        return "❄️"
    elif "mist" in description or "fog" in description:
        return "🌫️"

    return "🌤️"
    

def search_weather():
    city = city_entry.get().strip()

    if not city:
        messagebox.showwarning("Warning", "Please enter a city name.")
        return
    
    weather, error = get_weather_data(city, api_key)

    if error:
        messagebox.showerror("Error", error)
        return

    icon_label.config(text=get_weather_icon(weather['description']))
    temp_label.config(text=f"{round(weather['temperature'])}°C")
    city_label.config(text=f"{weather['city']}, {weather['country']}")
    desc_label.config(text=weather['description'].title())

    humidity_value.config(text=f"{weather['humidity']}%")
    wind_value.config(text=f"{weather['wind_speed']:.1f} m/s")
    pressure_value.config(text=f"{weather['pressure']} hPa")
    

# ---------------- WINDOW ----------------

root = tk.Tk()
root.geometry("400x550")
root.title("Weather App")
root.config(background=BG_COLOR, )
root.resizable(False, False)

icon = tk.PhotoImage(file="logo.png")
root.iconphoto(True, icon)

if not api_key:
    messagebox.showerror("API Key Error", "API key not found.\nPlease add API_KEY to your .env file.")
    root.destroy()
    sys.exit()

# Title
title_label = tk.Label(
    root,
    text="Weather App",
    font=("Segoe UI", 24, "bold"),
    bg = BG_COLOR,
    fg = TEXT_COLOR
)
title_label.pack(pady=20)

# Search Section
city_entry = tk.Entry(
    root,
    width=25,
    font=("Segoe UI", 14),
    justify="center",
    relief="flat",
    bg = "#E2E8F0"
)
city_entry.pack(pady=10)

search_button = tk.Button(
    root,
    text="Get Weather",
    font=("Segoe UI", 12, "bold"),
    command=search_weather,
    bg=BUTTON_COLOR,
    fg=TEXT_COLOR,
    activebackground=BUTTON_HOVER,
    activeforeground="white",
    relief="flat",
    bd=0,
    cursor="hand2"
)
search_button.pack(pady=15)

# Enter key support
city_entry.bind(                   # .bind creates an event object
    "<Return>",
    lambda event: search_weather() # Ignore event object and trigger search_weather function
    )

# Weather Card
weather_frame = tk.Frame(
    root,
    bg=CARD_COLOR,
    padx=15,
    pady=20
)
weather_frame.pack(
    padx=20,
    pady=20,
    fill="x"
)

weather_frame.columnconfigure(0, weight=1)

weather_frame.configure(highlightbackground=BORDER_COLOR)
weather_frame.configure(highlightthickness=2)

icon_label = tk.Label(
    weather_frame,
    text="🌤️",
    font=("Segoe UI Emoji", 28),
    bg=CARD_COLOR,
    fg="white"
)
icon_label.grid(row=0, column=0)

temp_label = tk.Label(
    weather_frame,
    text="--°C",
    font=("Segoe UI", 30, "bold"),
    bg=CARD_COLOR,
    fg="white"
)
temp_label.grid(row=1, column=0)

city_label = tk.Label(
    weather_frame,
    text="Search a city",
    font=("Segoe UI", 12, "bold"),
    bg=CARD_COLOR,
    fg="white"
)
city_label.grid(row=2, column=0)

desc_label = tk.Label(
    weather_frame,
    text="",
    font=("Segoe UI", 11),
    bg=CARD_COLOR,
    fg=SECONDARY_TEXT
)
desc_label.grid(row=3, column=0)

metrics_frame = tk.Frame(
    weather_frame,
    bg=CARD_COLOR,
    pady=20
)
metrics_frame.grid(
    row=4,
    column=0,
    pady=20,
    sticky="ew"
)

metrics_frame.columnconfigure(0, weight=1)
metrics_frame.columnconfigure(1, weight=1)
metrics_frame.columnconfigure(2, weight=1)

humidity_label = tk.Label(
    metrics_frame,
    text="Humidity",
    font=("Segoe UI", 11),
    bg=CARD_COLOR,
    fg=SECONDARY_TEXT
)
humidity_label.grid(row=0, column=0)

humidity_value = tk.Label(
    metrics_frame,
    text="---",
    font=("Segoe UI", 12, "bold"),
    bg=CARD_COLOR,
    fg=SECONDARY_TEXT
)
humidity_value.grid(row=1, column=0)

wind_label = tk.Label(
    metrics_frame,
    text="Wind",
    font=("Segoe UI", 11),
    bg=CARD_COLOR,
    fg=SECONDARY_TEXT
)
wind_label.grid(row=0, column=1)

wind_value = tk.Label(
    metrics_frame,
    text="---",
    font=("Segoe UI", 12, "bold"),
    bg=CARD_COLOR,
    fg=SECONDARY_TEXT
)
wind_value.grid(row=1, column=1)

pressure_label = tk.Label(
    metrics_frame,
    text="Pressure",
    font=("Segoe UI", 11),
    bg=CARD_COLOR,
    fg=SECONDARY_TEXT
)
pressure_label.grid(row=0, column=2)

pressure_value = tk.Label(
    metrics_frame,
    text="---",
    font=("Segoe UI", 12, "bold"),
    bg=CARD_COLOR,
    fg=SECONDARY_TEXT
)
pressure_value.grid(row=1, column=2)

root.mainloop()