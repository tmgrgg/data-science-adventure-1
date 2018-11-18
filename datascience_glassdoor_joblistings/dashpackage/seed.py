from dashpackage.models import City, Industry, Company, Job
from dashpackage.__init__ import db
import pandas as pd
from os import listdir
import pdb




###########Functions to Instantiate City, Industry, Company, Job objects################################################

def create_cities():
    print('<<<<<<<creating cities()>>>>>>>>')
    df = pd.read_csv('dashpackage/data/csv/city_expenses.csv')
    print('test printing df stats:', df.describe())
    cities = []
    for i in range(len(df)):
        req_income = int(df.req_income[i].replace('$', '').replace(',' , ''))
        expenses = (req_income * 4)/5000
        name = df.City[i]
        cities.append(City(name = name, expenses = expenses))
    return cities


#####################################################################


def create_industries(industries, df):
    print('<<<<<<<creating industries>>>>>>>>')
    df_industries = set([industry for industry in df.industry])
    industry_names = [industry.name for industry in industries if len(industries)!=0]
    for name in df_industries:
        if name not in industry_names:
            industries.append(Industry(name = name))

#####################################################################

#called iteratively to populate companies argument
#with each df representation of csv
def create_companies(companies, df):
    print('<<<<<<<creating companies>>>>>>>>')
    comp_names = [company.name for company in companies]
    for i in range(len(df)):
        if not (df.company[i] in comp_names):
            name = df.company[i]
            size_small = df.size_small[i]
            size_large = df.size_large[i]
            companies.append(Company(name = name, size_lower = size_small, size_upper = size_large))
            comp_names.append(name)


#return company object with name comp_name
def get_attribute(name, list):
    names = [item.name for item in list]
    if name in names:
        index = names.index(name)
        return list[index]



def create_jobs(jobs, df, companies, industries, cities):
    print('<<<<<<<creating jobs>>>>>>>>')
    for i in range(len(df)):
        nan = None
        title = df.position[i]
        sal_upper = df.sal_high[i]
        sal_lower = df.sal_low[i]
        glassdoorid = df.job_id[i]
        company = get_attribute(df.company[i], companies)
        salary_estimated = df.sal_est[i]/1000
        industry = get_attribute(df.industry[i], industries)
        city = get_attribute(df.location_search[i], cities)
        listed_city = df.job_city[i]
        jobs.append(Job(title=title, sal_upper=sal_upper, sal_lower=sal_lower, glassdoorid = glassdoorid, company=company, industry=industry, city=city, salary_estimated=salary_estimated, listed_city=listed_city ))

###########Functions to Get File Paths of & Read all CSV files################################################
def get_filepaths():
    path = 'dashpackage/data/csv'
    csv_filenames = list(filter(lambda f: '.csv' in f and 'data' in f,listdir(path)))
    file_paths = [path+'/'+name for name in csv_filenames]
    return file_paths

def pd_read_csv(file_paths):
    df_list = []
    for filepath in file_paths:
        df = pd.read_csv(filepath)
        print('test printing df stats:', df.describe())
        df_list.append(df)
    return df_list

#####Function to call all creator and filepath functions################################################

def build_database():
    cities = create_cities()
    companies = []
    industries = []
    jobs = []
    file_paths = get_filepaths()
    df_list = pd_read_csv(file_paths)
    for df in df_list:
        create_companies(companies, df)
        create_industries(industries, df)
        create_jobs(jobs, df, companies, industries, cities)
        all_lists = {'cities': cities, 'companies':companies, 'industries':industries, 'jobs':jobs}
    return all_lists


def populate_db():
    all_lists = build_database()
    print('cities :',len(all_lists['cities']), ',','companies :',len(all_lists['companies']), ',', 'inustries :', len(all_lists['industries']), ',', 'jobs:', len(all_lists['jobs']))
    # print(f'jobs = {len(all_lists['jobs'])})\n companies = {len(all_lists['companies'])}\n industries = {len(all_lists['industries'])}\n cities = {len(cities)}\n\n *****Ready To Commit******\n\n')
    for k,v in all_lists.items():
        db.session.add_all(v)



print('<<<<<<<DONE WITH SEED>>>>>>>>')
