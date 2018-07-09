
# coding: utf-8

# In[1]:


import matplotlib.pyplot as plt
import requests
import pandas as pd
from pprint import pprint
from api_key import weather_api
from random import uniform
from citipy import citipy
import numpy as np


# In[2]:


coordinate=[]
cities=[]


# In[3]:


def newpoint():
   return uniform(-90,90), uniform(-180, 180)

points = (newpoint() for x in range(1500))
for point in points:
   coordinate.append(point)


# In[4]:


for coordinate_pair in coordinate:
    lat, lon = coordinate_pair
    city=citipy.nearest_city(lat, lon)
    cities.append(city.city_name)


# In[5]:


df_cities=pd.DataFrame({'City':cities})
print(len(df_cities))
df_cities=df_cities.drop_duplicates('City')
print(len(df_cities))


# In[6]:


url = "http://api.openweathermap.org/data/2.5/weather"
params = {
    'appid': weather_api,
    'units': 'imperial'
    }


# In[7]:


temp=[]
cloud=[]
wind=[]
humid=[]
lat=[]
long=[]


# In[8]:


for city in df_cities['City']:
    params['q'] = city
    response = requests.get(url, params=params).json()

    try:
        temp.append(response['main']['temp'])
        wind.append(response['wind']['speed'])
        cloud.append(response['clouds']['all'])
        humid.append(response['main']['humidity'])
        lat.append(response['coord']['lat'])
        long.append(response['coord']['lon'])
    except KeyError:
        temp.append('NaN')
        wind.append('NaN')
        cloud.append('NaN')
        humid.append('NaN')
        lat.append('NaN')
        long.append('NaN')
    
    print(response)


# In[9]:


len(lat)


# In[10]:


df_cities['Lat']=lat
df_cities['Long']=long
df_cities['Temp']=temp
df_cities['Cloud']=cloud
df_cities['Wind']=wind
df_cities['Humidity']=humid

df_cities.head()


# In[11]:


df_final_cities = df_cities[df_cities.Lat != 'NaN']


# In[12]:


len(lat)


# In[13]:


df_final_cities = df_final_cities.rename(columns={'City':'Cities',
                                                  'Lat':'Latitude',
                                                  'Long':'Longitude',
                                                  'Temp':'Temperature (F)',
                                                  'Cloud':'Cloudiness (%)',
                                                  'Wind':'Wind Speed (mph)',
                                                  'Humidity':'Humidity (%)'})
df_final_cities.head()


# In[14]:


plt.scatter(df_final_cities['Temperature (F)'], df_final_cities['Latitude'])
plt.title("Temperature (F) vs. Latitude")
plt.xlabel("Temperature (F)")
plt.ylabel("Latitude")
plt.show()
plt.savefig('temp_lat.png')


# In[15]:


plt.scatter(df_final_cities['Humidity (%)'], df_final_cities['Latitude'])
plt.title("Humidity (%) vs. Latitude")
plt.xlabel("Humidity (%)")
plt.ylabel("Latitude")
plt.show()
plt.savefig('humid_lat.png')


# In[16]:


plt.scatter(df_final_cities['Cloudiness (%)'], df_final_cities['Latitude'])
plt.title("Cloudiness (%) vs. Latitude")
plt.xlabel("Cloudiness (%)")
plt.ylabel("Latitude")
plt.show()
plt.savefig('cloud_lat.png')


# In[17]:


plt.scatter(df_final_cities['Wind Speed (mph)'], df_final_cities['Latitude'])
plt.title("Wind Speed (mph) vs. Latitude")
plt.xlabel("Wind Speed (mph)")
plt.ylabel("Latitude")
plt.show()
plt.savefig('wind_lat.png')


# In[18]:


df_final_cities.to_csv('final_weather_cities.csv')

