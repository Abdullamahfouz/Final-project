""" 
COMP 593 - Final Project

Description: 
  Downloads NASA's Astronomy Picture of the Day (APOD) from a specified date
  and sets it as the desktop background image.

Usage:
  python apod_desktop.py [apod_date]

Parameters:
  apod_date = APOD date (format: YYYY-MM-DD)
"""
from datetime import date
import os
import image_lib
import inspect
import sys
import hashlib
import requests
import sqlite3
from apod_api import get_apod_image_url
import apod_api


# Global variables
image_cache_dir = None  # Full path of image cache directory
image_cache_db = None   # Full path of image cache database

def main():
    ## DO NOT CHANGE THIS FUNCTION ##
    # Get the APOD date from the command line
    apod_date = get_apod_date()    
    

    # Get the path of the directory in which this script resides
    script_dir = get_script_dir()

    # Initialize the image cache
    init_apod_cache(script_dir)

    # Add the APOD for the specified date to the cache
    apod_id = add_apod_to_cache(apod_date)

    # Get the information for the APOD from the DB
    apod_info = get_apod_info(apod_id)

    # Set the APOD as the desktop background image
    if apod_id != 0:
        image_lib.set_desktop_background_image(apod_info['file_path'])

def get_apod_date():
    """Gets the APOD date
     
    The APOD date is taken from the first command line parameter.
    Validates that the command line parameter specifies a valid APOD date.
    Prints an error message and exits script if the date is invalid.
    Uses today's date if no date is provided on the command line.

    Returns:
        date: APOD date
    """
    # checks if there are more than one command-line arguments 
    if len(sys.argv) > 1:
         # tries to covert the agrs into a date 
        try:
            apod_date = date.fromisoformat(sys.argv[1])
        # exception ERROR if  the format is incorrect 
        except ValueError:
            print(f"Error: Invalid date format: {sys.argv[1]}. PLEASE use this format (YYYY-MM-DD).")
            sys.exit(1)
    # if no date provided just uses today's date 
    else:
        apod_date = date.today()
     # if the date in the future 
    if apod_date > date.today():
        print(f"Error: Date {apod_date.isoformat()} is in the future.")
        sys.exit(1)
        
    return apod_date

def get_script_dir():
    """Determines the path of the directory in which this script resides

    Returns:
        str: Full path of the directory in which this script resides
    """
    ## DO NOT CHANGE THIS FUNCTION ##
    script_path = os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename)
    return os.path.dirname(script_path)

def init_apod_cache(parent_dir):
    """Initializes the image cache by:
    - Determining the paths of the image cache directory and database,
    - Creating the image cache directory if it does not already exist,
    - Creating the image cache database if it does not already exist.
    
    The image cache directory is a subdirectory of the specified parent directory.
    The image cache database is a sqlite database located in the image cache directory.

    Args:
        parent_dir (str): Full path of parent directory    
    """
    #  will store the paths to the image cache directory and database
    global image_cache_dir
    global image_cache_db
   # creates the path for the image cache directory joining the parent dircetory with the subdirectory  
    image_cache_dir = os.path.join(parent_dir, 'image_cache')
   #   checks if the image_cache_dir does not exist. If it doesn't, 
   # the directory is created using the os.makedirs() function.   
    if not os.path.exists(image_cache_dir):
        os.makedirs(image_cache_dir)
        print(f'Image cache directory: {image_cache_dir}')
        print('Image cache directory created.')
     # creates the path for the image cache database  by 
     # joining the image_cache_dir with the database file 
    else:
        print(f'Image cache directory: {image_cache_dir}')
        print('Image cache directory Already exists.')
     # creates the path for the image cache database  by 
     # joining the image_cache_dir with the database file 
    image_cache_db = os.path.join(image_cache_dir, 'image_cache.db')
    
    # checks if the file does not already exist
    if not os.path.exists(image_cache_db) :
        # If the database file does not exist, creates a SQLite database by creating 
        # a new file named 'apod_cache.db' in the image Dir .
        con = sqlite3.connect(image_cache_db)
        # creats the new file named 'named 'apod_cache.db 
        cur = con.cursor()
       # create a new table named 'apod' in the database. 
        query = """
            CREATE TABLE IF NOT EXISTS image_apod
            (
               id    INTEGER PRIMARY KEY,
               title TEXT NOT NULL,
               explanation TEXT NOT NULL,
               file_path TEXT NOT NULL,
               sha256 TEXT NOT NULL 
            );
        """ 
        #  executes an SQL command for the database above
        cur.execute(query)
        # saving the changes made to the database
        con.commit()
        # closes the connection to the SQLite database
        con.close()
        print(f'Image cache DB created: {image_cache_db}')
        print('Image cache DB created.')
    else:
        print(f'Image cache DB created: {image_cache_db}')
        print('Image cache DB Already exists')
        
