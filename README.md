
# Extracting information using Gaurdian API

The object of the problem is to extract information about "Justin Trudeau" using Gaurdian Media API, 
and do some basic analysis and answer the respective questions



## Task
1. Extract information about Justin Trudeau.
2. Count how many articles about Justin Trudeau have been posted since 01.01.2018 until
    today:
    The output should consist of two columns:
    „Date“ and „No. of articles“
    2018-01-01 3
    2018-01-02 4
    2018-01-03 2
3. Calculate the average of all days for the above-mentioned period from “No. of articles”.
4. In which section are most articles written?
5. Show the evolution of the "No. of articles" over time for the above period.
6. Are there any unusual events in the time series under investigation?
7. If so, show these. Why are these unusual? (Define for yourself what you want to show by
ordinary or unusual).
8. Based on question one. Show the cause of the unusual event.
Create a daily automated job that updates question 5 daily and creates an output that could be sent
to recipients who have not seen the data before. 


## Answers 

Anwers are located in 

```bash
cd CASE_STUDY/Answers.pdf
```
## Demo

For the purpose of the task I have created a streamlit web application to extract any person information using the "Search Bar" and "Date".  The web application will generate answers for all the questions in a automated way. 


## Screenshots

![App Screenshot](https://github.com/Venky0892/Case_study/blob/master/streamlit.png)




## Run Locally

Task answers are given in answer.pdf 

Or you could run the web application via docker to check the answer.

Install Docker, Inside the project directory

```bash
docker-compose up
```
OR 

Clone the project

```bash
  git clone https://github.com/Venky0892/Case_study.git
```

Go to the project directory

```bash
  ./CASE_STUDY
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  streamlit run stream.py

  Note: Once the application is started, replace the IP address to localhost:8051 to view the app.
```

In the streamlit application

```bash
Inside the search bar : "Provide the information to search"
Inside the date field : "Provide the date formate and to extract data"
```


