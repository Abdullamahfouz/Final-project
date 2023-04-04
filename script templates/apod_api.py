'''
Library for interacting with NASA's Astronomy Picture of the Day API.
'''

import requests


key = '0Q7g3afMUT7qvSLWqQ7P6IyLbjXzVN4Ju6c8vgRt'


def main():
    
    apod_info = get_apod_info('2022-08-08')
    print(apod_info)
    
    return

def get_apod_info(apod_date):
    """Gets information from the NASA API for the Astronomy 
    Picture of the Day (APOD) from a specified date.
    Args:
        apod_date (date): APOD date (Can also be a string formatted as YYYY-MM-DD)
    Returns:
        dict: Dictionary of APOD info, if successful. None if unsuccessful
    """
    apod_info = {'api_key': key, 'date': apod_date}
    params=apod_info
    req = requests.get('https://api.nasa.gov/planetary/apod', params)

    if req.status_code == 200:
        return req.json()

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
    # retutns the type of media
    return
   

if __name__ == '__main__':
    main()