def add_apod_to_cache(apod_date):
    """Adds the APOD image from a specified date to the image cache.
     
    The APOD information and image file is downloaded from the NASA API.
    If the APOD is not already in the DB, the image file is saved to the 
    image cache and the APOD information is added to the image cache DB.

    Args:
        apod_date (date): Date of the APOD image

    Returns:
        int: Record ID of the APOD in the image cache DB, if a new APOD is added to the
        cache successfully or if the APOD already exists in the cache. Zero, if unsuccessful.
    
    """
    
   # prints APOD date
    print("APOD date:", apod_date.isoformat())
    
    # gets the APOD date 
    apod_info = apod_api.get_apod_info(apod_date)
    print(f'Getting {apod_date} APOD information from NASA...success')
    
    image_title = apod_info['title']
    print(f'Image title: {image_title}')
   
    # gets the APOD image url
    apod_image_url = get_apod_image_url(apod_info)
    print(f'Image url:{apod_image_url}')
    
     # downlods the APOD image 
    image_data = image_lib.download_image(apod_image_url)
    print(f'Downloaded image from {apod_image_url}')
    
    # Checks the APOD SHA-256
    apod_hash = hashlib.sha256(image_data).hexdigest()
    print(f'APOD SHA-256:{apod_hash}')
    
    
    
    
    
    
    
   
    

def add_apod_to_db(title, explanation, file_path, sha256):
    """Adds specified APOD information to the image cache DB.
     
    Args:
        title (str): Title of the APOD image
        explanation (str): Explanation of the APOD image
        file_path (str): Full path of the APOD image file
        sha256 (str): SHA-256 hash value of APOD image

    Returns:
        int: The ID of the newly inserted APOD record, if successful.  Zero, if unsuccessful       
    """
     
    
    
  
    con = sqlite3.connect(image_cache_db)
    cur = con.cursor()
    
    
   
    add_apod_query = """
        INSERT INTO apod_image 
        (
         title, 
         explanation, 
         path, 
         sha256
        )
        VALUES (?, ?, ?, ?);
 """
    
    apod = (title, explanation, file_path, sha256)
    
    cur.execute(add_apod_query, apod)
    
    con.commit()
    con.close()
    return 0

def get_apod_id_from_db(image_sha256):
    """Gets the record ID of the APOD in the cache having a specified SHA-256 hash value
    
    This function can be used to determine whether a specific image exists in the cache.

    Args:
        image_sha256 (str): SHA-256 hash value of APOD image

    Returns:
        int: Record ID of the APOD in the image cache DB, if it exists. Zero, if it does not.
    """
    # TODO: Complete function body
    return 0

def determine_apod_file_path(image_title, image_url):
    """Determines the path at which a newly downloaded APOD image must be 
    saved in the image cache. 
    
    The image file name is constructed as follows:
    - The file extension is taken from the image URL
    - The file name is taken from the image title, where:
        - Leading and trailing spaces are removed
        - Inner spaces are replaced with underscores
        - Characters other than letters, numbers, and underscores are removed

    For example, suppose:
    - The image cache directory path is 'C:\\temp\\APOD'
    - The image URL is 'https://apod.nasa.gov/apod/image/2205/NGC3521LRGBHaAPOD-20.jpg'
    - The image title is ' NGC #3521: Galaxy in a Bubble '

    The image path will be 'C:\\temp\\APOD\\NGC_3521_Galaxy_in_a_Bubble.jpg'

    Args:
        image_title (str): APOD title
        image_url (str): APOD image URL
    
    Returns:
        str: Full path at which the APOD image file must be saved in the image cache directory
    """
    # TODO: Complete function body
    return

def get_apod_info(image_id):
    """Gets the title, explanation, and full path of the APOD having a specified
    ID from the DB.

    Args:
        image_id (int): ID of APOD in the DB

    Returns:
        dict: Dictionary of APOD information
    """
    con = sqlite3.connect(image_cache_db)
    cur = con.cursor()
    
   
    select_apod_query = """ 
      SELECT title, explanation, path FROM apod_image 
      WHERE id = ?
  """
    
    
    
    

def get_all_apod_titles():
    """Gets a list of the titles of all APODs in the image cache

    Returns:
        list: Titles of all images in the cache
    """
    # TODO: Complete function body
    # NOTE: This function is only needed to support the APOD viewer GUI
    return

if __name__ == '__main__':
    main()