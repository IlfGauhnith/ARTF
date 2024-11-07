import os
import tesseract as tes
import google_vision as goov

def tesseract():
    experiment = tes.experiment(os.path.join('dataset', 'Grotesk-Bold'))
    print(experiment)
    tes.create_evaluation_csv(experiment, csv_name='tesseract_grotesque_bold.csv')

def google_vision():
    experiment = goov.experiment(os.path.join('dataset', 'Grotesk-Bold'))
    print(experiment)
    goov.create_evaluation_csv(experiment, csv_name='google_grotesque_bold.csv')
    
if __name__ == '__main__':
    tesseract()
    google_vision()