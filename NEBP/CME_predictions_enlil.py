# -*- coding: utf-8 -*-
"""
Created on Fri Mar 14 21:18:35 2025

@author: joahb
"""
import os
import requests
import json
import asyncio
from PIL import Image
from io import BytesIO
import discord
from discord.ext import tasks

# Discord bot token and channel ID
DISCORD_TOKEN = ""
CHANNEL_ID = 1103344896162668720

# NOAA data URLs
ENLIL_JSON_URL = "https://services.swpc.noaa.gov/products/animations/enlil.json"
FORECAST_TEXT_URL = "https://services.swpc.noaa.gov/text/3-day-forecast.txt"
BASE_URL = "https://services.swpc.noaa.gov"

# Fetch image URLs from the JSON file
async def fetch_image_urls():
    response = requests.get(ENLIL_JSON_URL)
    if response.status_code == 200:
        json_data = response.json()
        image_urls = [BASE_URL + item['url'] for item in json_data]
        return image_urls[:80]  # Limiting to the first 80 images for faster processing
    return []

# Download a single image from a URL
async def download_image(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            return img
        else:
            print(f"Failed to download image: {url}")
    except Exception as e:
        print(f"Error downloading image {url}: {e}")
    return None

# Download images asynchronously
async def download_images(image_urls):
    tasks = [download_image(url) for url in image_urls]
    images = await asyncio.gather(*tasks)
    return [img for img in images if img is not None]

# Create a GIF from the images
async def create_gif(images):
    if images:
        gif_path = "cme_forecast.gif"
        images[0].save(gif_path, save_all=True, append_images=images[1:], duration=200, loop=0)
        return gif_path
    return None

# Fetch the 3-day forecast text file
async def fetch_text_forecast():
    response = requests.get(FORECAST_TEXT_URL)
    if response.status_code == 200:
        with open("3-day-forecast.txt", "w", encoding="utf-8") as file:
            file.write(response.text)
        return "3-day-forecast.txt"
    return None

# Send the forecast and GIF to Discord
async def send_forecast():
    client = discord.Client(intents=discord.Intents.default())

    @client.event
    async def on_ready():
        channel = client.get_channel(CHANNEL_ID)
        if channel:
            await channel.send("Good morning everyone! ☀️ Here is today's space weather forecast:")

            # Fetch and send the 3-day forecast text file
            forecast_file = await fetch_text_forecast()
            if forecast_file:
                with open(forecast_file, "rb") as file:
                    await channel.send("Here is the latest 3-day forecast:", file=discord.File(file, forecast_file))
            else:
                await channel.send("Failed to fetch the 3-day forecast.")

            # Fetch image URLs and download images asynchronously
            image_urls = await fetch_image_urls()
            if image_urls:
                images = await download_images(image_urls)
                gif_file = await create_gif(images)

                if gif_file:
                    with open(gif_file, "rb") as file:
                        await channel.send("Here is the CME forecast animation:", file=discord.File(file, gif_file))
                else:
                    await channel.send("Failed to create a GIF from the images.")
            else:
                await channel.send("Failed to fetch the images.")

        await client.close()

    await client.start(DISCORD_TOKEN)

# Run the send_forecast function
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_forecast())
