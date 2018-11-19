from dashpackage.__init__ import db
from dashpackage.models import  Job, City, Company, Industry
from sqlalchemy import func
import plotly.graph_objs as go
import pdb
import plotly.plotly as py
import pandas as pd

pie_chart_colors = {"marker": {"colors" : ['rgb(179,226,205)',\
                                          'rgb(247,247,247)','rgb(186,228,188)',\
                                          'rgb(237,248,233)','rgb(35,139,69)',\
                                          'rgb(116,196,118)','rgb(150,150,150)',\
                                          'rgb(82,82,82)','rgb(161,218,180)',\
                                          'rgb(240,249,232)', 'rgb(115,115,115)'\
                                          ,'rgb(35,139,69)','rgb(116,196,118)',\
                                          'rgb(35,139,69)','rgb(99,99,99)',\
                                          'rgb(204,204,204)','rgb(186,228,179)'\
                                          ,'rgb(150,150,150)']}}

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
        if (item[1] is not None):
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

def get_industry_pie_chart(city):
    #need to change this query!
    #df = pd.read_sql(db.session.query( Industry.name).join(Industry).order_by(func.count(Job.id).desc()).group_by(Industry.name).statement, db.session.bind) 
    
    #this gets us to a place where we just have san fran!
    #df = pd.read_sql(db.session.query(Job, City).join(City).filter(City.name == city).statement, db.session.bind)
    #df = pd.read_sql(db.session.query(Job, City).join(City).filter(City.name == city).join(Industry).statement, db.session.bind)
    #df = pd.read_sql(db.session.query(func.count(Job.id), City, Industry.name).join(City).filter(City.name == city).join(Industry).statement, db.session.bind)
    df = pd.read_sql(db.session.query(Job, Industry).join(City).join(Industry).filter(City.name == city).statement, db.session.bind)

    #could also easily vtake mean of estimated salary to get the mean salary per industry!
    print('DF BEFORE GROUP: ', df)
    df = df.groupby(['name'])['title'].count()
   # df = df.to_frame()
    pd.set_option('display.max_columns', None)
    
    df.to_csv('my_csv.csv')

    print('JOINED', df)

    
   # print('listy!', listy)
    #listy =db.session.query(func.count(Job.id), Industry.name).join(Industry).order_by(func.count(Job.id).desc()).group_by(Industry.name).all()
    # pdb.set_trace()
    values = df.values
    labels = df.index
    data = []
    
    data = [{"values":values,
             "title":city + " jobs<br>by Industry",
            "labels":labels,
            "domain": {"x": [0, .48]},
            "name": "Data Science Jobs by Industry",
            "type": "pie",
            "textposition":"outside",
            "showlegend":False,
            "hoverinfo":"label+percent+name",
            "marker":pie_chart_colors['marker'],
            "colors" : ['#FEBFB3', '#E1396C', '#96D38C', '#D0F9B1'],
            "hole": .4,}]
            
    layout = layout = go.Layout(
            autosize=False,
            width=500,
            height=500,
            margin=go.layout.Margin(
                    l=120,
                    r=20,
                    b=20,
                    t=20,
                    pad=4
            ),
            #paper_bgcolor='#7f7f7f',
            #plot_bgcolor='#c7c7c7'
            )
    # data = go.Pie (values = values, labels = labels)
    
    return data, layout



