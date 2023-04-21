#!/usr/bin/env python
# coding: utf-8

# In[1]:


# To inscrease the limit of Anaconda. From Anaconda prompt, type 
# jupyter notebook --NotebookApp.iopub_data_rate_limit=1e+10

#This example uses Python 2.7 and the python-request library.
import pandas as pd
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

# Create function to run API

def api_runner():
    global df
    # Link: https://coinmarketcap.com/api/documentation/v1/#section/Authentication
    # Authentication - Using Your API Key
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
      'start':'1',
      'limit':'15',
      'convert':'GBP'
    }

    # API Key https://pro.coinmarketcap.com/account
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': 'da7f3c28-00f1-4567-8c1b-43e41be6732e',
    }

    session = Session()
    session.headers.update(headers)

    try:
      response = session.get(url, params=parameters)
      data = json.loads(response.text)
      print(data)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)
    
    # Normalizing from original data with dictionary type to pandas table tyoe
    df2 = pd.json_normalize(data['data'])
    df2['Timestamp'] = pd.to_datetime('now')
    df = pd.DataFrame()
    df = pd.concat([df, df2], ignore_index=True)
    return df
df_raw = api_runner()


# In[2]:


# import os 
# from time import time
# from time import sleep

# for i in range(333):
#     api_runner()
#     print('API Runner completed')
#     sleep(60) #sleep for 1 minute
# exit()


# In[3]:


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)
# df_raw


# In[4]:


# reset the scientific numbers from dataframe to readable float numbers
pd.set_option('display.float_format', lambda x: '%.2f' % x)
df2 = df_raw.groupby('name', sort=False)[['quote.GBP.percent_change_1h','quote.GBP.percent_change_24h',
                                      'quote.GBP.percent_change_7d','quote.GBP.percent_change_30d',
                                      'quote.GBP.percent_change_60d','quote.GBP.percent_change_90d']].mean()


# In[5]:


# pivot dataframe by using 
# stack - series - dataframe
# need to reset index to rearrange the column names to right position
df3 = df2.stack().to_frame(name = 'values').reset_index().rename(columns = {'level_1':'percent_change'})


# In[6]:


# replace values long values like "quote.GBP.percent_change_" to shorter values
df3 = df3.replace('quote.GBP.percent_change_','', regex=True)
# df4 = df2.replace(regex=['quote.GBP.percent_change_'], value='')   
df3


# In[7]:


import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
# change color of the plot
palette = ["#F72585", "#7209B7", "#3A0CA3", "#4361EE", "#4CC9F0"]
cat_plot = sns.catplot(x='percent_change', y='values', 
                    hue='name', data=df3, kind='point', 
                    palette = palette)

cat_plot.set(title='Categorical plots show the percentage of cryptos prices change through period of time', 
             xlabel = 'Percent change', ylabel= '%')


# In[8]:


# hue='name' is showing the name of columns
bar_plot = sns.barplot(x='percent_change', y='values',
                       data=df3, estimator = np.median,
                       errorbar=('ci', 0),palette = palette,hue='name')

bar_plot = bar_plot.set(title='Bar chart indicates the percentage of cryptos prices change through period of time', 
             xlabel = 'Percent change', ylabel= '%')
# Change the legend box from inside the chart to outside
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)


# In[9]:


df4 = df_raw[['name','quote.GBP.price','Timestamp']]
df4 = df4.query("name == 'Bitcoin'")
df4


# In[10]:


sns.lineplot(x = 'Timestamp', y = 'quote.GBP.price', hue = 'name',data = df4 ,palette = palette)

