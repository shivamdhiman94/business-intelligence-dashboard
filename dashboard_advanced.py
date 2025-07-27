import dash
from dash import dcc, html, Input, Output, dash_table, callback
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime, timedelta

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Business Intelligence Dashboard"

# Custom CSS styling
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                background-color: #f5f7fa;
            }
            .metric-card {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                text-align: center;
                margin: 10px;
            }
            .metric-value {
                font-size: 2.5em;
                font-weight: bold;
                margin: 0;
            }
            .metric-label {
                font-size: 1.1em;
                opacity: 0.9;
                margin: 5px 0 0 0;
            }
            .filter-container {
                background: white;
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                margin: 20px 0;
            }
            .insights-container {
                background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
                padding: 25px;
                border-radius: 15px;
                margin: 30px 0;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Load or generate data
def load_data():
    try:
        # Try to load existing data
        sales_data = pd.read_csv('sales_data.csv')
        customer_data = pd.read_csv('customer_data.csv')
        product_data = pd.read_csv('product_data.csv')
        
        # Convert date columns
        sales_data['Date'] = pd.to_datetime(sales_data['Date'])
        customer_data['Join_Date'] = pd.to_datetime(customer_data['Join_Date'])
        customer_data['Last_Purchase'] = pd.to_datetime(customer_data['Last_Purchase'])
        product_data['Launch_Date'] = pd.to_datetime(product_data['Launch_Date'])
        
        print("Loaded existing data files")
        
    except FileNotFoundError:
        # Generate sample data if files don't exist
        print("Generating sample data...")
        
        np.random.seed(42)
        dates = pd.date_range(start='2023-01-01', end='2024-12-31', freq='D')
        
        # Generate more realistic sales data
        sales_records = []
        for date in dates:
            daily_transactions = np.random.randint(20, 100)
            for _ in range(daily_transactions):
                sales_records.append({
                    'Date': date,
                    'Sales': np.random.lognormal(8, 0.8),
                    'Region': np.random.choice(['North', 'South', 'East', 'West'], p=[0.3, 0.25, 0.25, 0.2]),
                    'Product_Category': np.random.choice(['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books']),
                    'Customer_Segment': np.random.choice(['Premium', 'Standard', 'Budget'], p=[0.25, 0.5, 0.25]),
                    'Channel': np.random.choice(['Online', 'Retail', 'Partner'], p=[0.6, 0.3, 0.1])
                })
        
        sales_data = pd.DataFrame(sales_records)
        
        # Customer data
        num_customers = 2000
        customer_data = pd.DataFrame({
            'Customer_ID': [f"CUST_{i:05d}" for i in range(1, num_customers + 1)],
            'Age': np.random.normal(40, 15, num_customers).clip(18, 80).astype(int),
            'Gender': np.random.choice(['Male', 'Female'], num_customers),
            'Total_Purchases': np.random.exponential(5, num_customers),
            'Satisfaction_Score': np.random.normal(7, 1.5, num_customers).clip(1, 10),
            'Region': np.random.choice(['North', 'South', 'East', 'West'], num_customers),
            'Customer_Segment': np.random.choice(['Premium', 'Standard', 'Budget'], num_customers, p=[0.25, 0.5, 0.25])
        })
        
        # Product data
        product_names = ['Smartphone Pro', 'Laptop Ultra', 'Wireless Headphones', 'Smart Watch', 'Gaming Console',
                        'Designer Jacket', 'Running Shoes', 'Casual Shirt', 'Premium Jeans', 'Winter Coat',
                        'Garden Tool Set', 'Kitchen Mixer', 'Coffee Maker', 'LED TV', 'Bluetooth Speaker']
        
        product_data = pd.DataFrame({
            'Product': product_names,
            'Category': ['Electronics'] * 5 + ['Clothing'] * 5 + ['Home & Garden'] * 5,
            'Revenue': np.random.uniform(50000, 300000, len(product_names)),
            'Units_Sold': np.random.randint(100, 2000, len(product_names)),
            'Profit_Margin': np.random.uniform(0.1, 0.5, len(product_names)),
            'Customer_Rating': np.random.uniform(3.5, 5.0, len(product_names))
        })
    
    return sales_data, customer_data, product_data

# Load the data
sales_data, customer_data, product_data = load_data()

# Calculate key metrics
total_revenue = sales_data['Sales'].sum()
total_customers = len(customer_data)
avg_satisfaction = customer_data['Satisfaction_Score'].mean()
avg_profit_margin = product_data['Profit_Margin'].mean()

# Define the layout
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("Business Intelligence Dashboard", 
                style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '10px', 'fontSize': '3em'}),
        html.P("Real-time Analytics & Insights", 
               style={'textAlign': 'center', 'color': '#7f8c8d', 'fontSize': '1.2em', 'marginBottom': '30px'})
    ]),
    
    # Key Metrics Row
    html.Div([
        html.Div([
            html.H2(f"${total_revenue:,.0f}", className='metric-value'),
            html.P("Total Revenue", className='metric-label')
        ], className='metric-card', style={'width': '22%', 'display': 'inline-block'}),
        
        html.Div([
            html.H2(f"{total_customers:,}", className='metric-value'),
            html.P("Active Customers", className='metric-label')
        ], className='metric-card', style={'width': '22%', 'display': 'inline-block'}),
        
        html.Div([
            html.H2(f"{avg_satisfaction:.1f}/10", className='metric-value'),
            html.P("Customer Satisfaction", className='metric-label')
        ], className='metric-card', style={'width': '22%', 'display': 'inline-block'}),
        
        html.Div([
            html.H2(f"{avg_profit_margin:.1%}", className='metric-value'),
            html.P("Average Margin", className='metric-label')
        ], className='metric-card', style={'width': '22%', 'display': 'inline-block'})
    ], style={'textAlign': 'center', 'marginBottom': '30px'}),
    
    # Filters
    html.Div([
        html.Div([
            html.Label("Region:", style={'fontWeight': 'bold', 'marginBottom': '5px', 'display': 'block'}),
            dcc.Dropdown(
                id='region-filter',
                options=[{'label': 'All Regions', 'value': 'all'}] + 
                        [{'label': region, 'value': region} for region in sales_data['Region'].unique()],
                value='all',
                style={'width': '100%'}
            )
        ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '5%'}),
        
        html.Div([
            html.Label("Product Category:", style={'fontWeight': 'bold', 'marginBottom': '5px', 'display': 'block'}),
            dcc.Dropdown(
                id='category-filter',
                options=[{'label': 'All Categories', 'value': 'all'}] + 
                        [{'label': cat, 'value': cat} for cat in sales_data['Product_Category'].unique()],
                value='all',
                style={'width': '100%'}
            )
        ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '5%'}),
        
        html.Div([
            html.Label("Date Range:", style={'fontWeight': 'bold', 'marginBottom': '5px', 'display': 'block'}),
            dcc.DatePickerRange(
                id='date-range',
                start_date=sales_data['Date'].min(),
                end_date=sales_data['Date'].max(),
                display_format='YYYY-MM-DD',
                style={'width': '100%'}
            )
        ], style={'width': '30%', 'display': 'inline-block'})
    ], className='filter-container'),
    
    # Charts Row 1
    html.Div([
        html.Div([
            dcc.Graph(id='sales-trend-chart')
        ], style={'width': '50%', 'display': 'inline-block', 'padding': '10px'}),
        
        html.Div([
            dcc.Graph(id='regional-performance-chart')
        ], style={'width': '50%', 'display': 'inline-block', 'padding': '10px'})
    ]),
    
    # Charts Row 2
    html.Div([
        html.Div([
            dcc.Graph(id='category-analysis-chart')
        ], style={'width': '50%', 'display': 'inline-block', 'padding': '10px'}),
        
        html.Div([
            dcc.Graph(id='customer-segment-chart')
        ], style={'width': '50%', 'display': 'inline-block', 'padding': '10px'})
    ]),
    
    # Advanced Analytics Row
    html.Div([
        html.Div([
            dcc.Graph(id='product-performance-bubble')
        ], style={'width': '60%', 'display': 'inline-block', 'padding': '10px'}),
        
        html.Div([
            dcc.Graph(id='satisfaction-by-segment')
        ], style={'width': '40%', 'display': 'inline-block', 'padding': '10px'})
    ]),
    
    # Data Tables
    html.Div([
        html.Div([
            html.H3("Top Performing Products", style={'textAlign': 'center', 'color': '#2c3e50'}),
            dash_table.DataTable(
                id='top-products-table',
                columns=[
                    {'name': 'Product', 'id': 'Product'},
                    {'name': 'Revenue', 'id': 'Revenue', 'type': 'numeric', 'format': {'specifier': '$,.0f'}},
                    {'name': 'Units Sold', 'id': 'Units_Sold', 'type': 'numeric'},
                    {'name': 'Profit Margin', 'id': 'Profit_Margin', 'type': 'numeric', 'format': {'specifier': '.1%'}},
                    {'name': 'Rating', 'id': 'Customer_Rating', 'type': 'numeric', 'format': {'specifier': '.1f'}}
                ],
                data=product_data.nlargest(10, 'Revenue').to_dict('records'),
                style_cell={'textAlign': 'center', 'padding': '10px'},
                style_header={
                    'backgroundColor': '#3498db',
                    'color': 'white',
                    'fontWeight': 'bold',
                    'border': '1px solid white'
                },
                style_data={
                    'backgroundColor': '#ecf0f1',
                    'border': '1px solid white'
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 0},
                        'backgroundColor': '#2ecc71',
                        'color': 'white',
                    }
                ]
            )
        ], style={'width': '50%', 'display': 'inline-block', 'padding': '20px'}),
        
        html.Div([
            html.H3("Regional Leaders", style={'textAlign': 'center', 'color': '#2c3e50'}),
            dash_table.DataTable(
                id='regional-table',
                columns=[
                    {'name': 'Region', 'id': 'Region'},
                    {'name': 'Total Sales', 'id': 'Total_Sales', 'type': 'numeric', 'format': {'specifier': '$,.0f'}},
                    {'name': 'Avg Transaction', 'id': 'Avg_Transaction', 'type': 'numeric', 'format': {'specifier': '$,.0f'}},
                    {'name': 'Customers', 'id': 'Customer_Count', 'type': 'numeric'}
                ],
                style_cell={'textAlign': 'center', 'padding': '10px'},
                style_header={
                    'backgroundColor': '#e74c3c',
                    'color': 'white',
                    'fontWeight': 'bold',
                    'border': '1px solid white'
                },
                style_data={
                    'backgroundColor': '#ecf0f1',
                    'border': '1px solid white'
                }
            )
        ], style={'width': '50%', 'display': 'inline-block', 'padding': '20px'})
    ], style={'backgroundColor': 'white', 'margin': '20px 0', 'borderRadius': '15px', 'boxShadow': '0 2px 10px rgba(0,0,0,0.1)'}),
    
    # Insights Section
    html.Div([
        html.H3("📊 Key Business Insights & Recommendations", 
                style={'color': '#2c3e50', 'marginBottom': '20px', 'fontSize': '1.8em'}),
        
        html.Div([
            html.Div([
                html.H4("💰 Revenue Optimization", style={'color': '#27ae60', 'marginBottom': '10px'}),
                html.Ul([
                    html.Li("Focus marketing spend on top-performing product categories"),
                    html.Li("Implement dynamic pricing for high-margin products"),
                    html.Li("Expand inventory in peak sales periods identified in trends")
                ])
            ], style={'width': '50%', 'display': 'inline-block', 'verticalAlign': 'top', 'paddingRight': '20px'}),
            
            html.Div([
                html.H4("🎯 Customer Experience", style={'color': '#3498db', 'marginBottom': '10px'}),
                html.Ul([
                    html.Li("Implement targeted retention programs for high-value segments"),
                    html.Li("Address satisfaction gaps in underperforming regions"),
                    html.Li("Develop personalized product recommendations")
                ])
            ], style={'width': '50%', 'display': 'inline-block', 'verticalAlign': 'top'})
        ]),
        
        html.Div([
            html.Div([
                html.H4("📈 Growth Opportunities", style={'color': '#e67e22', 'marginBottom': '10px'}),
                html.Ul([
                    html.Li("Expand successful product lines to underperforming regions"),
                    html.Li("Investigate seasonal patterns for inventory planning"),
                    html.Li("Develop cross-selling strategies for premium customers")
                ])
            ], style={'width': '50%', 'display': 'inline-block', 'verticalAlign': 'top', 'paddingRight': '20px'}),
            
            html.Div([
                html.H4("⚡ Operational Efficiency", style={'color': '#9b59b6', 'marginBottom': '10px'}),
                html.Ul([
                    html.Li("Optimize supply chain for top-selling products"),
                    html.Li("Implement predictive analytics for demand forecasting"),
                    html.Li("Automate reporting for real-time decision making")
                ])
            ], style={'width': '50%', 'display': 'inline-block', 'verticalAlign': 'top'})
        ])
    ], className='insights-container')
    
], style={'margin': '0 20px', 'fontFamily': 'Segoe UI, sans-serif'})

