from models import City, Industry, Company, Job
import pandas as pd
import pdb
from sqlalchemy.orm import sessionmaker

#import re
#re.sub('\D', '', str)

# from console import db


#####################################################################

# print('<<<<<<<running func city_creator()>>>>>>>>')

def create_cities():
    df = pd.read_csv('data/csv/city_expenses.csv')
    print('test printing df stats:', df.describe())
    cities = []
    for i in range(len(df)):
        req_income = int(df.req_income[i].replace('$', '').replace(',' , ''))
        expenses = (req_income * 4)/5000
        name = df.City[i]
        cities.append(City(name = name, expenses = expenses))
    return cities

# cities = city_creator()

# print('<<<<<<<testing func city_creator()>>>>>>>>')
# vars(cities[0])
# print('test printing cities[0].name:', cities[0].name)

#####################################################################

# print('<<<<<<<running func industry_creator()>>>>>>>>')

def create_industries(industries, df):
    df_industries = set([industry for industry in df.industry])
    industry_names = [industry.name for industry in industries if len(industries)!=0]
    for name in df_industries:
        if name not in industry_names:
            industries.append(Industry(name = name))

# industries = industry_creator(df)

# print('<<<<<<<testing func industry_creator()>>>>>>>>')
# # vars(industries[0])
# print('test printing industies[0].name:', industries[0].name)
# # pdb.set_trace()

#####################################################################

# print('<<<<<<<running func company_creator()>>>>>>>>')

#called iteratively to populate companies argument
#with each df representation of csv
def create_companies(companies, df):
    comp_names = [company.name for company in companies]
    for i in range(len(df)):
        if not (df.company[i] in comp_names):
            name = df.company[i]
            size_small = df.size_small[i]
            size_large = df.size_large[i]
            companies.append(Company(name = name, size_lower = size_small, size_upper = size_large))
            comp_names.append(name)
# print('****PAUSE****')
# pdb.set_trace()

# companies = company_creator(df)
# print('<<<<<<<testing func company_creator()>>>>>>>>')
# print(f'company size upper{companies[0].size_upper} and lower:{companies[0].size_lower}' )
# print(f'company_names = {[comp.name for comp in companies]}\n\n <<<<<<<<<<MOVING ON>>>>>>>>>>\n\n')
# # pdb.set_trace()
#
#####################################################################

# print('\n\n<<<<<<<running func job_creator()>>>>>>>>')

#return company object with name comp_name
def get_attribute(name, list):
    names = [item.name for item in list]
    if name in names:
        index = names.index(name)
        return list[index]



def create_jobs(jobs, df, companies, industries, cities):
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

# jobs = job_creator(df)

print('<<<<<<<DONE WITH SEED>>>>>>>>')

# print(f'job_industries = {[(job.industry.name, job.title) for job in jobs]}\n\njob_companies = {[(job.company.name, job.title) for job in jobs]}\n\njob_cities = {[(job.city.name, job.title) for job in jobs]}\n\n <<<<<<<<<<MOVING ON>>>>>>>>>>\n\n')

#####################################################################

# print('\n\n<<<<<<<setting job company>>>>>>>>')
#
# def set_job_company():
#     company_names = [comp.name for comp in companies]
#     for job in jobs:
#         if job.comp_name in company_names:
#             index = company_names.index(job.comp_name)
#             job.company = companies[index]
#
# set_job_company()
#
# print('<<<<<<<testing func set_job_company()>>>>>>>>')
# print(f'job_companies = {[(job.company.name, job.title) for job in jobs]}\n\n <<<<<<<<<<MOVING ON>>>>>>>>>>\n\n')
#
#####################################################################

# print('\n\n<<<<<<<setting job industry>>>>>>>>')
#
# def set_job_industry():
#     industry_names = [industry.name for industry in industries]
#     for job in jobs:
#         if job.ind_name in industry_names:
#             index = industry_names.index(job.ind_name)
#             job.industry = industries[index]
#
# set_job_industry()
#
# print('<<<<<<<testing func set_job_industry()>>>>>>>>')
# print(f'job_industries = {[(job.industry.name, job.title) for job in jobs]}\n\n <<<<<<<<<<MOVING ON>>>>>>>>>>\n\n')

#####################################################################

# print('\n\n<<<<<<<setting job city>>>>>>>>')
#
# def set_job_city():
#     city_names = [city.name for city in cities]
#     for job in jobs:
#         if job.major_cit in city_names:
#             index = city_names.index(job.major_cit)
#             job.city = cities[index]
#         else:
#             cities.append(City(name=job.major_cit))
#             city_names = [city.name for city in cities]
#             index = city_names.index(job.major_cit)
#             job.city = cities[index]
#
# set_job_city()
#
# print('<<<<<<<testing func set_job_city()>>>>>>>>')
# print(f'job_cities = {[(job.city.name, job.title) for job in jobs]}\n\n <<<<<<<<<<MOVING ON>>>>>>>>>>\n\n')



# print('            ***DONE***\n\n*********YOU ARE AWESOME!!*********')


# might need the following functions later>>>
# print('****PAUSE****')
# pdb.set_trace()
# def set_job_city():#creates new city object then sets job city if city is missing
#     city_names = [city.name for city in cities]
#     for job in jobs:
#         if job.cit_name in city_names:
#             index = city_names.index(job.cit_name)
#             job.city = cities[index]
#         else:
#             cities.append(City(name=job.cit_name))
#             city_names = [city.name for city in cities]
#             index = city_names.index(job.cit_name)
#             job.city = cities[index]

# def citylist_creator():
#     df = pd.read_csv(job_csv)
#     listy = [city for city in df.job_city]
#     cities = []
#     for i in range(len(df)):
#         if not df.job_city[i] in cities:
#             cities.append(df.job_city[i])
#     return cities
# cities2 = citylist_creator()


# def city_exp_dict():
#     city_dict = {}
#     for i in range (len(df)):
#         for i in range(len(df)):
#             req_income = int(df.req_income[i].replace('$', '').replace(',' , ''))
#             expenses = (req_income * 4)/5000
#             name = df.City[i]
#             city_i ={'name': name, 'expenses': expenses }
#             city_dict[name] = city_i
#         return city_dict
