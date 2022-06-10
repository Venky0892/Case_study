from fbprophet import Prophet
import pandas as pd 
import numpy as np

class Forecast():

    def __init__(self):
            '''
            
            '''

    def fit_predict_model(self, dataframe, interval_width = 0.99, changepoint_range = 0.8):
        m = Prophet(daily_seasonality = False, yearly_seasonality = False, weekly_seasonality = False,
                    seasonality_mode = 'additive',
                    interval_width = interval_width,
                    changepoint_range = changepoint_range)
        m = m.fit(dataframe)
        forecast = m.predict(dataframe)
        forecast['fact'] = dataframe['y'].reset_index(drop = True)
        return forecast, m

    def detect_anomalies(self, forecast):
        forecasted = forecast.copy()
        forecasted['anomaly'] = 0
        forecasted.loc[forecasted['fact'] > forecasted['yhat_upper'], 'anomaly'] = 1
        forecasted.loc[forecasted['fact'] < forecasted['yhat_lower'], 'anomaly'] = -1
        #anomaly importances
        forecasted['importance'] = 0
        forecasted.loc[forecasted['anomaly'] ==1, 'importance'] = \
            (forecasted['fact'] - forecasted['yhat_upper'])/forecast['fact']
        forecasted.loc[forecasted['anomaly'] ==-1, 'importance'] = \
            (forecasted['yhat_lower'] - forecasted['fact'])/forecast['fact']
  
        return forecasted