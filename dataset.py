import os
    
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

def main():
    text_sample = """
        If you cannot measure it, you cannot improve it.
        When you can measure what you are speaking about, and express it in numbers,
        you know something about it; but when you cannot measure it, when you cannot
        express it in numbers, your knowledge is of a meagre and unsatisfactory kind.
    """
    fonts = get_fonts('/usr/share/fonts', 'ttf')
    

if __name__ == '__main__':
    main()