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

    for root, _, files in os.walk(path):
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

    styles = getSampleStyleSheet()
    styleN = styles['Normal']

    styleN.fontName = Path(font_path).stem
    styleN.fontSize = font_size
    styleN.leading = font_size

    pdf_path = os.path.join(output_path, f"{Path(font_path).stem}_{font_size}.pdf")

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

def main():
    
    with open(os.path.join('sample.txt'), 'r') as file:
        text_sample = file.read()

    font_path = sys.argv[1]
    reportlab.rl_config.TTFSearchpath = font_path

    fonts = get_fonts(font_path, 'ttf')
    font_sizes = [12, 14, 16, 18, 20, 22, 24, 26]
    font_corpus = list(itertools.product(fonts, font_sizes))

    progress_bar = tqdm(total=len(font_corpus), desc='Creating documents', unit='document')
    for font_path, font_size in font_corpus:

        ttf_font = reportlab.pdfbase.ttfonts.TTFont(Path(font_path).stem, os.path.basename(font_path))
        pdfmetrics.registerFont(ttf_font) # registering font on reportlab

        create_document(text=text_sample, 
                        font_path=font_path, 
                        font_size=font_size, 
                        output_path=os.path.join('dataset', 'pdf'))
        progress_bar.update(1)

if __name__ == '__main__':
    main()
