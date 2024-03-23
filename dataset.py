import os
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from pathlib import Path
from logger import logger
    
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
    
    return font_paths

def create_document(text, font_path, font_size=16, output_path='dataset'):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    image = Image.new("RGB", (800, 200), color="white")
    draw = ImageDraw.Draw(image)
    
    try:
        
        font = ImageFont.truetype(font_path, font_size)
        draw.text((5, 5), text, fill="black", font=font, language="en")
        
    except OSError as ose:
        logger.error(f"exception:{OSError.__name__} - message:{ose} - font:{os.path.basename(font_path)}")
        
    image_path = os.path.join(output_path, f"{Path(font_path).stem}_{font_size}.png")
    image.save(image_path)
    
    logger.info(f"Document {os.path.basename(image_path)} created successfully")

def main():
    text_sample = """
        If you cannot measure it, you cannot improve it.
        When you can measure what you are speaking about, and express it in numbers,
        you know something about it; but when you cannot measure it, when you cannot
        express it in numbers, your knowledge is of a meagre and unsatisfactory kind.
    """
    fonts = get_fonts('/usr/share/fonts', 'ttf')
    
    for font_path in fonts:
        create_document(text_sample, font_path)

if __name__ == '__main__':
    main()