from sqlalchemy.orm import sessionmaker
from models import *
from seed import *
import pandas as pd
from os import listdir, getcwd


def get_filepaths():
    path = 'data/csv'
    csv_filenames = list(filter(lambda f: '.csv' in f and 'data' in f, listdir(path)))
    file_paths = [path+'/'+name for name in csv_filenames]
    return file_paths

def pd_read_csv(file_paths):
    df_list = []
    for filepath in file_paths:
        df = pd.read_csv(filepath)
        print('test printing df stats:', df.describe())
        df_list.append(df)
    return df_list

###########################################################################

# def build_instances(session, df):
#     industries = create_industries(df, industries)
#     companies = create_companies(df)
#     jobs = create_jobs(df)


cities = create_cities()
companies = []
industries = []
jobs = []
def build_database():
    file_paths = get_filepaths()
    df_list = pd_read_csv(file_paths)
    for df in df_list:
        create_companies(companies, df)
        create_industries(industries, df)
        create_jobs(jobs, df, companies, industries, cities)

build_database()
print('<<<<<<<testing builder()>>>>>>>>')
print(f'jobs = {len(jobs)}\n companies = {len(companies)}\n industries = {len(industries)}\n {len(cities)}\n\n <<<<<<<<<<DONE BUILDING>>>>>>>>>>\n\n')
# session.add_all(cities)
# session.add_all(industries)
# session.add_all(companies)
# session.add_all(jobs)


# /Users/samiramunir/Documents/Flatiron_2018/Projects/project1/scraper
