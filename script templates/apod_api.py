'''
Library for interacting with NASA's Astronomy Picture of the Day API.
'''

import requests
import os
import hashlib
import sqlite3
import argparse
from datetime import date

# Define the NASA APOD API endpoint URL
NASA_APOD_API_URL = 'https://api.nasa.gov/planetary/apod'

# Define the path to the SQLite database
DB_PATH = 'apod.db'

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Download and set NASA APOD image as desktop background')
    parser.add_argument('date', metavar='date', type=str, help='APOD date in the format YYYY-MM-DD')
    args = parser.parse_args()

    # Get APOD info for specified date
    apod_info = get_apod_info(args.date)
    
    if apod_info is None:
        print('Unable to retrieve APOD info.')
        return
    
    # Get the APOD image URL
    apod_image_url = get_apod_image_url(apod_info)
    
    if apod_image_url is None:
        print('Unable to retrieve APOD image URL.')
        return
    
    # Download the APOD image
    image_path = download_apod_image(apod_image_url)
    
    if image_path is None:
        print('Unable to download APOD image.')
        return
    
    # Set the APOD image as the desktop background
    set_desktop_background(image_path)
    
    # Store the APOD info in the database
    store_apod_info(apod_info, image_path)
    
    print('APOD downloaded and set as desktop background successfully.')

def get_apod_info(apod_date, api_key):
    """Gets information from the NASA API for the Astronomy 
    Picture of the Day (APOD) from a specified date.

    Args:
        apod_date (date): APOD date (Can also be a string formatted as YYYY-MM-DD)
        api_key (str): NASA API developer key

    Returns:
        dict: Dictionary of APOD info, if successful. None if unsuccessful
    """
    url = f'https://api.nasa.gov/planetary/apod?api_key={api_key}&date={apod_date}'
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return None
def get_apod_image_url(apod_info_dict):
    """Gets the URL of the APOD image from the dictionary of APOD information.

    If the APOD is an image, gets the URL of the high definition image.
    If the APOD is a video, gets the URL of the video thumbnail.

    Args:
        apod_info_dict (dict): Dictionary of APOD info from API

    Returns:
        str: APOD image URL
    """
    media_type = apod_info_dict['media_type']
    
    if media_type == 'image':
        return apod_info_dict['hdurl']
    elif media_type == 'video':
        return apod_info_dict['thumbnail_url']
    else:
        return None

def download_apod_image(image_url):
    """Downloads the APOD image from the specified URL and saves it to disk.

    Returns:
        str: File path of the downloaded image, if successful. None if unsuccessful
    """
    response = requests.get(image_url)
    
    if response.status_code == 200:
        # Compute the MD5 hash of the image content
        image_hash = hashlib.md5(response.content).hexdigest()