
from fnmatch import fnmatchcase

from setuptools import find_namespace_packages

def process_multi_img(set):
    global multi 
    multi = set

def is_multi():
    return multi

def set_file_name(filename):
    global file_name
    file_name = filename

def get_file_name():
    return file_name


output_path = "C:\\Users\\user\\Desktop\\Project\\segmentor\\outputs"
char_path = "C:\\Users\\user\\Desktop\\Project\\segmentor\\characters"