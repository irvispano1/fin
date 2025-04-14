
# -*- coding: utf-8 -*-

# Enter your candidate ID here:
# Enter your student ID here:
# Do NOT enter your name

# 4QQMN506 Coursework Q2


#%% Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#%% a) Import the LNS14000000.xlsx to a pandas DataFrame. See details provided. 
#Write a function to transform the unemployment rate to a time series. 
# Plot a line chart of the unemployment data. 


def transform_to_timeseries(file_path, sheet_name=0):
    df = pd.read_excel(file_path, sheet_name=sheet_name) 
    data_list = []
    for _, row in df.iterrows():
        year = row['Year']
        for month, month_name in enumerate(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                                            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], 1):
            if month_name in df.columns and not pd.isna(row[month_name]):
                date = pd.Timestamp(year=int(year), month=month, day=1)
                data_list.append({'Date': date, 'Unemployment_Rate': row[month_name]})
    ts_df = pd.DataFrame(data_list)
    ts_df.set_index('Date', inplace=True)
    ts_df = ts_df.sort_index()
    
    return ts_df

unemployment_file = './Q2 data/LNS14000000.xlsx'
unemployment_ts = transform_to_timeseries(unemployment_file)

if unemployment_ts is not None:
    plt.figure(figsize=(14, 7))
    unemployment_ts.plot(title='Unemployment Rate', 
                        grid=True, 
                        color='blue',
                        linewidth=1.5)
    plt.xlabel('Date')
    plt.ylabel('Unemployment Rate (%)')
    plt.xticks(rotation=45)
    plt.show()
    print("Transformed Unemployment Rate Data (First 100 rows):")
    print(unemployment_ts.head(100))



#%%  b) Are there any interesting observations you can deduce from this plot? 
#Write answer as a comment.

# Based on the provide plot we can observe the following:

# We notice recessions periods followed by unenployment spikes and normal periods.
# Latest recession periods are 2008-2010 and during Covid 2020.
# Maximum unemployment rate was 14.7% in April 2020 during the COVID-19 pandemic.
# After covid spike unemployment rate got back to normal levels in extremely short time compared to other recessions.
# 2nd highest unemployment rate was nearly 10% in around 1982-1983, third highest was around 2009-2010.
# The unemployment rate has had a downward trend since the 1982-1983 recession.


#%% c) What is the max and min unemployment rates and on what dates. 
#Print results to screen. 

max_unemployment = unemployment_ts['Unemployment_Rate'].max()
max_date = unemployment_ts['Unemployment_Rate'].idxmax()

min_unemployment = unemployment_ts['Unemployment_Rate'].min()
min_date = unemployment_ts['Unemployment_Rate'].idxmin()

print(f"Maximum Unemployment Rate: {max_unemployment:.1f}% on {max_date.strftime('%B %Y')}")
print(f"Minimum Unemployment Rate: {min_unemployment:.1f}% on {min_date.strftime('%B %Y')}")



#%% d) Now calculate the average yearly unemployment for all years and
# plot a line chart where the date axis is the year.


unemployment_ts['Year'] = unemployment_ts.index.year
yearly_avg = unemployment_ts.groupby('Year')['Unemployment_Rate'].mean()
yearly_df = pd.DataFrame({'Year': yearly_avg.index, 'Average_Unemployment': yearly_avg.values})
yearly_df.set_index('Year', inplace=True)
yearly_df = yearly_df[yearly_df.index < 2024]
plt.figure(figsize=(12, 6))
plt.plot(yearly_df.index, yearly_df['Average_Unemployment'], marker='o', linestyle='-', color='blue', linewidth=2)
plt.title('Avg Yearly US Unemployment Rate', fontsize=16)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Avg Unemployment Rate (%)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.ylim(0, yearly_df['Average_Unemployment'].max() * 1.1)
plt.legend()
plt.show()


#%% e) Why do we want to exclude 2024 from part d? 

#We exclude 2024 because we do not have complete data for that year.


#%% f) Import the CUUR0000SA0.xlsx and PRS85006152.xlsx to separate DataFrames. 
#See details provided. Using your transform
# function from part a, also transform these data files to a time series. 
#Join the unemployment, cpi and total nonfarm into a single 
#DataFrame. Due to the units, set a secondary axis and plot three 
#separate line graphs comparing each economic time series from 2000 until current.


cpi_file = './Q2 data/CUUR0000SA0.xlsx'
nonfarm_file = './Q2 data/CES0000000001.xlsx'


cpi_timeseries = transform_to_timeseries(cpi_file)
if cpi_timeseries is not None and 'Unemployment_Rate' in cpi_timeseries.columns:
    cpi_timeseries.rename(columns={'Unemployment_Rate': 'CPI'}, inplace=True)