def get_industry_pie_chart2(city):
    #need to change this query!
    #df = pd.read_sql(db.session.query( Industry.name).join(Industry).order_by(func.count(Job.id).desc()).group_by(Industry.name).statement, db.session.bind)

    #this gets us to a place where we just have san fran!
    #df = pd.read_sql(db.session.query(Job, City).join(City).filter(City.name == city).statement, db.session.bind)
    #df = pd.read_sql(db.session.query(Job, City).join(City).filter(City.name == city).join(Industry).statement, db.session.bind)
    #df = pd.read_sql(db.session.query(func.count(Job.id), City, Industry.name).join(City).filter(City.name == city).join(Industry).statement, db.session.bind)
    df = pd.read_sql(db.session.query(Job, Industry).join(City).join(Industry).filter(City.name == city).statement, db.session.bind)

    #could also easily vtake mean of estimated salary to get the mean salary per industry!
    print('DF BEFORE GROUP: ', df)
    df = df.groupby(['name'])['title'].count()
   # df = df.to_frame()
    pd.set_option('display.max_columns', None)

    df.to_csv('my_csv.csv')

    print('JOINED', df)


   # print('listy!', listy)
    #listy =db.session.query(func.count(Job.id), Industry.name).join(Industry).order_by(func.count(Job.id).desc()).group_by(Industry.name).all()
    # pdb.set_trace()
    values = df.values
    labels = df.index
    data = []

    data = [{"values":values,
             "title":city + " jobs<br>by Industry",
            "labels":labels,
            "domain": {"x": [0, .48]},
            "name": "Data Science Jobs by Industry",
            "type": "pie",
            "textposition":"outside",
            "showlegend":False,
            "hoverinfo":"label+percent+name",
            "marker": {"colors" : ['rgb(179,226,205)', 'rgb(247,247,247)','rgb(186,228,188)','rgb(237,248,233)','rgb(35,139,69)', 'rgb(116,196,118)','rgb(150,150,150)', 'rgb(82,82,82)','rgb(161,218,180)', 'rgb(240,249,232)', 'rgb(115,115,115)'    ,'rgb(35,139,69)','rgb(116,196,118)','rgb(35,139,69)','rgb(99,99,99)','rgb(204,204,204)','rgb(186,228,179)','rgb(150,150,150)']},
            "hole": .4,}]
    
    layout = go.Layout(
            autosize=False,
            width=500,
            height=500,
            margin=go.layout.Margin(
                    l=120,
                    r=20,
                    b=20,
                    t=20,
                    pad=4
            ),
            #paper_bgcolor='#7f7f7f',
            #plot_bgcolor='#c7c7c7'
            )
    # data = go.Pie (values = values, labels = labels)

    return data, layout

def get_samira_chart():
    df = pd.read_sql(db.session.query(Job, City).join(City).statement, db.session.bind)
    city_df = df.groupby(['name'])['salary_estimated'].mean()
    city_df = city_df.to_frame()
    city_exp_df = df.groupby(['name'])['expenses'].mean().to_frame()
    x = [city for city in city_df.index]
    y = [round(salary, 2) for salary in city_df['salary_estimated']]
    y2 = [round(expense, 2) for expense in city_exp_df['expenses']]
    trace1 = dict(x=x,y=y,name='Estimated Salary', marker=dict(color='rgb(12, 167, 65)'), type='bar')
    trace2 = dict(x=x,y=y2,name='Expenses', marker=dict(color='rgb(180, 200, 180)'), type='bar')
    data = [trace1, trace2]
    
    layout = go.Layout(
    barmode='group'
    )
    return data, layout

