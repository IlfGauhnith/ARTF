import pytesseract
from PIL import Image
import Levenshtein
import numpy as np
import pandas as pd
import os
from util import exclude_outliers
from pathlib import Path
from tqdm import tqdm

def get_font_style(font_name):
    """
    Returns boolean dictionary indicating font styles based on font_name.
    """
    font_name = font_name.lower()
    
    return {
        'regular': 'regular' in font_name,
        'mono': 'mono' in font_name,
        'black': 'black' in font_name,
        'bold': 'bold' in font_name,
        'italic': 'italic' in font_name,
        'extralight': 'extralight' in font_name,
        'semibold': 'semibold' in font_name,
        'extrabold': 'extrabold' in font_name,
        'thin': 'thin' in font_name,
        'extracondensed': 'extracondensed' in font_name
    }

def create_evaluation_csv(experiment):
    frame = pd.DataFrame(experiment)
    frame.to_csv('experiment.csv', index=False)

def experiment():
    dataset_path = os.path.join('dataset', 'image')
    with open(os.path.join('sample.txt'), 'r') as file:
        ground_truth = file.read()  

    files = os.listdir(dataset_path)
    progress_bar = tqdm(total=len(files), desc='Processing files', unit='file')

    experiment = []
    for filename in files:
        img_path = os.path.join(dataset_path, filename)
        score = ocr_eval(img_path, ground_truth)
        
        font_name = Path(img_path).stem
        font_size = font_name.split("_")[-1]
        
        font_name = ''.join(font_name.split("_")[:-1])
        font_style = get_font_style(font_name)
        
        experiment.append({**{'font_name':font_name, 'accuracy':f"{score:.2f}%", 'font_size': font_size}, **font_style})
        progress_bar.update(1)

    progress_bar.close()
    return experiment
    
def ocr_eval(img_path, ground_truth):
    img = Image.open(img_path)
    
    extracted_text = pytesseract.image_to_string(img)
    dist = Levenshtein.distance(extracted_text, ground_truth)

    score = ((len(ground_truth) - dist) / len(ground_truth)) * 100
    return score

if __name__ == '__main__':
    experiment = experiment()
    create_evaluation_csv(experiment)
