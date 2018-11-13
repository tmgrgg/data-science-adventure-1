import numpy as np
import re
import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
import pdb

from selenium.common.exceptions import NoSuchElementException
from gdHelper import wait, save_obj, init_driver, unpickle, get_pkl_path


#Get rid of pop ups
def handle_popup(browser):
    try:
        browser.find_element_by_xpath('//*[@id="JAModal"]/div/div[2]/div').click() #pop up
    except:
        pass


# Scrape page_count pages of jobs
def enter_search_terms(browser, job_title, location):
    job_field = browser.find_element_by_id("KeywordSearch")
    location_field = browser.find_element_by_id("LocationSearch") 
    
    wait()
    
    job_field.send_keys(job_title)  #enter job_title into searchbox
    
    wait() 
    
    location_field.clear() #clear location form (already populated)
   
    location_field.send_keys(location) #enter ocation into searchbox
    
    wait()    

    browser.find_element_by_class_name('gd-btn-mkt').click()

    wait()
    
def scrape_pages(browser, page_count, job_dict, job_title, location):
    for i in range(page_count):
        job_list =browser.find_elements_by_class_name('jl')
        
        wait()

        #create a list of (unique job_id, Selenium WebElement repr. job)
        job_tuples = map(lambda job: (job.get_attribute('data-id'), job), job_list)

        #filter job ids that are already in job_dict (avoid reprocessing)
        job_tuples = list(filter(lambda j: j[0] not in job_dict.keys(),job_tuples)) 
        
        print(len(job_list))
        print(len(job_tuples))
        
        wait()
        
        #each job scraped in a new tab
        for job in job_tuples:
            info_link = job[1].find_element_by_tag_name('a').get_attribute('href')
            job_info = scrape_job(browser, job[1].text, info_link, location)
            job_dict[job[0]] = job_info
            save_obj(job_dict, get_pkl_path(job_title, location))

        #browser should be back in the original window here
        next_page_btn = browser.find_element_by_class_name('next')
        next_page_btn.click()
        
        
        #get rid of popups
        handle_popup(browser)
        
        wait()
        
    browser.close()

def scrape_job(browser, job_text, info_link, location):
    #open and switch to a new tab
    browser.execute_script("window.open('" + info_link + "');")    
    browser.switch_to_window(browser.window_handles[1])
       
    job_attributes = parse_job(browser, job_text, location)
    
    wait()
    
    #close tab and switch back
    browser.close()
    browser.switch_to_window(browser.window_handles[0])
    return job_attributes


#Turn a selenium web_element into required job info
def parse_job(browser, job_text, location_search):
    raw_rating = re.findall('\d\.\d', job_text)
    print(raw_rating)
    if len(raw_rating) == 1:
        rating = raw_rating[0]
    else:
        rating = ''
    raw_sal_range = re.findall('\d+k', job_text)
    print('raw_sal_range = ', raw_sal_range)
    if len(raw_sal_range) == 2:
        sal_low = int(raw_sal_range[0].replace('k', ''))
        sal_high = int(raw_sal_range[1].replace('k', ''))
    else:
        sal_low = np.nan
        sal_high = np.nan
    raw_company = re.findall('.+–.+,.+',job_text)
    print('raw_company = ', raw_company)
    if len(raw_company) == 1:
        tt = raw_company[0].split('–')
        company = tt[0].strip()
        job_city = tt[1].split(',')[0].strip()
        job_state_code = tt[1].split(',')[1].strip()
    else:
        company = ''
        job_city = ''
        job_state_code = ''
    raw_position = re.findall('(.+sci.+|.+ana.+|.+eng.+)', job_text.lower())
    print('raw_position = ', raw_position)
    if len(raw_position) == 1:
        position = raw_position[0]
    else:
        position = job_text.split('\n')[1].lower()
        
    #GET DATA FROM FULL JOB POSTING
    #Go to Company tab
    #ensure no popups
    
    #set to default
    
    #TODO: should be np NAN
    sal_est = ''
    industry = ''
    sector = ''
    size_small = ''
    size_large = ''
    
    handle_popup(browser)
    
    #get estimated sal from jobs page
    print('location_search = ' + location_search)

    try:
        sal_elem = browser.find_element_by_id('salWrap').\
        find_element_by_class_name('salEst')
        if (re.fullmatch('\$.+\/ year', sal_elem.text)):
            sal_est = int(re.sub('\D', '', sal_elem.text))
            print('sal_est = ' + str(sal_est))
    except NoSuchElementException as e:
        pass


    tabs = browser.find_elements_by_class_name('tabLabel')
    
    if (len(tabs) >= 2):
        tabs[1].click()
        
        #Get Company Info
        company_info = browser.find_element_by_id('EmpBasicInfo').\
        find_element_by_class_name('info').\
        find_elements_by_class_name('infoEntity')
    
        if (len(company_info) > 4):
             if ('Industry' in company_info[4].text):
                industry = company_info[4].text.replace('Industry','')
                print('industry = ' + str(industry))
    
        if (len(company_info) > 5):
            if ('Sector' in company_info[5].text):
                sector = company_info[5].text.replace('Sector','')
                print('sector = ' + str(sector))
    
    
        if (len(company_info) > 1):
            company_size = company_info[1].text.split(' to ')
            if (len(company_size)) >= 1:
                size_small = int(re.sub('\D', '', company_size[0]))
                print('size_small = ', size_small)
            
            if (len(company_size)) >= 2:
                size_large =  int(re.sub('\D', '', company_size[1]))
                print('size_large = ', size_large)
    
    return {'rating': rating, 'position': position, 'company': company, 'job_city': job_city,\
            'location_search': location_search, 'job_state_code': job_state_code, 'sal_low': sal_low,\
            'sal_est': sal_est, 'sal_high': sal_high, 'industry': industry, 'sector': sector,\
            'size_small': size_small, 'size_large': size_large}


        
######### RUN  ##########

def build_dataset(job_title, location, page_count = 15):
    print('job_title = '+ job_title + ', location = ' + location)
    
    url = "https://www.glassdoor.com/index.htm"
    
    job_dict = unpickle(job_title, location)
    
    browser = init_driver()

    wait()
    
    browser.get(url)
    
    enter_search_terms(browser, job_title, location)
    
    scrape_pages(browser, page_count, job_dict, job_title, location)
        
    

    
    