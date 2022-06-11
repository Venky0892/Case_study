from time import sleep, time
import streamlit as st
import pandas as pd
import requests
from pathlib import Path
from app import Inference
from forecast import Forecast
from pandasql import sqldf
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import pandas_profiling
from streamlit_pandas_profiling import st_profile_report
from fbprophet.plot import plot_plotly, plot_components_plotly
# import plotly.graph_objs as go

engine = create_engine('sqlite://', echo=False)



inf = Inference()
forecast = Forecast()
def main():
    body()
    sidebar()

def header(url):
     st.markdown(f'<p style=color:#F5340B;font-size:10px;border-radius:2%;">{url}</p>', unsafe_allow_html=True)

def body():
    st.set_page_config(layout="wide")

    st.markdown("""
    <style>
    .big-font {
        font-size:50px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown('<p class="big-font"> Auto-Extraction App 🎉 </p>', unsafe_allow_html=True)
    st.markdown('<p class="small-font">Owner: Venkatesh Prasath M </p>', unsafe_allow_html=True)
    
def plot(X, Y, name_x,name_y, line = False, bar = False):
    year = list(X)
    No_Articles = list(Y)
    
    fig = plt.figure(figsize = (10, 5))
    
    # creating the bar plot
    if line == True:
        plt.plot(year, No_Articles, color ='blue',
                )
    if bar == True:
        plt.bar(year, No_Articles, color ='blue',
                width=0.4)
    
    plt.xlabel(name_x)
    plt.ylabel(name_y)
    plt.title(name_x + '  vs  ' + name_y) 
    st.pyplot(fig)


def sidebar():
    st.markdown(
    f'''
        <style>
            .sidebar .sidebar-content {{
                width: 1500px;
            }}
        </style>
    ''',
    unsafe_allow_html=True
)

    MY_API_KEY = open("key.txt").read().strip()

    api_key = '4fefdc9f-964f-4a4f-b862-61e63534d079'

    title = st.sidebar.text_input('Search Name')
    Dy = st.sidebar.text_input('Date')
    st.sidebar.write("Date format in (%Y-%m-%d) ie: '2012-01-01' ")
    if st.sidebar.button("Extract 👈"):
        if title != "" and Dy != "":
            with st.spinner('Please wait......'):
                df = inf.get_results_for_all_tags( title, Dy, MY_API_KEY)
                df.to_csv('result_00.csv')
                st.write(f"Extracting information about {title} done")
                df = pd.read_csv('result_00.csv')
                df.drop_duplicates(subset=['webTitle', 'webUrl'], inplace = True)
                df['Date'] = pd.to_datetime(df['webPublicationDate']).dt.date
                df['year'] = pd.DatetimeIndex(df['Date']).year
                df['week'] = pd.DatetimeIndex(df['Date']).week

                # pr = df.profile_report()

                # st_profile_report(pr)


                df.to_sql('users', con=engine)

                
                # pysqldf = lambda q: sqldf(q, globals()) 
                # q = "SELECT distinct(Date) , count(type) as article FROM df WHERE type = 'article' and Date  >= '2018-01-01' group by Date;"

                # names = pysqldf(q)    
                # Question 1 *********************************************************************************************************** 
                st.write(f"Question 1: Extract information about {title} ") 
                st.write(df.head())
                st.write("Total number of records:", len(df))

                st.write("------------------------------------------------------------------------------------------------------------")
                # QUESTION 2 *********************************************************************************************************** 
                question2 = engine.execute( f"select distinct(Date) , count(type) as article FROM users WHERE type = 'article' and Date  >= {Dy} group by Date;")
                df_1 = pd.DataFrame(question2.fetchall(), columns=['Date','Article_count']) 
                st.write("Question 2: Count how many articles have been posted since 2018-01-01", df_1,)
                st.write("------------------------------------------------------------------------------------------------------------")

                # QUESTION 3 ***********************************************************************************************************
                df_1.to_sql('users_ex', con=engine)
                question3 = engine.execute(f"select Sum(Article_count) / (julianday(max(date)) - julianday(min(date))) as average from users_ex;")
                # question3 = engine.execute(f"select julianday(max(date)) - julianday(min(date))as average from users_ex;")
                df_2 = pd.DataFrame(question3.fetchall()) 
                st.write("Question 3: Average of all days from the above mention period from No.of.articles", df_2)
                st.write("------------------------------------------------------------------------------------------------------------")



                question4 = engine.execute("select sectionid, max(count) from (select sectionid, count(sectionid) as count from users where type = 'article' group by sectionid order by count DESC);")
                
                df_3 = pd.DataFrame(question4.fetchall(), columns=['Section_id','Max(count)']) 
                st.write("Question 4: Which section most articles are written:", df_3)
                st.write("------------------------------------------------------------------------------------------------------------")


                question5 = engine.execute("Select year, count(type) as No_articles from users where type = 'article' group by year")
                df_5 = pd.DataFrame(question5.fetchall(), columns=['Year','Total_count_ofarticles']) 
                st.write("Question 5: Show Evolution of no_of_articles have written over the period", df_5)
                plot(df_5['Year'], df_5['Total_count_ofarticles'], df_5.columns[0], df_5.columns[1], bar = True)
                

                st.write("------------------------------------------------------------------------------------------------------------")

                question8 = engine.execute( f"select distinct(Date) , count(type) as article FROM users WHERE Date  >= {Dy} group by Date;")
                df_8 = pd.DataFrame(question8.fetchall(), columns=['Date','Article_count'])
                # df_1.to_csv("forecast.csv")
                df_1 = df_8.rename({'Date': 'ds', 'Article_count': 'y'}, axis='columns')
                fore, model = forecast.fit_predict_model(df_1)
                pred = forecast.detect_anomalies(fore)
                ## Anamolies 
                anamolies = pred[pred['anomaly'] > 0]
                anamolies['Date'] = pd.to_datetime(anamolies['ds']).dt.date
                anamolies.to_sql('anamolies', con=engine)

                st.write(" Question 6: Are their any unusual events under the time series?")
                if len(anamolies) < 0:
                    st.write("No unusual events as per the current period under time series analysis")
                else:
                    st.write("Yes, Their are some unusual Events in the current time period calculated from time series analysis")
                    st.write("------------------------------------------------------------------------------------------------------------")
                    st.write("Question 7:If so, show these. Why are these unusual? (Define for yourself what you want to show by ordinary or unusual).", anamolies[['ds', 'anomaly']])
                    st.write("There we unsual events between late 2019 and early 2020, article about Trudeau about brown face issue, coronovirus sweep and plan crash.")
                    st.write(model.plot(pred))


                test = engine.execute("select u1.webTitle, u1.Date, u2.anomaly FROM users as u1 inner join anamolies as u2 on u1.Date = u2.Date where type = 'article' group by u1.Date, u2.anomaly;")
                # test = engine.execute("select distinct(Date), webtitle from users where Date in (select Date from anamolies)")
                df_test = pd.DataFrame(test.fetchall(), columns=['webTitle', 'Date', 'anomaly'])
                st.write("------------------------------------------------------------------------------------------------------------")
                st.write("Question 8: Based on question one. Show the cause of the unusual event")
                st.write("Some examples of the unusual event", df_test)
                st.write("Article trending vs Time Period with some anomalies")
                # # st.write("Question6", question6)

                st.write("------------------------------------------------------------------------------------------------------------")
                st.write(f"Pandas Profilling for the overview of the {title}")
                pr = df.profile_report()

                st_profile_report(pr)

                
                # st.balloons()
        
           
        else:
            # st.write("To extract information you need to specify Date and Search name")
            header(" ⚠️ To extract information you need to specify Date and Search name")

    



if __name__ == '__main__':

    main()