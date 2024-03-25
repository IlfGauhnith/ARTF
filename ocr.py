import pytesseract
from PIL import Image
import Levenshtein
import numpy as np
import pandas as pd
import os
from util import exclude_outliers
from pathlib import Path

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

def experiment(pop:int):
    dataset_path = os.path.join('dataset')
    with open(os.path.join('sample.txt'), 'r') as file:
        ground_truth = file.read()

    experiment = []
    for filename in os.listdir(dataset_path):
        img_path = os.path.join(dataset_path, filename)
        median, std = ocr_eval(img_path, ground_truth, pop)
        
        font_name = Path(img_path).stem
        font_style = get_font_style(font_name)
        
        experiment.append({**{'font_name':font_name, 'median':median, 'std':std}, **font_style})
        break
    
    return experiment
    
def ocr_eval(img_path, ground_truth, pop:int):
    img = Image.open(img_path)
    
    experiment = []
    for _ in range(pop):
        extracted_text = pytesseract.image_to_string(img)
        dist = Levenshtein.distance(extracted_text, ground_truth)
        experiment.append(dist)
        
    exclude_outliers(experiment)
    
    return (np.median(experiment), np.std(experiment))

if __name__ == '__main__':
    experiment = experiment(1)
    create_evaluation_csv(experiment)
