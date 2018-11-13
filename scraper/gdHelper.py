from selenium import webdriver
#from bs4 import BeautifulSoup # For HTML parsing
from time import sleep # To prevent overwhelming the server between connections
import pickle
import csv
import os
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
    browser = webdriver.Chrome(executable_path=os.getcwd() + '/chromedriver', chrome_options=chrome_options)
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
                
def build_csv(job_title, location):
    job_dict = load_obj(get_pkl_path(job_title, location))
    print(len(job_dict))
    csv_filename = 'data/csv/{}_{}.csv'.format(job_title.lower(), location.lower())
    if os.path.isfile(csv_filename):
        print("csv file exists - delete and try again")
        return
    with open(csv_filename, 'w') as f:
        fieldnames = ['job_id','rating', 'position', 'company', 'job_city', 'location_search', 'job_state_code',\
                 'sal_low', 'sal_est', 'sal_high', 'industry', 'sector', 'size_small', 'size_large']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for k,v in job_dict.items():
            d = {}
            d['job_id']= k
            d.update(v)
            print(d)
            
            writer.writerow(d)
            
#make pauses seem difficult to predict
def get_pause():
    c = 0.3
    seq = [0, 1, 2, 3, 3.5]
    rand = random.choice(seq)
    
    if (rand <= 2):
        return random.uniform(1.4, 2.7)*c
    else:
        return random.uniform(rand - 1, rand*1.5)*c

def wait():
    pause = get_pause()
    print('waiting for' + str(pause) + ' seconds')
    sleep(pause)

# Grab data stored in pkl - if none is present then create pkl storage files.        
def unpickle(job_title, location):
    try:    
        job_dict = load_obj(get_pkl_path(job_title, location))
    except:
        save_obj({}, get_pkl_path(job_title, location))
        job_dict = load_obj(get_pkl_path(job_title, location))

    print('len(job_dict) = '+str(len(job_dict)))
    
    return job_dict


    
    