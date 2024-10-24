import os
import tesseract as tes
import google_vision as goov

def tesseract():
    experiment = tes.experiment(os.path.join('dataset', 'perpetua'))
    print(experiment)
    tes.create_evaluation_csv(experiment, csv_name='tesseract_perpetua.csv')

def google_vision():
    experiment = goov.experiment(os.path.join('dataset', 'perpetua'))
    print(experiment)
    goov.create_evaluation_csv(experiment, csv_name='google_perpetua.csv')
    
if __name__ == '__main__':
    tesseract()
    google_vision()