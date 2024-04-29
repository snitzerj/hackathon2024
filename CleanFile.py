import re
class CleanFile:
    
    def __init__(self, filepath):
        pattern = r'\s+'
        self.filepath = filepath
        try:
            with open(filepath) as file:
                    file_contents = file.read()
                    file_contents =  file_contents.rstrip('/r/n/0/t/f/v')
                    self.file_contents = re.sub(pattern, ' ', file_contents)
        except UnicodeDecodeError:
            self.file_contents = ''




