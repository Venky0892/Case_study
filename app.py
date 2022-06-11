

import pandas as pd
import requests



class Inference():

    def __init__(self):
        '''
        
        '''
        

    name  = 'Justin Trudeau'

    def query_api(self, tag, page, from_date, api_key):
        """
        Function to query the API for a particular tag
        returns: a response from API
        """
        response = requests.get("https://content.guardianapis.com/search?q="
                                + tag + "&from-date=" + from_date 
                                +"&page=" + str(page) + "&page-size=200&api-key=" + api_key)
        return response

    def get_results_for_tag(self, tag, from_date, api_key):
        """
        Function to run a for loop for results greater than 200. 
        Calls the query_api function accordingly
        returns: a list of JSON results
        """
        json_responses = []
        response = self.query_api(tag, 1, from_date, api_key).json()
        json_responses.append(response)
        number_of_results = response['response']['total']
        if number_of_results > 200:
            for page in range(2, (round(number_of_results/200))+1):
                response = self.query_api(tag, page, from_date, api_key).json()
                json_responses.append(response)
        return json_responses

    def convert_json_responses_to_df(self, json_responses):
        """
        Function to convert the list of json responses to a dataframe
        """
        df_results = []
        for json in json_responses:
            try:
                df = pd.json_normalize(json['response']['results'])
                df_results.append(df)
            except KeyError:
                pass
        all_df = pd.concat(df_results)
        return all_df
            
    def get_results_for_all_tags(self, tag, from_date, api_key):
        tag_df_list = []
        json_responses = self.get_results_for_tag(tag, from_date, api_key)
        tag_df = self.convert_json_responses_to_df(json_responses)
        tag_df_list.append(tag_df)
        all_tag_df = pd.concat(tag_df_list)
        # all_tag_df = all_tag_df.drop_duplicates(subset=['webTitle', 'webUrl'], inplace = True)
        # all_tag_df['webPublicationDate'] = all_tag_df['webPublicationDate'].apply(lambda x: pd.to_datetime(x))
        # all_tag_df['Date'] = pd.to_datetime(all_tag_df['webPublicationDate']).dt.date
        # all_tag_df['year'] = pd.DatetimeIndex(all_tag_df['Date']).year
        # all_tag_df['week'] = pd.DatetimeIndex(all_tag_df['Date']).week

        return all_tag_df



# API Key 
MY_API_KEY = open("key.txt").read().strip()


