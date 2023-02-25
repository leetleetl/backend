import os


def read_file(path1):
    filelist1 = os.listdir(path1)
    file_image = [file for file in filelist1 if file.endswith('.png')]
    return file_image


path = "pythonProject2/predict/w"
print(read_file(path))
