import os

def create_folder(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)



create_folder('pdf/')