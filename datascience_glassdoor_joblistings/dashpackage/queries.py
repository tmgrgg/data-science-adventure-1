from dashpackage.__init__ import db
from dashpackage.models import  Job, City, Company, Industry
from sqlalchemy import func
import plotly.graph_objs as go
import pdb


def return_companies():
    return [company.name for company in db.session.query(Company).all() ]
# print(return_companies())

def return_industries():
    return [industry.name for industry in db.session.query(Industry).all() ]
# print(return_industries())


def industries_and_job_listings_donut_chart():
    listy =db.session.query(func.count(Job.id), Industry.name).join(Industry).order_by(func.count(Job.id).desc()).group_by(Industry.name).all()
    # pdb.set_trace()
    values = []
    labels = []
    data = []
    for item in listy:
        values.append(round((item[0]/len(return_industries()))*100, 2))

        labels.append(item[1])
    data = [{"values":values,
            "labels":labels,
            "domain": {"x": [0, .48]},
            "name": "Data Science Jobs by industry",
            "type": "pie",
            "textposition":"inside",
            "hoverinfo":"label+percent+name",
            "hole": .4,}]
    # data = go.Pie (values = values, labels = labels)


    return data

print('******Done with Queries******')
#
#
# print(top_10_industries_witht_highest_job_listings())


# def return_list_of_dicts_of_tech_company_names_and_their_EVs_ordered_by_EV_descending():
#     techs = session.query(Company).filter(Company.industry == 'Technology').order_by(Company.enterprise_value.desc())
#     listy = []
#     for c in techs:
#         c_dict = {'company_name': c.company , 'EV': c.enterprise_value}
#         listy.append(c_dict)
#     return listy
#
# def return_list_of_consumer_products_companies_with_EV_above_225():
#     listy = session.query(Company).filter(Company.industry == 'Consumer products').filter(Company.enterprise_value > 225).all()
#     return [(c.company, f'EV = {c.enterprise_value}') for c in listy]
#
#
# def return_conglomerates_and_pharmaceutical_companies():
#     listy = session.query(Company).filter(or_(Company.industry =='Pharmaceuticals', Company.industry == 'Conglomerate')).all()
#     return [(c.company, f'Industry : {c.industry}') for c in listy]
# def avg_EV_of_dow_companies():
#     return round(session.query(func.avg(Company.enterprise_value))[0][0], 3)
# #
# def return_industry_and_its_total_EV():
#      return session.query(func.sum(Company.enterprise_value), Company.industry).group_by(Company.industry).all()
#      # return [{'industry' : c.industry, 'EV' : c.enterprise_value} for c in listy]
# # session.query(Table.column, func.count(Table.column)).group_by(Table.column).all()
# #     # session.query(func.count(User.id)).\
# #     #     group_by(User.name)