def get_sector_pie_chart(city):
    #need to change this query!
    #df = pd.read_sql(db.session.query( Industry.name).join(Industry).order_by(func.count(Job.id).desc()).group_by(Industry.name).statement, db.session.bind) 
    
    #this gets us to a place where we just have san fran!
    #df = pd.read_sql(db.session.query(Job, City).join(City).filter(City.name == city).statement, db.session.bind)
    #df = pd.read_sql(db.session.query(Job, City).join(City).filter(City.name == city).join(Industry).statement, db.session.bind)
    #df = pd.read_sql(db.session.query(func.count(Job.id), City, Industry.name).join(City).filter(City.name == city).join(Industry).statement, db.session.bind)
    df = pd.read_sql(db.session.query(Job).join(City).filter(City.name == city).statement, db.session.bind)

    #could also easily vtake mean of estimated salary to get the mean salary per industry!
    print('DF BEFORE GROUP: ', df)
    df = df.groupby(['sector'])['title'].count()
   # df = df.to_frame()
    pd.set_option('display.max_columns', None)
    
    df.to_csv('my_csv.csv')

    print('JOINED', df)

    
   # print('listy!', listy)
    #listy =db.session.query(func.count(Job.id), Industry.name).join(Industry).order_by(func.count(Job.id).desc()).group_by(Industry.name).all()
    # pdb.set_trace()
    values = df.values
    labels = df.index
    data = []
    
    data = [{"values":values,
             "title":city + " jobs<br>by Sector",
            "labels":labels,
            "domain": {"x": [0, .48]},
            "name": "Data Science Jobs by Sector",
            "type": "pie",
            "textposition":"outside",
            "marker": {"colors" : ['rgb(179,226,205)', 'rgb(247,247,247)','rgb(186,228,188)','rgb(237,248,233)','rgb(35,139,69)', 'rgb(116,196,118)','rgb(150,150,150)', 'rgb(82,82,82)','rgb(161,218,180)', 'rgb(240,249,232)', 'rgb(115,115,115)'    ,'rgb(35,139,69)','rgb(116,196,118)','rgb(35,139,69)','rgb(99,99,99)','rgb(204,204,204)','rgb(186,228,179)','rgb(150,150,150)']},
            "showlegend":False,
            "hoverinfo":"label+percent+name",
            "colors" : ['#FEBFB3', '#E1396C', '#96D38C', '#D0F9B1'],
            "hole": .4,}]
            
    layout = layout = go.Layout(
            autosize=False,
            width=500,
            height=500,
            
            margin=go.layout.Margin(
                    l=120,
                    r=20,
                    b=20,
                    t=20,
                    pad=4
            ),
            #paper_bgcolor='#7f7f7f',
            #plot_bgcolor='#c7c7c7'
            )
    # data = go.Pie (values = values, labels = labels)
    
    return data, layout

def interactive_map_data_example(): 
    #create pandas dataframe from sql
    #listy = db.session.query(Job).all()
    #print("INTERACTIVE MAP DATA: ", listy, "END INTERACTIVE MAP DATA")
    #return None
    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_february_us_airport_traffic.csv')
    df.head()
    
    df['text'] = df['airport'] + '' + df['city'] + ', ' + df['state'] + '' + 'Arrivals: ' + df['cnt'].astype(str)
    
    scl = [ [0,"rgb(5, 10, 172)"],[0.35,"rgb(40, 60, 190)"],[0.5,"rgb(70, 100, 245)"],\
        [0.6,"rgb(90, 120, 245)"],[0.7,"rgb(106, 137, 247)"],[1,"rgb(220, 220, 220)"] ]
    
    data = [ dict(
            type = 'scattergeo',
            locationmode = 'USA-states',
            lon = df['long'],
            lat = df['lat'],
            text = df['text'],
            mode = 'markers',
            marker = dict(
                size = 8,
                opacity = 0.8,
                reversescale = True,
                autocolorscale = False,
                symbol = 'square',
                line = dict(
                    width=1,
                    color='rgba(102, 102, 102)'
                ),
                colorscale = scl,
                cmin = 0,
                color = df['cnt'],
                cmax = df['cnt'].max(),
                colorbar=dict(
                    title="Incoming flightsFebruary 2011"
                )
            ))]
    
    layout = dict(
            title = 'Most trafficked US airports<br>(Hover for airport names)',
            colorbar = True,
            geo = dict(
                scope='usa',
                projection=dict( type='albers usa' ),
                showland = True,
                landcolor = "rgb(250, 250, 250)",
                subunitcolor = "rgb(217, 217, 217)",
                countrycolor = "rgb(217, 217, 217)",
                countrywidth = 0.5,
                subunitwidth = 0.5
            ),
        )
    
    return data, layout

def to_dollars(x_thousands):
    return '${:,}'.format(int(x_thousands*1000))

