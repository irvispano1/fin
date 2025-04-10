
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
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def transform_to_timeseries(file_path, sheet_name=0):
    """
    Transforms data from Excel file to a pandas time series.
    
    Parameters:
    file_path (str): Path to the Excel file
    sheet_name: Sheet to read (default=0, first sheet)
    
    Returns:
    pandas.DataFrame: DataFrame with a datetime index
    """
    # Read the Excel file
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    
    # Check if data is in wide format (years in rows, months in columns)
    if 'Jan' in df.columns and 'Year' in df.columns:
        # Create an empty list to store the transformed data
        data_list = []
        
        # Iterate through each row (year) and extract monthly values
        for _, row in df.iterrows():
            year = row['Year']
            for month, month_name in enumerate(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                                               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], 1):
                if month_name in df.columns and not pd.isna(row[month_name]):
                    # Create a date for this year and month
                    date = pd.Timestamp(year=int(year), month=month, day=1)
                    data_list.append({'Date': date, 'Unemployment_Rate': row[month_name]})
        
        # Create a DataFrame from the list
        ts_df = pd.DataFrame(data_list)
        ts_df.set_index('Date', inplace=True)
        
        # Sort index to ensure chronological order
        ts_df = ts_df.sort_index()
        
        return ts_df
    
    # Original code for the other format with Year, Period, Value columns    
    elif 'Year' in df.columns and 'Period' in df.columns and 'Value' in df.columns:
        # Convert Month abbreviation (e.g., 'M01') to month number
        df['Month'] = df['Period'].str.replace('M', '').astype(int)
        
        # Create a datetime index
        df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month'].astype(str) + '-01')
        
        # Set the Date as the index and keep only the Value column
        ts_df = df.set_index('Date')[['Value']]
        
        # Rename the column to be more descriptive
        ts_df.rename(columns={'Value': 'Unemployment_Rate'}, inplace=True)
        
        return ts_df
    else:
        print("Error: Expected columns format not recognized.")
        print("Available columns:", df.columns)
        return None

# Apply the function to the unemployment data
unemployment_file = './Q2 data/LNS14000000.xlsx'
unemployment_ts = transform_to_timeseries(unemployment_file)

