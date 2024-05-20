import pytesseract
from PIL import Image
import os
from dataset import create_document, create_image
import reportlab
from pathlib import Path
from reportlab.pdfbase import pdfmetrics

image_path = os.path.join('dataset', 'image', 'scripts', 'balzac_22.png')
input_image = Image.open(image_path)    

extracted_text = pytesseract.image_to_string(input_image)

with open(os.path.join('sample.txt'), 'r') as file:
        text_sample = file.read()
        

font_path = os.path.join('dataset', 'fonts', 'VoxATypl simple', 'humanistic', 'Centaur-Regular.ttf')
reportlab.rl_config.TTFSearchPath.append(os.path.join('dataset', 'fonts', 'VoxATypl simple'))

ttf_font = reportlab.pdfbase.ttfonts.TTFont(Path(font_path).stem, font_path)
pdfmetrics.registerFont(ttf_font)

create_document(text=extracted_text, 
                        font_path=font_path, 
                        font_size=16, 
                        output_path=os.path.join('sandbox', 'pdf'))

create_image(doc_path=os.path.join('sandbox', 'pdf', 'Centaur-Regular_16.pdf'),
        output_path=os.path.join('sandbox', 'image'))
