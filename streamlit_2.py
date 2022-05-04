# import libraries
import pandas as pd
import streamlit as st
import plotly.express as px

# page title
st.title("Sales Data Analysis")

# function to get data
@st.cache
def get_data():
    
    df = pd.read_csv('sales.csv', parse_dates=['OrderDate'])
    df['Year'] = df['OrderDate'].dt.strftime('%Y') # year column for aggregations
    df['Month'] = df['OrderDate'].dt.to_period('M').dt.to_timestamp() # month column for aggregations
    return df

# call function to get data
df = get_data()

# function to plot yearly aggregated bar plot
def plot_yearly_bars(year):
    
    grouped_df = df[['ProdCategory','Order Total']][df.Year==year].groupby('ProdCategory').sum().reset_index()
    fig = px.bar(data_frame=grouped_df.sort_values('Order Total',ascending=False),
           x='Order Total',
           y='ProdCategory',
           color='ProdCategory',
           labels={'ProdCategory':'Product Category'},
           )
    fig.update_traces(width=0.5)
    fig.update_layout(xaxis_title="Total Sales ($)",
                      yaxis_title="Product Category",
                      width=1000,
                      height=550
                      )
    return fig

# total sales by Category by Year
st.subheader("Total Sales by Product Category by Year")
year = st.radio(label="Choose Year", options=df.Year.unique())
st.plotly_chart(plot_yearly_bars(year))

# Sales Region time series
st.subheader("Monthly Sales by Sales Region")
grouped_df_2 = df[['Month','Sales Region','Order Total']].groupby(['Month','Sales Region']).sum().reset_index()
regions = st.multiselect("Select Sales Region(s)",
                         options=grouped_df_2['Sales Region'].unique(),
                         default=grouped_df_2['Sales Region'].unique()[:3]
                        )
fig = px.line(data_frame=grouped_df_2[grouped_df_2['Sales Region'].isin(regions)],
              x='Month',
              y='Order Total',
              width=1000,
              height=550,
              color='Sales Region'
              )
fig.update_layout(xaxis_title="Timeline", yaxis_title="Sales ($)")
st.plotly_chart(fig, use_container_width=False)

# Total Individual Sales by State with button for Business sales
st.subheader("Total Sales by State and Customer Type")
grouped_df_3 = df[['CustomerType','CustState','Order Total']].groupby(['CustomerType','CustState']).sum().reset_index()


if st.button("Change Customer Type to Business"):
    
    fig = px.bar(data_frame=grouped_df_3[grouped_df_3['CustomerType']=='Business'].sort_values('Order Total',ascending=False),
                 x='CustState',
                 y='Order Total',
                 width=1000,
                 height=550
                )
    fig.update_layout(title_text="Total Sales by State for Business Customers",
                      xaxis_title="State",
                      yaxis_title="Sales ($)"
                      )
    fig.update_xaxes(tickangle=-90)
    st.plotly_chart(fig, use_container_width=False)
    
else:
    
    fig = px.bar(data_frame=grouped_df_3[grouped_df_3['CustomerType']=='Individual'].sort_values('Order Total',ascending=False),
                 x='CustState',
                 y='Order Total',
                 width=1000,
                 height=550
                )
    fig.update_layout(title_text="Total Sales by State for Individual Customers",
                      xaxis_title="State",
                      yaxis_title="Sales ($)"
                      )
    fig.update_xaxes(tickangle=-90)
    st.plotly_chart(fig, use_container_width=False)