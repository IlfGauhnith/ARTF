# ARTF - Analysing OCRs performance on different fonts
### How to run

```
pip install -r requirements.txt
```
```
python dataset.py <fonts_path>
```
```dataset.py``` generates the dataset in ./dataset.  
```<fonts_path>```: path containing fonts .ttf that will be used to generate the dataset.  
For example: ```python dataset.py '/usr/share/fonts'``` uses fonts from my ubuntu-based default font path.
