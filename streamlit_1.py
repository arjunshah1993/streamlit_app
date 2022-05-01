# library imports
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# page title
st.title("Walmart Stock Price (2012 - 2016)")


# function to get data
def get_data():
    
    url = 'https://raw.githubusercontent.com/arjunshah1993/streamlit_app/main/walmart_stock.csv'
    df = pd.read_csv(url, header=0, parse_dates=['Date'])
    return df

# data_load_state = st.text('Loading data...') # display loading text message
df = get_data() # function call to load data

# add 50-day and 200-day moving averages
df['MA (50)'] = df['Adj Close'].rolling(50).mean()
df['MA (200)'] = df['Adj Close'].rolling(200).mean()

# subheader for line chart
st.subheader("Daily Adjusted Close Price ($) with 50-day and 200-day moving averages")

# line chart of daily stock price with moving averages
fig = px.line(data_frame=df,
              x='Date',
              y=['Adj Close', 'MA (50)', 'MA (200)'],
               width=1000,
               height=550
              )
fig.update_layout(xaxis_title="Timeline", yaxis_title="Stock Price ($)")
st.plotly_chart(fig, use_container_width=False)

# create a dataframe aggregated by month for monthly candlestick chart
df['Month'] = df['Date'].dt.to_period('M').dt.to_timestamp() # truncate date to month
monthly_df = df[['Month','Open','High','Low','Close']].groupby('Month').agg({'Open':'first',
                                                                             'High':'max',
                                                                             'Low':'min',
                                                                             'Close':'last'}).reset_index()

# monthly candlestick chart
st.subheader("Monthly Candlestick Chart")
candles = go.Candlestick(x=monthly_df['Month'],
                         open=monthly_df['Open'],
                         high=monthly_df['High'],
                         low=monthly_df['Low'],
                         close=monthly_df['Close']
                         )
fig = go.Figure(data=[candles])
fig.update_layout(xaxis_rangeslider_visible=False,
                   width=1000,
                   height=550,
                  xaxis_title="Timeline",
                  yaxis_title="Stock Price ($)")
st.plotly_chart(fig, use_container_width=False)