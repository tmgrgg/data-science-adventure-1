from selenium import webdriver
#from bs4 import BeautifulSoup # For HTML parsing
from time import sleep # To prevent overwhelming the server between connections
from collections import Counter # Keep track of our term counts
from nltk.corpus import stopwords # Filter out stopwords, such as 'the', 'or', 'and'
import pandas as pd # For converting results to a dataframe and bar chart plots
from selenium.webdriver.common import action_chains, keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
import pickle
import re
import csv
import os.path
from os import walk
#from collections import OrderedDict
import warnings
import random

from OurHelper import load_obj, save_obj, init_driver, searchJobs,\
string_from_text

warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

def build_csv_tom(pickle_obj): ####&&&&
    job_city_info = pickle_obj.replace('glassDoorDict', '')
    my_dict = load_obj(pickle_obj)
    csv_filename = f'jobcsv{job_city_info}.csv'
    if os.path.isfile(csv_filename):
        print('File already exists! Please rename it.')
        return
    with open(csv_filename, 'w') as f:  # Just use 'w' mode in 3.x
        fieldnames = ['job_id','rating', 'position', 'company', 'job_city', 'job_state_code',\
                 'sal_low', 'sal_high', 'sector', 'industry', 'size_small', 'size_big', 'link',]
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()

        for k,v in my_dict.items():
                new_dict = {}
                new_dict['job_id'] = k
                new_dict['rating'] = v['rating']
                new_dict['position'] = v['position']
                new_dict['company'] = v['company']
                new_dict['job_city'] = v['job_city']
                new_dict['job_state_code'] = v['job_state_code']
                new_dict['sal_low'] = v['sal_low']
                new_dict['sal_high'] = v['sal_high']
                new_dict['sector'] = v['sector']
                new_dict['industry'] = v['industry']
                new_dict['size_small'] = v['size_small']
                new_dict['size_large'] = v['size_big']

                writer.writerow(new_dict)
                
def get_pause():
    return random.uniform(0.1, 0.3)

def wait():
    sleep(get_pause())



    
    