import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose

def is_holiday(date):
    return (date.month == 10 and date.day >= 3) or (date.month == 11 and date.day <= 7)  # Dashain and Tihar (3rd Oct - 7th Nov)


# Load the data
data = pd.read_csv('kalimati1.csv')
data['Date'] = pd.to_datetime(data['Date'])

# Find the first and last date
first_date = data['Date'].min()
last_date = data['Date'].max()


# Define selected commodities
selected_commodities = ['Cauli Local', 'Ginger', 'Potato Red', 'Carrot(Local)', 'Cabbage(Local)']

# Filter the DataFrame for the specified commodities
filtered_commodities = data[data['Commodity'].isin(selected_commodities)]

# Create the pivot table
pivot_table = filtered_commodities.pivot_table(index='Date', columns='Commodity', values='Average')

# Calculate the correlation matrix
correlation_matrix = pivot_table.corr()

# Sidebar for navigation
st.sidebar.title('Navigation')
pages = st.sidebar.selectbox('Select Page:', ['About Dataset', 'Question 1', 'Question 2', 'Question 3'])

# About Dataset
if pages == 'About Dataset':
    st.title('About Dataset')
    st.write("""
    This dataset contains daily average prices of various commodities sold at Kalimati Fruits and Vegetable Market in Kathmandu, Nepal. 
    The data includes information about the date, commodity type, minimum price, maximum price, and average price of each item. 
    The dataset is collected from the year 2013 to 2024.
    """)

    st.subheader('Dataset Overview')
    st.write(data.head())

    st.subheader('Statistical Summary')
    st.write(data.describe())

    st.write(f'##### First Date: {first_date}')
    st.write(f'##### Last Date: {last_date}')

    st.subheader('Selected Commodities')
    st.write(selected_commodities)

    st.write("## Correlation Matrix of Selected Commodities")

    # Plot heatmap for the correlation matrix
    fig, ax = plt.subplots(figsize=(15, 10))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', ax=ax)
    plt.title('Correlation Matrix of Commodity Prices')
    st.pyplot(fig)

    st.title('Price Distribution of Selected Commodities')

    for commodity in selected_commodities:
        subset = data[data['Commodity'] == commodity]['Average']
        st.subheader(f'Distribution of Prices for {commodity}')
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(subset, bins=30, kde=True, color='skyblue', ax=ax)
        ax.set_xlabel('Average Price')
        ax.set_ylabel('Frequency')
        ax.set_title(f'Distribution of Prices for {commodity}')
        st.pyplot(fig)

    st.title('Price Comparison: High vs Low Demand Periods')

    selected_data = data[data['Commodity'].isin(selected_commodities)]

    # Example: Comparing prices between summer (high demand) and winter (low demand) for selected commodities
    summer_data = selected_data[(selected_data['Date'].dt.month >= 6) & (selected_data['Date'].dt.month <= 8)]
    winter_data = selected_data[(selected_data['Date'].dt.month >= 12) | (selected_data['Date'].dt.month <= 2)]

    summer_avg_prices = summer_data.groupby('Commodity')['Average'].mean().reset_index()
    winter_avg_prices = winter_data.groupby('Commodity')['Average'].mean().reset_index()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    ax1.bar(summer_avg_prices['Commodity'], summer_avg_prices['Average'], color='orange')
    ax1.set_xlabel('Commodity')
    ax1.set_ylabel('Average Price')
    ax1.set_title('Average Prices in Summer')
    ax1.tick_params(axis='x', rotation=45)

    ax2.bar(winter_avg_prices['Commodity'], winter_avg_prices['Average'], color='skyblue')
    ax2.set_xlabel('Commodity')
    ax2.set_ylabel('Average Price')
    ax2.set_title('Average Prices in Winter')
    ax2.tick_params(axis='x', rotation=45)

    st.pyplot(fig)

    st.title('Price Trends by Season')

    seasons = {
        'Summer': [6, 7, 8],
        'Monsoon': [6, 7, 8],
        'Winter': [12, 1, 2],
    }

    for season, months in seasons.items():
        season_data = selected_data[selected_data['Date'].dt.month.isin(months)]
        avg_prices_season = season_data.groupby('Commodity')['Average'].mean().reset_index()

        st.subheader(f'Average Prices in {season}')
        fig = px.bar(avg_prices_season, x='Commodity', y='Average', title=f'Average Prices in {season}',
                    labels={'Commodity': 'Commodity', 'Average': 'Average Price'})
        fig.update_xaxes(title='Commodity')
        fig.update_yaxes(title='Average Price')
        st.plotly_chart(fig)

    st.title('Outlier Analysis in Commodity Prices')

    subset = data[data['Commodity'] == commodity]['Average']
    st.subheader(f'Box Plot of Prices for {commodity}')
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.boxplot(x='Commodity', y='Average', data=data[data['Commodity'].isin(selected_commodities)])
    ax.set_xlabel('Average Price')
    ax.set_title(f'Box Plot of Prices for {commodity}')
    st.pyplot(fig)

