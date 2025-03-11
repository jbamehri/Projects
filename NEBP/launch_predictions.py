# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 00:01:48 2025

@author: joahb
"""

import time
import requests
import discord
from datetime import datetime, timedelta
from discord.ext import tasks
import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# Discord bot token and channel ID
DISCORD_TOKEN = ""
CHANNEL_ID = 1151543485887954974

# Base URL for SondeHub Predictor
BASE_URL = "https://predict.sondehub.org/"

# Launch locations with names
LOCATIONS = [
    {"name": "South of Kalamazoo", "lat": 42.2674, "lon": 274.398},
    {"name": "South of Jackson", "lat": 42.2128, "lon": 275.5872}
]

# Prediction parameters
ASCENT_RATE = 5
BURST_ALTITUDE = 29000
DESCENT_RATE = 7
PREDICTION_TYPE = "3_hour"
PROFILE = "standard_profile"

# Function to get current start and end times
def get_prediction_times():
    start_time = datetime.now()
    end_time = start_time + timedelta(days=7)
    return start_time.strftime('%B %d, %Y %H:%M'), end_time.strftime('%B %d, %Y %H:%M')

def get_prediction_url(lat, lon):
    """Constructs the SondeHub prediction URL."""
    return (f"{BASE_URL}?launch_datetime=now&launch_latitude={lat}&launch_longitude={lon}"
            f"&launch_altitude=0&ascent_rate={ASCENT_RATE}&profile={PROFILE}"
            f"&prediction_type={PREDICTION_TYPE}&burst_altitude={BURST_ALTITUDE}&descent_rate={DESCENT_RATE}")

def capture_screenshot(url, filename):
    """Captures a screenshot of the given URL using Selenium."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)
    time.sleep(90)  # Wait for page to load
    driver.save_screenshot(filename)
    driver.quit()



async def send_prediction():
    """Fetches the prediction image and sends it to Discord."""
    client = discord.Client(intents=discord.Intents.default())

    @client.event
    async def on_ready():
        channel = client.get_channel(CHANNEL_ID)
        if channel:
            await channel.send("Good morning everyone! ☀️ Here are today's launch predictions:")
            start_time, end_time = get_prediction_times()
            await channel.send(f"Prediction range: **{start_time}** EST (black dot) to **{end_time}** EST (red dot)")
            #await channel.send("Note: the black dots represent sooner dates and the red ones ")
            for idx, loc in enumerate(LOCATIONS):
                url = get_prediction_url(loc['lat'], loc['lon'])
                filename = f"prediction_{idx}.png"
                capture_screenshot(url, filename)

                with open(filename, "rb") as file:
                    await channel.send(f"Prediction for {loc['name']}:\n{url}", file=discord.File(file, filename))
        await client.close()

    await client.start(DISCORD_TOKEN)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_prediction())
