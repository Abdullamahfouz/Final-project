'''
Library for interacting with NASA's Astronomy Picture of the Day API.
'''

import requests


API_KEY = '0Q7g3afMUT7qvSLWqQ7P6IyLbjXzVN4Ju6c8vgRt'
APOD_URL = 'https://api.nasa.gov/planetary/apod'

def main():
    
    apod_info = get_apod_info('1999-08-08')
    print(apod_info)
    image_url = get_apod_image_url(apod_info)
    print("Image URL:", image_url)
    
    
    return None

def get_apod_info(apod_date):
    """Gets information from the NASA API for the Astronomy 
    Picture of the Day (APOD) from a specified date.
    Args:
        apod_date (date): APOD date (Can also be a string formatted as YYYY-MM-DD)
    Returns:
        dict: Dictionary of APOD info, if successful. None if unsuccessful
    """
    image_params = {
     'api_key': API_KEY, 
     'date': apod_date
    }
    
    req = requests.get(APOD_URL, params=image_params)
    
    
    if req.status_code == 200:
        print(f'Getting {apod_date} APOD information from NASA...success')
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
    
    media_type = apod_info_dict['media_type']
    
    # checks the media type
    if media_type == 'image':
        image_url = apod_info_dict['hdurl'] 
        return image_url
    if media_type == 'video':
        image_url = apod_info_dict['thumbnail_url']
        return image_url
    else:
        print('invalid media')
    
    
    
    


if __name__ == '__main__':
    main()