# Question 1
elif pages == 'Question 1':
    st.title('Seasonal Analysis of Commodity Prices')
    st.write("""
    ### Question: 
    Can we identify and classify seasonal patterns in commodity prices based solely on historical data?

    ### Practical Motivation:
    Understanding seasonal patterns in commodity prices is crucial for various stakeholders in agriculture, retail, and policy making. It helps in planning production cycles, optimizing inventory management, and anticipating price fluctuations. By analyzing historical data, we can categorize commodities into seasonal groups (e.g., seasonal, non-seasonal) and identify which commodities exhibit predictable seasonal price variations.
    """)

    st.subheader('Average Price Trends of Selected Commodities Over Time')

    
    fig = px.line(title='Average Price Trends of Selected Commodities Over Time')
    for commodity in selected_commodities:
        # Filter data for the current commodity
        subset = data[data['Commodity'] == commodity]
        
        # Create an empty figure
        fig = px.line(subset, x='Date', y='Average', title=f'Average Price Trend of {commodity} Over Time')
        
        # Customize layout
        fig.update_layout(
            xaxis_title='Date',
            yaxis_title='Average Price',
            legend_title='Commodity',
        )
        
        # Show the plot
        st.plotly_chart(fig)

    st.title('Seasonal Decomposition of Commodity Prices')

    for vegetable in selected_commodities:
        st.subheader(f'Seasonal Decomposition of {vegetable}')
        commodity_data = data[data['Commodity'] == vegetable]
        commodity_data.set_index('Date', inplace=True)
        decomposition = seasonal_decompose(commodity_data['Average'], model='multiplicative', period=365)

        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(15, 10))
        decomposition.observed.plot(ax=ax1)
        ax1.set_ylabel('Observed')
        decomposition.trend.plot(ax=ax2)
        ax2.set_ylabel('Trend')
        decomposition.seasonal.plot(ax=ax3)
        ax3.set_ylabel('Seasonal')
        decomposition.resid.plot(ax=ax4)
        ax4.set_ylabel('Residual')
        plt.suptitle(f'Seasonal Decomposition of {vegetable}')
        st.pyplot(fig)

# Question 3
elif pages == 'Question 3':
    st.title('Price Analysis During Holidays and Non-Holidays')

    st.write("""
    ### Question: 
    How do holidays, specifically Dashain and Tihar (October 3rd to November 7th), affect the prices of commodities in the Kalimati market? Are there noticeable price fluctuations during these festive periods compared to non-holiday periods?

    ### Practical Motivation:
    Understanding the impact of cultural holidays like Dashain and Tihar on commodity prices is crucial for both consumers and retailers in the Kalimati market. This analysis helps in predicting and managing price variations, allowing stakeholders to adjust their strategies such as stocking inventory or setting prices in response to expected changes in demand and supply during these festive seasons. By visualizing price fluctuations during holidays versus non-holidays, this study aims to provide insights that can inform better decision-making and operational planning for market participants.    
    """)

    data['IsHoliday'] = data['Date'].apply(is_holiday)

    for commodity in selected_commodities:
        filtered_data = data[data['Commodity'] == commodity]
        
        st.subheader(f'Price Volatility Over Time for {commodity}')
        fig, ax = plt.subplots(figsize=(15, 8))
        
        holiday_commodity_data = filtered_data[filtered_data['IsHoliday']]
        non_holiday_commodity_data = filtered_data[~filtered_data['IsHoliday']]
        
        ax.scatter(holiday_commodity_data['Date'], holiday_commodity_data['Average'], label=f'{commodity} (Holiday)', marker='o', color='red')
        ax.plot(non_holiday_commodity_data['Date'], non_holiday_commodity_data['Average'], linestyle='--', label=f'{commodity} (Non-Holiday)', color='blue')
        
        ax.set_xlabel('Date')
        ax.set_ylabel('Average Price (NPR)')
        ax.set_title(f'Price Fluctuations During Holidays and Non-Holidays for {commodity}')
        ax.legend()
        ax.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        st.pyplot(fig)

# Question 2
elif pages == 'Question 2':
    st.title('Price dynamics between commodities of different origins or varieties')

    st.write("""
    ### Question: 
    How do price dynamics differ between commodities with similar usage but different origins or varieties?

    ### Practical Motivation:
    Understanding regional price variations can provide insights into local supply and demand dynamics, transportation costs, and market inefficiencies. This information can be valuable for logistics planning, pricing strategies, and identifying potential arbitrage opportunities for traders and businesses operating in multiple locations.
    """)

    indian_nepali_data = data[data['Commodity'].str.contains('Onion|Potato|Tomato|Litchi|Orange')]
    avg_prices = indian_nepali_data.groupby('Commodity')['Average'].mean().reset_index()

    st.subheader('Average Price of Different Origin Products')
    fig = px.bar(avg_prices, x='Commodity', y='Average', title='Average Price of Different Origin Products', labels={'Commodity': 'Commodity', 'Average': 'Average Price'})
    fig.update_xaxes(title='Commodity')
    fig.update_yaxes(title='Average Price')
    st.plotly_chart(fig)