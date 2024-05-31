from pathlib import Path
from logger import logger
import itertools
from fontTools.ttLib import TTFont
from tqdm import tqdm

from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import reportlab.pdfbase.ttfonts
import reportlab.rl_config

from wand.image import Image as WandImage
from wand.color import Color

import os
import sys

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
    
def get_files(path, extension='ttf'):
    """
    This is an auxiliar method.
    It returns all <extension> type files paths from <path>, including subfolders.
    
    :param path: The directory path to search for files.
    :param extension: The file extension of the files to search for.
    :return: A list of file paths.
    
    For example: get_files('/usr/share/fonts', 'ttf') get all truetype fonts
    from that ubuntu-based default font path. 
    """
    file_paths = []

    for root, _, files in os.walk(path):
        for file in files:
            if file.lower().endswith(f".{extension}"):
                file_paths.append(os.path.join(root, file))
    
    if not file_paths:
        logger.debug(f"No {extension} files found in {path}.")
        
    return file_paths

def register_font_reportlab(font_path):
    try:
        ttf_font = reportlab.pdfbase.ttfonts.TTFont(Path(font_path).stem, os.path.basename(font_path))
        pdfmetrics.registerFont(ttf_font) # registering font on reportlab
    except Exception as e:
        logger.error(f"Error registering font {Path(font_path).stem} on ReportLab: {e}")


def create_document(text, font_path, font_size=16, output_path='dataset', underlined=False):
    if underlined:
        text = '<u>' + text + '</u>'
        pdf_path = os.path.join(output_path, f"(underlined){Path(font_path).stem}_{font_size}.pdf")
    
    elif 'bold' in Path(font_path).stem.lower():
        pdf_path = os.path.join(output_path, f"(bold){Path(font_path).stem}_{font_size}.pdf")
        
    else:
        pdf_path = os.path.join(output_path, f"{Path(font_path).stem}_{font_size}.pdf")

    if os.path.exists(pdf_path):
        logger.info(f"{Path(pdf_path).stem} already exists.")
        return
    
            
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    styles = getSampleStyleSheet()
    styleN = styles['Normal']

    styleN.fontName = Path(font_path).stem
    styleN.fontSize = font_size
    styleN.leading = font_size

    try:
        doc = SimpleDocTemplate(
            pdf_path,
            pagesize=A4,
            bottomMargin=.4 * inch,
            topMargin=.6 * inch,
            rightMargin=.8 * inch,
            leftMargin=.8 * inch)
        P = Paragraph(text, styleN)
        
        doc.build([P])
        logger.debug(f"Document {os.path.basename(pdf_path)} created successfully")

    except Exception as e:
        logger.error(f"Error writing document with font '{os.path.basename(font_path)}': {e}")
        print(f"Error writing document with font '{os.path.basename(font_path)}': {e}")

def create_image(doc_path, output_path):
    # Check if the output directory exists, create it if not
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Open the PDF file
    with WandImage(filename=doc_path, resolution=300) as img:
        # Set the background color to white
        img.background_color = Color("white")
        # Set the resolution to 300dpi
        img.resolution = (300, 300)
        # Remove transparency and replace with bg
        img.alpha_channel = 'remove'
        # Convert PDF to PNG
        img.format = 'png'
        # Save the PNG with the same name as the PDF in the output directory
        img.save(filename=os.path.join(output_path, os.path.basename(doc_path)[:-4] + '.png'))

def main():
    
    with open(os.path.join('sample.txt'), 'r') as file:
        text_sample = file.read()

    font_path = sys.argv[1]
    reportlab.rl_config.TTFSearchPath.append(font_path) 
    
    fonts = get_files(font_path, 'ttf')
    font_sizes = [10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34]
    font_corpus = list(itertools.product(fonts, font_sizes))

    document_progress_bar = tqdm(total=len(font_corpus), desc='Creating documents', unit='document')
    for font_path, font_size in font_corpus:
        register_font_reportlab(font_path)
        
        dir_components = font_path.split(os.sep)
        vox_atypl = dir_components[-2]
        
        create_document(text=text_sample, 
                        font_path=font_path, 
                        font_size=font_size, 
                        output_path=os.path.join('dataset', 'pdf', vox_atypl))
        
        create_document(text=text_sample, 
                        font_path=font_path, 
                        font_size=font_size, 
                        output_path=os.path.join('dataset', 'pdf', vox_atypl),
                        underlined=True)
        
        document_progress_bar.update(1)
    document_progress_bar.close()
    
    
    documents = get_files(os.path.join('dataset', 'pdf'), extension='pdf')
    image_progress_bar = tqdm(total=len(documents), desc='Creating images', unit='images')
    for document in documents:
        
        dir_components = document.split(os.sep)
        vox_atypl = dir_components[-2]
        
        create_image(document, os.path.join('dataset', 'image', vox_atypl))
        image_progress_bar.update(1)
    image_progress_bar.close()
    
    
if __name__ == '__main__':
    main()
