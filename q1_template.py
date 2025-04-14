# -*- coding: utf-8 -*-

# Enter your candidate ID here:
# Enter your student ID here:
# Do NOT enter your name

# 4QQMN506 Coursework Q1
#%%
"""
The data provided is from https://data.worldbank.org/
world_bank.csv is Indicator ID FP.CPI.TOTL.ZG for Inflation, consumer prices (annual %)
The world_bank_countries.csv is a list of the world bank countries and continents. 

"""
#%% a) Load world_bank.csv and world_bank_countries.csv into two separate DataFrames 
# called wb_data and wb_country_data
import pandas as pd
import numpy as np
wb_data = pd.read_csv('./Q1 data/world_bank.csv')
wb_country_data = pd.read_csv('./Q1 data/world_bank_countries.csv')
# print(wb_data.head())
# print(wb_country_data.head(10))
#%% b) Plot a line graph of the Poland Inflation Data for all dates from the wb_data DataFrame.  
import matplotlib.pyplot as plt
poland_data = wb_data[wb_data['country'] == 'Poland']

plt.figure(figsize=(15, 8))
poland_data.plot(x='year', y='FP.CPI.TOTL.ZG', kind='line', 
                color='black')

plt.title('Poland Inflation FP.CPI.TOTL.ZG')
plt.xlabel('Year')
plt.ylabel('Inflation in(%)')
plt.grid(True, linestyle='--')
plt.xticks(rotation=45)
plt.show()


#%% c) Plot a line graph of the High Income, Low & Middle Income, Low Income, 
# Lower middle income, Middle Income and Upper Middle Income for all dates 
# from the wb_data DataFrame. 
import matplotlib.pyplot as plt
income_group_types = ['High income', 'Low & middle income', 'Low income', 
                'Lower middle income', 'Middle income', 'Upper middle income']
income_data = wb_data[wb_data['country'].isin(income_group_types)]
income_pivot = income_data.pivot(index='year', columns='country', values='FP.CPI.TOTL.ZG')
income_pivot = income_pivot.sort_index()
plt.figure(figsize=(15, 8))
for group in income_group_types:
    if group in income_pivot.columns:
        plt.plot(income_pivot.index, income_pivot[group], marker='o', linestyle='-', label=group)

plt.title('Inflation Rate by Income Group', fontsize=14)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Inflation (%)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(title='Income Group Types', fontsize=10)
plt.xticks(rotation=45)
plt.show()

#%% d) Calculate the mean for all countries, sort from highest to lowest and 
# plot the top 10 in a bar chart using matplotlib. 
# Exclude aggregates like income groups and regions
# First, identify all aggregates to exclude (income groups plus regions/groups)
# Income groups already defined earlier
import matplotlib.pyplot as plt
wb_country_info = pd.read_csv('./Q1 data/world_bank_countries.csv')
aggregates = wb_country_info[wb_country_info['region'] == 'Aggregates']['name'].tolist()

income_groups = ['High income', 'Low & middle income', 'Low income', 
                'Lower middle income', 'Middle income', 'Upper middle income']
aggregates.extend(income_groups)
regional_aggregates = [
    'World', 'Arab World', 'Caribbean small states', 'Central Europe and the Baltics',
    'Early-demographic dividend', 'East Asia & Pacific', 'Europe & Central Asia', 
    'Euro area', 'European Union', 'Fragile and conflict affected situations',
    'Heavily indebted poor countries (HIPC)', 'IBRD only', 'IDA & IBRD total',
    'IDA blend', 'IDA only', 'IDA total', 'Late-demographic dividend',
    'Latin America & Caribbean', 'Least developed countries: UN classification',
    'Middle East & North Africa', 'North America', 'OECD members', 'Other small states',
    'Pacific island small states', 'Post-demographic dividend', 'Pre-demographic dividend',
    'Small states', 'South Asia', 'Sub-Saharan Africa'
]
aggregates.extend(regional_aggregates)
aggregate_patterns = ['excluding high income', 'IDA & IBRD countries']
country_data = wb_data[~wb_data['country'].isin(aggregates)]
for pattern in aggregate_patterns:
    country_data = country_data[~country_data['country'].str.contains(pattern, na=False)]

country_means = country_data.groupby('country')['FP.CPI.TOTL.ZG'].mean().reset_index()
country_means = country_means.sort_values('FP.CPI.TOTL.ZG', ascending=False)
top_10 = country_means.head(10)

plt.figure(figsize=(14, 8))
bars = plt.bar(top_10['country'], top_10['FP.CPI.TOTL.ZG'], color='blue')

