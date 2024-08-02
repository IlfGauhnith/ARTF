import requests
from bs4 import BeautifulSoup
import os

 
def download_image(url, filename):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded: {filename}")
        else:
            print(f"Failed to download: {url}")
    except Exception as e:
        print(f"Exception occurred while downloading {url}: {e}")


url = "https://learn.microsoft.com/en-us/typography/font-list/"


fonts = ['Impact', 'Imprint MT Shadow', 'Informal Roman', 'Ink Free', 'Jokerman', 'Juice ITC', 
         'Kino MT', 'Kristen ITC', 'Kunstler Script', 'LCD', 'Lucida Blackletter', 'Lucida Bright', 
         'Lucida Calligraphy', 'Lucida Console', 'Lucida Fax', 'Lucida Handwriting', 'Lucida Sans', 
         'Lucida Sans Typewriter', 'Magneto', 'Maiandra GD', 'Matisse ITC', 'Matura MT', 'McZee', 'Mead Bold', 
         'Mercurius Script MT Bold', 'Microsoft Sans Serif', 'Minion Web', 'Mistral', 'Modern No. 20', 
         'Monotype Corsiva', 'Myanmar Text', 'Neue Haas Grotesk Text Pro', 'Lucida Blackletter', 'News Gothic MT', 
         'New Caledonia', 'Niagara', 'OCRB', 'OCR A Extended', 'Old English Text MT', 'Onyx', 'Palace Script MT', 
         'Palatino Linotype', 'Papyrus', 'Parade', 'Parchment', 'Peignot Medium', 'Pepita MT', 'Perpetua', 'Perpetua Titling', 
         'Placard Condensed', 'Playbill', 'Poor Richard', 'Pristina', 'Quire Sans', 'Rage Italic', 'Ransom', 'Ravie', 'Rockwell', 
         'Runic MT Condensed', 'Sabon Next LT', 'Sagona', 'Script MT Bold', 'Segoe Print', 'Segoe Script', 'Segoe UI', 'Showcard Gothic', 
         'Sitka', 'Snap ITC', 'Stencil', 'Stop', 'Tahoma', 'Tempo Grunge', 'Tempus Sans ITC', 'The Hand', 'The Serif Hand', 
         'Times New Roman', 'Tisa Offc Serif Pro', 'Tw Cen MT', 'Univers', 'Verdana Pro', 'Viner Hand ITC', 'Vivaldi', 'Vixar ASCI', 
         'Vladimir Script', 'Walbaum', 'Westminster', 'Wide Latin', 'Yu Mincho']


response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

for div in soup.find_all('div', class_='content'):
    links = div.find_all('a')
    
    for link in links:
        
        for searched_fonts in fonts:

            href = link['href'].lower().replace(" ", "").replace("-", "")

            if href in searched_fonts.lower().replace(" ", "").replace("-", ""):
                
                response = requests.get(url + link['href'])
                soup = BeautifulSoup(response.content, 'html.parser')
                main = soup.find('main', {'id': 'main'})

                img = main.find("img")
                download_image(url + img['src'], f"{img['alt'].replace(" ", "_")}.png")