nonfarm_ts = transform_to_timeseries(nonfarm_file)
if nonfarm_ts is not None and 'Unemployment_Rate' in nonfarm_ts.columns:
    nonfarm_ts.rename(columns={'Unemployment_Rate': 'Nonfarm_Employment'}, inplace=True)
print("Cpi Timeseries :")
print(cpi_timeseries.head())


print("\nNonfarm Employment ")

print(nonfarm_ts.head())



    
combined_data = unemployment_ts.join([cpi_timeseries, nonfarm_ts], how='outer')


combined_data = combined_data[combined_data.index >= '2000-01-01']


fig, ax1 = plt.subplots(figsize=(16, 8))
color1 = 'tab:blue'
ax1.set_xlabel('Date', fontsize=12)
ax1.set_ylabel('Unemployment Rate (%)', color=color1, fontsize=12)
ax1.plot(combined_data.index, combined_data['Unemployment_Rate'], 
            label='Unemployment Rate (%)', color=color1, linewidth=2)
ax1.tick_params(axis='y', labelcolor=color1)
ax2 = ax1.twinx()
color2 = 'tab:red'
ax2.set_ylabel('Consumer Price Index', color=color2, fontsize=12)
ax2.plot(combined_data.index, combined_data['CPI'], 
            label='CPI', color=color2, linewidth=2, linestyle='--')
ax2.tick_params(axis='y', labelcolor=color2)
ax3 = ax1.twinx()

ax3.spines["right"].set_position(("axes", 1.1))
color3 = 'tab:green'
ax3.set_ylabel('Nonfarm Employment', color=color3, fontsize=12)
ax3.plot(combined_data.index, combined_data['Nonfarm_Employment'], 
            label='Nonfarm Employment', color=color3, linewidth=2, linestyle='-.')
ax3.tick_params(axis='y', labelcolor=color3)
plt.title('US Economic Indicators ', fontsize=16)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
lines3, labels3 = ax3.get_legend_handles_labels()
lines = lines1 + lines2 + lines3
labels = labels1 + labels2 + labels3
ax1.legend(lines, labels, loc='upper center', bbox_to_anchor=(0.5, -0.1), 
            shadow=True, ncol=3, fontsize=10)

plt.grid(True, alpha=0.3)
plt.show()






#%% g) What economic conclusions / observations can you make between these 
#three time series plots over the last 20 years? 
# Write your answer as a comment. Specifically discuss the 2020 to 2022 period.  

# Economic observations from the time series plots:

# 1. General patterns (2000-2020):
#    - Economic indicators show clear cyclical patterns corresponding to economic expansions and recessions
#    - The 2008-2009 Great Recession shows gradual deterioration and slow recovery in all metrics
#    - Prior to 2020, economic cycles followed predictable patterns with gradual changes

# 2. 2020-2022 COVID period observations:
#    - Unprecedented volatility: All three indicators showed extreme movements in a compressed timeframe
#    - Unemployment: Skyrocketed from ~3.5% to ~15% in just two months (March-April 2020), then recovered 
#      much faster than after previous recessions
#    - CPI: Initially dropped during early pandemic months, then showed dramatic inflation spike 
#      starting in early 2021, reaching levels not seen in decades
#    - Nonfarm Employment: Experienced severe contraction (loss of ~22 million jobs) followed by
#      relatively rapid but incomplete recovery

# 3. Unusual relationships during 2020-2022:
#    - Traditional economic relationships were disrupted - normally high unemployment correlates with 
#      low inflation, but 2021-2022 saw both high inflation and relatively higher unemployment
#    - Employment recovery occurred at different rates across sectors, unlike typical recessions
#    - The rapid recovery in employment and economic activity contributed to supply chain disruptions,
#      further fueling inflation

# 4. Policy influences (2020-2022):
#    - Unprecedented fiscal and monetary interventions (stimulus packages, expanded unemployment benefits,
#      low interest rates) likely accelerated the recovery of employment and consumption
#    - These same policies, combined with supply chain disruptions, contributed to the inflation surge
#    - The data reflects a policy tradeoff between supporting employment recovery and controlling inflation

# 5. Long-term implications:
#    - The COVID period represents a unique economic shock that doesn't follow traditional recession patterns
#    - The inflation surge that began in 2021 has forced policy responses (interest rate increases) that 
#      will influence economic indicators beyond the timeframe shown in these plots
#    - Labor market dynamics fundamentally changed with persistent mismatches between job openings and 
#      available workers, even as unemployment recovered


#%%