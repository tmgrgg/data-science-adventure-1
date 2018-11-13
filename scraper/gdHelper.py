from selenium import webdriver
#from bs4 import BeautifulSoup # For HTML parsing
from time import sleep # To prevent overwhelming the server between connections
import pickle
import csv
import os.path
#from collections import OrderedDict
import warnings
import random

warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

def init_driver():
    ''' Initialize chrome driver'''

    chrome_options = webdriver.ChromeOptions()

    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--profile-directory=Default')
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-plugins-discovery")
    chrome_options.add_argument("--start-maximized")
    #browser = webdriver.Chrome(driver, chrome_options=chrome_options)
    browser = webdriver.Chrome(executable_path='/Users/griggles/Documents/FLATIRON/PROJECT_1/data-science-adventure-1/scraper/chromedriver'
, chrome_options=chrome_options)
    #browser = webdriver.Chrome()

    return browser

##############################################################################

def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

###############################################################################

def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)
    
def get_pkl_path(job_title, location):
    return 'data/pkl/glassDoorDict_' + job_title.lower() + '_' + location.lower()

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
                
def build_csv(job_title, location):
    job_dict = load_obj(get_pkl_path(job_title, location))
    print(len(job_dict))
    csv_filename = 'data/csv/{}_{}.csv'.format(job_title.lower(), location.lower())
    if os.path.isfile(csv_filename):
        print("csv file exists - delete and try again")
        return
    with open(csv_filename, 'w') as f:
        fieldnames = ['job_id','rating', 'position', 'company', 'job_city', 'job_state_code',\
                 'sal_low', 'sal_high', 'industry', 'sector', 'size_small', 'size_large']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for k,v in job_dict.items():
            d = {}
            d['job_id']= k
            d.update(v)
            print(d)
            
            writer.writerow(d)
                
def get_pause():
    return random.uniform(0.1, 0.3)

def wait():
    sleep(get_pause())

# Grab data stored in pkl - if none is present then create pkl storage files.        
def unpickle(job_title, location):
    try:    
        job_dict = load_obj(get_pkl_path(job_title, location))
    except:
        save_obj({}, get_pkl_path(job_title, location))
        job_dict = load_obj(get_pkl_path(job_title, location))

    print('len(job_dict) = '+str(len(job_dict)))
    
    return job_dict


    
    