# Plot the time series
if unemployment_ts is not None:
    plt.figure(figsize=(14, 7))
    unemployment_ts.plot(title='US Unemployment Rate Over Time', 
                        grid=True, 
                        color='blue',
                        linewidth=1.5)
    plt.xlabel('Date')
    plt.ylabel('Unemployment Rate (%)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    
    # Display the first few rows of the transformed data
    print("Transformed Unemployment Rate Data (First 5 rows):")
    print(unemployment_ts.head(111))



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

# Find the maximum unemployment rate and its date
max_unemployment = unemployment_ts['Unemployment_Rate'].max()
max_date = unemployment_ts['Unemployment_Rate'].idxmax()

# Find the minimum unemployment rate and its date
min_unemployment = unemployment_ts['Unemployment_Rate'].min()
min_date = unemployment_ts['Unemployment_Rate'].idxmin()

# Print the results with formatted dates and values
print(f"Maximum Unemployment Rate: {max_unemployment:.1f}% on {max_date.strftime('%B %Y')}")
print(f"Minimum Unemployment Rate: {min_unemployment:.1f}% on {min_date.strftime('%B %Y')}")

# Create a visualization highlighting the extremes
plt.figure(figsize=(14, 7))
unemployment_ts.plot(title='US Unemployment Rate with Maximum and Minimum Points', 
                     grid=True, 
                     color='blue',
                     linewidth=1.5)

# Mark the maximum point
plt.plot(max_date, max_unemployment, 'ro', markersize=10)
plt.annotate(f'Max: {max_unemployment:.1f}%\n{max_date.strftime("%b %Y")}', 
             xy=(max_date, max_unemployment),
             xytext=(30, 20),
             textcoords='offset points',
             arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2'))

# Mark the minimum point
plt.plot(min_date, min_unemployment, 'go', markersize=10)
plt.annotate(f'Min: {min_unemployment:.1f}%\n{min_date.strftime("%b %Y")}', 
             xy=(min_date, min_unemployment),
             xytext=(30, -30),
             textcoords='offset points',
             arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2'))

plt.xlabel('Date')
plt.ylabel('Unemployment Rate (%)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()



#%% d) Now calculate the average yearly unemployment for all years and
# plot a line chart where the date axis is the year.

# Extract the year from the datetime index
unemployment_ts['Year'] = unemployment_ts.index.year

# Group by year and calculate the mean unemployment rate
yearly_avg = unemployment_ts.groupby('Year')['Unemployment_Rate'].mean()

# Create a DataFrame with yearly averages
yearly_df = pd.DataFrame({'Year': yearly_avg.index, 'Average_Unemployment': yearly_avg.values})

# Set the year as the index
yearly_df.set_index('Year', inplace=True)

# Exclude 2024 since we don't have complete data for the year
yearly_df = yearly_df[yearly_df.index < 2024]

# Create the line plot
plt.figure(figsize=(12, 6))
plt.plot(yearly_df.index, yearly_df['Average_Unemployment'], marker='o', linestyle='-', color='navy')

# Enhance the plot
plt.title('Average Yearly US Unemployment Rate (1948-2023)', fontsize=16)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Average Unemployment Rate (%)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)

# Add value annotations for key recession periods
# 1981-1982 recession
plt.annotate('1981-1982\nRecession', xy=(1982, yearly_df.loc[1982, 'Average_Unemployment']),
             xytext=(5, 25), textcoords='offset points', arrowprops=dict(arrowstyle='->'))

# 2008-2009 Great Recession
plt.annotate('2008-2009\nGreat Recession', xy=(2009, yearly_df.loc[2009, 'Average_Unemployment']),
             xytext=(5, 25), textcoords='offset points', arrowprops=dict(arrowstyle='->'))

# 2020 COVID-19 pandemic
plt.annotate('COVID-19\nPandemic', xy=(2020, yearly_df.loc[2020, 'Average_Unemployment']),
             xytext=(5, 25), textcoords='offset points', arrowprops=dict(arrowstyle='->'))

# Set appropriate y-axis limits with some padding
plt.ylim(0, yearly_df['Average_Unemployment'].max() * 1.1)

# Add horizontal lines at notable unemployment levels
plt.axhline(y=4, color='green', linestyle='--', alpha=0.5, label='Full Employment (~4%)')
plt.axhline(y=8, color='orange', linestyle='--', alpha=0.5, label='High Unemployment (8%)')

plt.legend()
plt.tight_layout()
plt.show()

# Print the highest yearly average
max_year = yearly_df['Average_Unemployment'].idxmax()
max_avg = yearly_df.loc[max_year, 'Average_Unemployment']
print(f"The highest yearly average unemployment was {max_avg:.2f}% in {max_year}")

# Print the lowest yearly average
min_year = yearly_df['Average_Unemployment'].idxmin()
min_avg = yearly_df.loc[min_year, 'Average_Unemployment']
print(f"The lowest yearly average unemployment was {min_avg:.2f}% in {min_year}")


#%% e) Why do we want to exclude 2024 from part d? 

#We exclude 2024 because we do not have complete data for that year.


#%% f) Import the CUUR0000SA0.xlsx and PRS85006152.xlsx to separate DataFrames. 
#See details provided. Using your transform
# function from part a, also transform these data files to a time series. 
#Join the unemployment, cpi and total nonfarm into a single 
#DataFrame. Due to the units, set a secondary axis and plot three 
#separate line graphs comparing each economic time series from 2000 until current.

# Import the CPI and Total Nonfarm Employment data
cpi_file = './Q2 data/CUUR0000SA0.xlsx'
nonfarm_file = './Q2 data/CES0000000001.xlsx'

# Transform data using the same function from part a
cpi_ts = transform_to_timeseries(cpi_file)
if cpi_ts is not None and 'Unemployment_Rate' in cpi_ts.columns:
    cpi_ts.rename(columns={'Unemployment_Rate': 'CPI'}, inplace=True)

nonfarm_ts = transform_to_timeseries(nonfarm_file)
if nonfarm_ts is not None and 'Unemployment_Rate' in nonfarm_ts.columns:
    nonfarm_ts.rename(columns={'Unemployment_Rate': 'Nonfarm_Employment'}, inplace=True)

# Display the first few rows of each dataset
print("CPI Data (First 5 rows):")
if cpi_ts is not None:
    print(cpi_ts.head())
else:
    print("CPI data could not be loaded.")

print("\nNonfarm Employment Data (First 5 rows):")
if nonfarm_ts is not None:
    print(nonfarm_ts.head())
else:
    print("Nonfarm employment data could not be loaded.")

# Join the datasets into a single DataFrame
if cpi_ts is not None and nonfarm_ts is not None:
    # Join the dataframes
    combined_data = unemployment_ts.join([cpi_ts, nonfarm_ts], how='outer')
    
    # Filter for data from 2000 onwards
    combined_data = combined_data[combined_data.index >= '2000-01-01']
    
    # Create a multi-series plot with secondary axes
    fig, ax1 = plt.subplots(figsize=(16, 8))
    
    # Primary axis - Unemployment Rate
    color1 = 'tab:blue'
    ax1.set_xlabel('Date', fontsize=12)
    ax1.set_ylabel('Unemployment Rate (%)', color=color1, fontsize=12)
    ax1.plot(combined_data.index, combined_data['Unemployment_Rate'], 
             label='Unemployment Rate (%)', color=color1, linewidth=2)
    ax1.tick_params(axis='y', labelcolor=color1)
    
    # Secondary axis 1 - CPI
    ax2 = ax1.twinx()
    color2 = 'tab:red'
    ax2.set_ylabel('Consumer Price Index', color=color2, fontsize=12)
    ax2.plot(combined_data.index, combined_data['CPI'], 
             label='CPI', color=color2, linewidth=2, linestyle='--')
    ax2.tick_params(axis='y', labelcolor=color2)
    
    # Secondary axis 2 - Nonfarm Employment
    ax3 = ax1.twinx()
    # Offset the secondary axis to the right
    ax3.spines["right"].set_position(("axes", 1.1))
    color3 = 'tab:green'
    ax3.set_ylabel('Nonfarm Employment', color=color3, fontsize=12)
    ax3.plot(combined_data.index, combined_data['Nonfarm_Employment'], 
             label='Nonfarm Employment', color=color3, linewidth=2, linestyle='-.')
    ax3.tick_params(axis='y', labelcolor=color3)
    
    # Add title and legend
    plt.title('US Economic Indicators (2000-Present)', fontsize=16)
    
    # Create custom legend to include all series
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    lines3, labels3 = ax3.get_legend_handles_labels()
    lines = lines1 + lines2 + lines3
    labels = labels1 + labels2 + labels3
    ax1.legend(lines, labels, loc='upper center', bbox_to_anchor=(0.5, -0.1), 
               shadow=True, ncol=3, fontsize=10)
    
    # Highlight recession periods
    # 2008-2009 Great Recession
    ax1.axvspan('2007-12-01', '2009-06-30', alpha=0.2, color='gray', label='Great Recession')
    
    # 2020 COVID-19 pandemic
    ax1.axvspan('2020-02-01', '2020-04-30', alpha=0.2, color='darkgray', label='COVID-19 Shutdown')
    
    # Improve layout and show plot
    plt.tight_layout()
    plt.grid(True, alpha=0.3)
    plt.show()
    
    # Also create individual plots for clearer comparison
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(16, 12), sharex=True)
    
    # Unemployment Rate
    ax1.plot(combined_data.index, combined_data['Unemployment_Rate'], color='blue', linewidth=2)
    ax1.set_ylabel('Unemployment Rate (%)', fontsize=12)
    ax1.set_title('US Unemployment Rate (2000-Present)', fontsize=14)
    ax1.grid(True, alpha=0.3)
    
    # Consumer Price Index
    ax2.plot(combined_data.index, combined_data['CPI'], color='red', linewidth=2)
    ax2.set_ylabel('Consumer Price Index', fontsize=12)
    ax2.set_title('US Consumer Price Index (2000-Present)', fontsize=14)
    ax2.grid(True, alpha=0.3)
    
    # Nonfarm Employment
    ax3.plot(combined_data.index, combined_data['Nonfarm_Employment'], color='green', linewidth=2)
    ax3.set_ylabel('Nonfarm Employment', fontsize=12)
    ax3.set_title('US Nonfarm Employment (2000-Present)', fontsize=14)
    ax3.grid(True, alpha=0.3)
    
    # Improve x-axis formatting
    ax3.set_xlabel('Date', fontsize=12)
    plt.xticks(rotation=45)
    
    # Highlight recession periods on all subplots
    for ax in [ax1, ax2, ax3]:
        # 2008-2009 Great Recession
        ax.axvspan('2007-12-01', '2009-06-30', alpha=0.2, color='gray')
        
        # 2020 COVID-19 pandemic
        ax.axvspan('2020-02-01', '2020-04-30', alpha=0.2, color='darkgray')
    
    plt.tight_layout()
    plt.show()
else:
    print("Unable to create combined plots due to missing data.")


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