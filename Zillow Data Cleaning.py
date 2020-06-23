#!/usr/bin/env python
# coding: utf-8

# In[2]:


from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
import csv
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
from bs4 import BeautifulSoup 
import time


# In[3]:


df=pd.read_csv('sandiego_output.csv')
df.head()


# In[4]:


df.info()


# ### data cleaning steps
- heatmap NA- drop NA
- 'area' columns: rename ,,area in sqft"
- drop column 'addressCity' and 'addressState'
- rename 'price' column: 'monthly price in $'
- 'price' column: remove ,,$" and ,,/mo" ,,+/mo", remove comma
- every column = convert to numeric
# In[6]:


#check for missing values
#before cleaning: 840 entries
df.isna()


# In[7]:


#check for missing values
#same dataset missing: are, baths, beds, price
sns.heatmap(df.isna(), yticklabels=False,cbar=False,cmap='Greens')


# In[8]:


df=df.dropna()


# In[10]:


df.info()
#after cleaning: 485 entries (more than 40% of the data were dropped)


# In[12]:


#after dropping missing data we have no non-null values anymore
sns.heatmap(df.isna(), yticklabels=False,cbar=False,cmap='Greens')


# In[13]:


#change column name from 'area' to 'area in sqft'
df['area in sqft']= df['area']


# In[14]:


df.head()


# In[15]:


#drop the 'addressCity' and 'addressState' column because every entry is related to San Diego and California
df.drop(['addressCity', 'addressState'], axis=1, inplace=True)


# In[16]:


df.head()


# In[17]:


#reset the index since rows were deleted during the dropping missing value process
df=df.reset_index(drop=True)


# In[18]:


df.head()


# In[19]:


#rename column from 'price' to 'monthly price in $'
df['monthly price in $']=df['price']


# In[20]:


df.head()


# In[21]:


# remove entries with '/mo', 'mo', '+' inside the 'monthly price in $' columns

def modify_price(x):
    if '/mo' in x:
        return x.strip('/mo')
    elif '+/mo' in x:
        return x.strip('+/mo')
    elif '+' in x:
        return x.split('+')[0]
    else:
        return x


# In[22]:


#apply the 'modify_price' function
df['monthly price in $']=df['monthly price in $'].apply(modify_price)


# In[24]:


#modification: remove '$' sign from the 'monthly price in $' entries

def remove_dollar_sign(x):
    for i in x:
        if '$' in x:
            return x.replace('$','')
        else:
            return x


# In[26]:


#apply the 'remove_dollar_sign' function
df['monthly price in $']=df['monthly price in $'].apply(remove_dollar_sign)


# In[28]:


#check the current dataframe 
df.head()


# In[29]:


#drop columns: 'area', 'price' since we renamed them


# In[30]:


df.drop(['area', 'price'], axis=1, inplace=True)


# In[31]:


#check the current dataframe 
df.head()


# In[32]:


#change column order
df=df[['area in sqft', 'baths', 'beds', 'latitude', 'longitude', 'monthly price in $']]


# In[33]:


df.head()


# In[34]:


# remove the comma inside the 'monthly price in $' column

def remove_comma(x):
    for i in x:
        if ',' in x:
            return x.replace(',','')
        else:
            return x


# In[37]:


#apply the 'remove_underscore' function
df['monthly price in $']=df['monthly price in $'].apply(remove_comma)


# In[40]:


#convert the 'monthly price in $' column to float
df['monthly price in $']=df['monthly price in $'].astype(float)


# In[273]:


#check the dataframe infos- now every column is a float type
df.info()


# In[42]:


#check the modified dataframe 
df.head()


# In[ ]:


#save as csv file
df.to_csv('Zillow_cleaned_data.csv')

