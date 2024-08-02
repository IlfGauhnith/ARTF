import os
from pathlib import Path
from tqdm import tqdm
import pandas as pd
import numpy as np
import Levenshtein
from PIL import Image
from google.cloud import vision

def get_font_style(font_name):
    font_name = font_name.lower()
    
    return {
        'regular': 'regular' in font_name,
        'mono': 'mono' in font_name,
        'black': 'black' in font_name,
        'semibold': 'semibold' in font_name,
        'bold': 'bold' in font_name,
        'extrabold': 'extrabold' in font_name,
        'italic': 'italic' in font_name,
        'light': 'light' in font_name,
        'extralight': 'extralight' in font_name,
        'semibold': 'semibold' in font_name,
        'thin': 'thin' in font_name,
        'medium': 'medium' in font_name,
        'semicondensed': 'semicondensed' in font_name,
        'condensed': 'condensed' in font_name,
        'extracondensed': 'extracondensed' in font_name,
        'compact': 'compact' in font_name,
        'oblique': 'oblique' in font_name
    }

def count_png(path):
    png_count = 0

    for root, dirs, files in os.walk(path):
        for filename in files:
            if filename.lower().endswith(".png"):
                png_count += 1

    return png_count

def create_evaluation_csv(experiment):
    frame = pd.DataFrame(experiment)
    frame.to_csv('google_vision_experiment.csv', index=False)

def experiment():
    dataset_path = os.path.join('dataset', 'image')
    with open(os.path.join('sample.txt'), 'r') as file:
        ground_truth = file.read()  

    vox_atypl_dir = dataset_path
    count = count_png(vox_atypl_dir)
    progress_bar = tqdm(total=count, desc='Processing files', unit='file')

    experiment = []
    
    for root, dirs, files in os.walk(dataset_path):
        for dir in dirs:
            for filename in os.listdir(os.path.join(dataset_path, dir)):
                img_path = os.path.join(dataset_path, dir, filename)
                score = ocr_eval(img_path, ground_truth)
                
                font_name = Path(img_path).stem
                font_name = font_name.replace("(underlined)", "")
                font_name = font_name.replace("(bold)", "")
                
                font_size = font_name.split("_")[-1]
                
                font_name = ''.join(font_name.split("_")[:-1])
                
                experiment.append({'font_name': font_name, 
                                   'accuracy': f"{score:.2f}%", 
                                   'font_size': font_size, 
                                   'vox_atypl': dir, 
                                   'underlined': 'underlined' in Path(img_path).stem,
                                   'bold': 'bold' in Path(img_path).stem
                                   })
                progress_bar.update(1)

    progress_bar.close()
    return experiment
    
def ocr_eval(img_path, ground_truth):
    client = vision.ImageAnnotatorClient()
    
    with open(img_path, 'rb') as image_file:
        content = image_file.read()
    
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    annotations = response.text_annotations
    
    extracted_text = annotations[0].description if annotations else ""
    print(extracted_text)
    dist = Levenshtein.distance(extracted_text, ground_truth)

    score = ((len(ground_truth) - dist) / len(ground_truth)) * 100
    return score

if __name__ == '__main__':
    experiment = experiment()
    create_evaluation_csv(experiment)