def get_stats(city):
    print('GOT INTO STATS AT LEAST')
    df = pd.read_sql(db.session.query(Job, City).join(City).filter(City.name == city).statement, db.session.bind)
    
    stats = {'salary_estimated_hi': to_dollars(df['salary_estimated'].max()),
             'salary_estimated_lo': to_dollars(df['salary_estimated'].min()),
             'expenses': to_dollars(df['expenses'].max())
            }
    
    print('STATS:', stats)
    return stats


def interactive_map_data(): 
    #create pandas dataframe from sql
    #listy = db.session.query(Job).all()
    #print("INTERACTIVE MAP DATA: ", listy, "END INTERACTIVE MAP DATA")
    #return None
    
    #group_by as_index=False to keep it as a dataframe prolly
    airport_df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_february_us_airport_traffic.csv')
    print(airport_df)
    
    airport_df = airport_df.groupby(['city'])['long', 'lat'].max()
    
    print(airport_df.loc['New York']['long'])

    df = pd.read_sql(db.session.query(Job, City).join(City).statement, db.session.bind) 

    
   # pdb.set_trace()
    
    city_df = df.groupby(['name'])['salary_estimated'].mean()
    city_df = city_df.to_frame()
    #city_df = city_df.reset_index()
   # print(city_df)

    city_df['text'] = city_df.index + ': ' + city_df['salary_estimated'].apply(to_dollars)
    
    city_df['long'] = [0.0,0.0,0.0,0.0,0.0,0.0]
    city_df['lat'] = [0.0,0.0,0.0,0.0,0.0,0.0]
    
    for city in city_df.index:
        
        #city_df.loc[]
        print('setting ' + city + ' lat from ' + str(city_df.loc[city]['lat']) + ' to ' + str(airport_df.loc[city]['lat']))
        city_df.at[city, 'lat'] = airport_df.loc[city]['lat']
        
        print('setting ' + city + ' long from ' + str(city_df.loc[city]['long']) + ' to ' + str(airport_df.loc[city]['long']))
        city_df.at[city, 'long'] = airport_df.loc[city]['long']

    print(city_df)
   
   
   # city_df['text'] = city_df['name'] + ', mean Glassdoor est. salary = ' + str(city_df[1])
    
    
  #  scl = [ [0,"rgb(172, 10, 5)"],[0.35,"rgb(190, 60, 40)"],[0.5,"rgb(245, 100, 70)"],\
   #     [0.6,"rgb(245, 120, 90)"],[0.7,"rgb(247, 137, 106)"],[1,"rgb(220, 220, 220)"] ]
    
    scl = [ [0,"rgb(12, 165, 67)"],[1,"rgb(180, 180, 180)"]]
    
    data = [ dict(
            type = 'scattergeo',
            locationmode = 'USA-states',
            lon = city_df['long'],
            lat = city_df['lat'],
            text = city_df['text'],
            hoverinfo = 'text',
            mode = 'markers',
            marker = dict(
                size = 8,
                opacity = 0.8,
                reversescale = True,
                autocolorscale = False,
                symbol = 'circle',
                line = dict(
                    width=2,
                    color='rgba(102, 102, 102)'
                ),
                colorscale = scl,
                cmin = city_df['salary_estimated'].min(),
                color = city_df['salary_estimated'],
                cmax = city_df['salary_estimated'].max(),
                colorbar=dict(
                    title='',
                    #width=30,
                    tickprefix='$',
                    ticksuffix='K'
                )
            ))]
    
    layout = dict(
            #title = 'Mean Glassdoor Estimed Data<br> Science Salaries for US cities',
            colorbar = True,
            geo = dict(
                scope='usa',
                projection=dict( type='albers usa' ),
                showland = True,
                landcolor = "rgb(250, 250, 250)",
                subunitcolor = "rgb(217, 217, 217)",
                countrycolor = "rgb(217, 217, 217)",
                #countrywidth = 0.5,
                #subunitwidth = 0.5
            ),
        )
            
    
    
    return data, layout

   # return data, layout
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
