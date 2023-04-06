'''
Library for interacting with NASA's Astronomy Picture of the Day API.
'''

import requests


api_key = '0Q7g3afMUT7qvSLWqQ7P6IyLbjXzVN4Ju6c8vgRt'
url = 'https://api.nasa.gov/planetary/apod'

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
    params = {'api_key': api_key, 
              'date': apod_date
              }
    
    req = requests.get(url, params)

    if req.status_code == 200:
        return req.json()
    else:
        print('failure')

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
    
    
     
    return None


if __name__ == '__main__':
    main()