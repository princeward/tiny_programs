from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
import os

import argparse

def download_jpg_urls(url, download_path):
    """
    Download JPG files from a webpage to a local path.

    Args:
        url (str): URL of the webpage.
        download_path (str): Local path to download the JPG files.
    """
    # Set up ChromeDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Navigate to the webpage
    driver.get(url)

    # Get the HTML content
    html_content = driver.page_source

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all img tags with a src attribute containing .jpg
    jpg_imgs = soup.find_all('img', src=lambda x: x and x.endswith('.jpg'))

    # Extract the src attribute (URL) from each img tag
    jpg_urls = [img['src'] for img in jpg_imgs]

    # Close the browser window
    driver.quit()

    # # Create the download directory if it doesn't exist
    # if not os.path.exists(download_path):
    #     os.makedirs(download_path)

    # Download each JPG file
    for url in jpg_urls:
        url = "https://"+url[2:]
        print("url: ", url)
        filename = url.split("/")[-1]
        file_path = os.path.join(download_path, filename)

        print("file_path: ", file_path)

        response = requests.get(url)
        if response.status_code == 200:
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded {filename}")
        else:
            print(f"Failed to download {filename}")

# Example usage:
# url = "https://triolensphotographystudio.pixieset.com/eva/?pid=13871780838&id=1&h=MTcwMTY4MjIwMw"
# download_path = "/home/zijian/Downloads/maternity_photo/"
# download_jpg_urls(url, download_path)



print("hello")
parser = argparse.ArgumentParser(description="Download JPG files from a webpage")
parser.add_argument("-o", "--output", help="Output directory", default="/home/zijian/Downloads/maternity_photo/")
url = input("Enter the URL of the webpage: ")
args = parser.parse_args()

download_jpg_urls(url, args.output)