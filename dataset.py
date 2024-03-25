import os
import sys
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from pathlib import Path
from logger import logger
from fontTools.ttLib import TTFont
import itertools
    
def supports_latin_alphabet(font_path):
    try:
        font = TTFont(font_path)
        cmap = font.getBestCmap() or []
        latin_chars = [chr(i) for i in range(0x0020, 0x007F)]  # Basic Latin characters
        for char in latin_chars:
            if ord(char) not in cmap:
                return False
        return True
    except Exception as e:
        logger.error(f"Error analyzing font '{font_path}': {e}")
        print(f"Error analyzing font '{font_path}': {e}")
        return False
    
def get_fonts(path, extension='ttf'):
    """
    This is an auxiliar method.
    It returns all <extension> type fonts paths from <path>, including subfolders.
    
    :param path: The directory path to search for fonts.
    :param extension: The file extension of the fonts to search for.
    :return: A list of file paths to fonts.
    
    For example: get_fonts('/usr/share/fonts', 'ttf') get all truetype fonts
    from that ubuntu-based default font path. 
    """
    font_paths = []

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(f".{extension}"):
                font_paths.append(os.path.join(root, file))
    
    if not font_paths:
        logger.debug('No fonts found.')
        
    return font_paths

def create_document(text, font_path, font_size=16, output_path='dataset'):
    if not supports_latin_alphabet(font_path):
        logger.info(f"{os.path.basename(font_path)} does not support latin alphabet.")
        return
            
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    image = Image.new("RGB", (1300, 400), color="white")
    draw = ImageDraw.Draw(image)
    
    try:
        
        font = ImageFont.truetype(font_path, font_size)
        draw.text((5, 5), text, fill="black", font=font, language="en")
        
    except OSError as ose:
        logger.error(f"Error writing document with font '{os.path.basename(font_path)}': {ose}")
        print(f"Error writing document with font '{os.path.basename(font_path)}': {ose}")
        
    image_path = os.path.join(output_path, f"{Path(font_path).stem}_{font_size}.png")
    image.save(image_path)
    
    logger.debug(f"Document {os.path.basename(image_path)} created successfully")

def main():
    
    with open(os.path.join('sample.txt'), 'r') as file:
        text_sample = file.read()

    font_path = sys.argv[1]
    
    fonts = get_fonts(font_path, 'ttf')
    font_sizes = [12, 14, 16, 18, 20, 22]
    for font_path, font_size in itertools.product(fonts, font_sizes):
        create_document(text_sample, font_path, font_size)

if __name__ == '__main__':
    main()