plt.title('Top 10 Countries with Mean Inflation Rate', fontsize=16)
plt.xlabel('Country', fontsize=12)
plt.ylabel('Mean Inflation Rate (%)', fontsize=12)
plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.xticks(rotation=45, ha='right')
plt.show()

print("Top 10 countries with highest mean inflation:")
for i, (country, rate) in enumerate(zip(top_10['country'], top_10['FP.CPI.TOTL.ZG'])):
    print(f"{i}. {country}: {rate}%")

#%% e) What are the 5 countries with the lowest inflation data in 2020?
# Filter for 2020 data

import matplotlib.pyplot as plt

data_2020 = wb_data[wb_data['year'] == 2020]
aggregates = wb_country_info[wb_country_info['region'] == 'Aggregates']['name'].tolist()
income_groups = ['High income', 'Low & middle income', 'Low income', 
                'Lower middle income', 'Middle income', 'Upper middle income']
aggregates.extend(income_groups)
regional_aggregates = [
    'World', 'Arab World', 'Caribbean small states', 'Central Europe and the Baltics',
    'Early-demographic dividend', 'East Asia & Pacific', 'Europe & Central Asia', 
    'Euro area', 'European Union', 'Fragile and conflict affected situations',
    'Heavily indebted poor countries (HIPC)', 'IBRD only', 'IDA & IBRD total',
    'IDA blend', 'IDA only', 'IDA total', 'Late-demographic dividend',
    'Latin America & Caribbean', 'Least developed countries: UN classification',
    'Middle East & North Africa', 'North America', 'OECD members', 'Other small states',
    'Pacific island small states', 'Post-demographic dividend', 'Pre-demographic dividend',
    'Small states', 'South Asia', 'Sub-Saharan Africa'
]
aggregates.extend(regional_aggregates)
countries_2020 = data_2020[~data_2020['country'].isin(aggregates)]
aggregate_patterns = ['excluding high income', 'IDA & IBRD countries']
for pattern in aggregate_patterns:
    countries_2020 = countries_2020[~countries_2020['country'].str.contains(pattern, na=False)]
lowest_inflation_2020 = countries_2020.sort_values('FP.CPI.TOTL.ZG').head(5)

print("Five countries with the lowest inflation during 2020")
for i, (country, inflation) in enumerate(zip(lowest_inflation_2020['country'], 
                                           lowest_inflation_2020['FP.CPI.TOTL.ZG']), 1):
    print("Country" + f" {i}: {country} with inflation rate: {inflation}%")

#%% f) How many countries are stated with a capital city in the world_bank_countries.csv?
countries_with_capital = wb_country_data[wb_country_data['capitalCity'] != ''].shape[0]
print(f"No of countries with a capital city: {countries_with_capital}")

#%% g) The Haversine formula is a widely used method for calculating the distance between two points on the
# surface of a sphere (like the Earth) given their latitude and longitude coordinates. 
# The longitude range is from -180 to 180 degrees and the latitude range is from -90 to 90 degrees. 
# The latitude and longitude values for each country with a capital are stated in world_bank_countries.csv. 
# Our reference point is 0 longitude and 0 latitude. What capital is the furthest away from the reference point?

from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
    
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371
    return c * r


capitals = wb_country_data[wb_country_data['capitalCity'] != ''].dropna(subset=['longitude', 'latitude'])

capitals['distance'] = capitals.apply(
    lambda row: haversine(0, 0, row['longitude'], row['latitude']), axis=1
)

furthest_capital = capitals.loc[capitals['distance'].idxmax()]
print(f"The furthest city from coordinated (0,0) is {furthest_capital['capitalCity']} ({furthest_capital['name']}) with a distance of {furthest_capital['distance']:.2f} km")
#%% h) Calculate the difference in annual mean from the highest country obtained in part d 
#and the remotest country obtained in part g)

highest_inflation_country = top_10.iloc[0]['country']
highest_inflation_mean = top_10.iloc[0]['FP.CPI.TOTL.ZG']

print(f"Country with highest mean inflation: {highest_inflation_country} with {highest_inflation_mean:.2f}%")

# Get the remotest country from part g
remotest_country = furthest_capital['name']
print(f"Remotest country: {remotest_country}")

remotest_country_data = wb_data[wb_data['country'] == remotest_country]

remotest_country_mean = remotest_country_data['FP.CPI.TOTL.ZG'].mean()
print(f"Mean inflation for {remotest_country}: {remotest_country_mean}%")

difference = highest_inflation_mean - remotest_country_mean
print(f"Difference in annual mean inflation: {difference}%")



# %%