# Callbacks for interactivity
@app.callback(
    [Output('sales-trend-chart', 'figure'),
     Output('regional-performance-chart', 'figure'),
     Output('category-analysis-chart', 'figure'),
     Output('customer-segment-chart', 'figure'),
     Output('product-performance-bubble', 'figure'),
     Output('satisfaction-by-segment', 'figure'),
     Output('regional-table', 'data')],
    [Input('region-filter', 'value'),
     Input('category-filter', 'value'),
     Input('date-range', 'start_date'),
     Input('date-range', 'end_date')]
)
def update_dashboard(selected_region, selected_category, start_date, end_date):
    # Filter data
    filtered_sales = sales_data[
        (sales_data['Date'] >= start_date) & 
        (sales_data['Date'] <= end_date)
    ]
    
    if selected_region != 'all':
        filtered_sales = filtered_sales[filtered_sales['Region'] == selected_region]
    
    if selected_category != 'all':
        filtered_sales = filtered_sales[filtered_sales['Product_Category'] == selected_category]
    
    # 1. Sales Trend Chart
    daily_sales = filtered_sales.groupby('Date')['Sales'].sum().reset_index()
    trend_fig = px.line(daily_sales, x='Date', y='Sales', 
                       title='Sales Trend Over Time',
                       color_discrete_sequence=['#3498db'])
    trend_fig.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    # 2. Regional Performance Chart
    regional_sales = filtered_sales.groupby('Region')['Sales'].sum().reset_index()
    regional_fig = px.bar(regional_sales, x='Region', y='Sales',
                         title='Sales Performance by Region',
                         color='Sales',
                         color_continuous_scale='viridis')
    regional_fig.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    # 3. Category Analysis Chart
    category_sales = filtered_sales.groupby('Product_Category')['Sales'].sum().reset_index()
    category_fig = px.pie(category_sales, values='Sales', names='Product_Category',
                         title='Sales Distribution by Category',
                         color_discrete_sequence=px.colors.qualitative.Set3)
    category_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    # 4. Customer Segment Chart
    segment_sales = filtered_sales.groupby('Customer_Segment')['Sales'].sum().reset_index()
    segment_fig = px.bar(segment_sales, x='Customer_Segment', y='Sales',
                        title='Revenue by Customer Segment',
                        color='Customer_Segment',
                        color_discrete_sequence=['#e74c3c', '#f39c12', '#2ecc71'])
    segment_fig.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    # 5. Product Performance Bubble Chart
    bubble_fig = go.Figure()
    bubble_fig.add_trace(go.Scatter(
        x=product_data['Units_Sold'],
        y=product_data['Revenue'],
        mode='markers',
        marker=dict(
            size=product_data['Customer_Rating'] * 8,
            color=product_data['Profit_Margin'],
            colorscale='viridis',
            showscale=True,
            colorbar=dict(title="Profit Margin", x=1.02)
        ),
        text=product_data['Product'],
        textposition='middle center',
        hovertemplate='<b>%{text}</b><br>Units Sold: %{x}<br>Revenue: $%{y:,.0f}<br>Rating: %{marker.size/8:.1f}<extra></extra>'
    ))
    bubble_fig.update_layout(
        title='Product Performance Matrix<br><sub>Size = Customer Rating, Color = Profit Margin</sub>',
        xaxis_title='Units Sold',
        yaxis_title='Revenue ($)',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    # 6. Satisfaction by Segment
    satisfaction_fig = px.box(customer_data, x='Customer_Segment', y='Satisfaction_Score',
                             title='Customer Satisfaction by Segment',
                             color='Customer_Segment',
                             color_discrete_sequence=['#e74c3c', '#f39c12', '#2ecc71'])
    satisfaction_fig.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    # 7. Regional Table Data
    regional_stats = filtered_sales.groupby('Region').agg({
        'Sales': ['sum', 'mean', 'count']
    }).round(0)
    regional_stats.columns = ['Total_Sales', 'Avg_Transaction', 'Customer_Count']
    regional_stats = regional_stats.reset_index()
    regional_stats = regional_stats.sort_values('Total_Sales', ascending=False)
    
    return (trend_fig, regional_fig, category_fig, segment_fig, 
            bubble_fig, satisfaction_fig, regional_stats.to_dict('records'))

if __name__ == '__main__':
    print("Starting Business Intelligence Dashboard...")
    print("Dashboard will be available at: http://localhost:8050")
    app.run_server(debug=True, port=8050)
