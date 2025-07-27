import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_business_data():
    """Generate realistic business data for dashboard demonstration"""
    
    np.random.seed(42)
    
    # Generate dates for 2 years
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 12, 31)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Sales Data with seasonal patterns
    base_sales = 10000
    seasonal_factor = np.sin(np.arange(len(dates)) * 2 * np.pi / 365) * 3000
    trend_factor = np.linspace(0, 2000, len(dates))  # Growing trend
    noise = np.random.normal(0, 1500, len(dates))
    
    sales_data = []
    for i, date in enumerate(dates):
        daily_sales = base_sales + seasonal_factor[i] + trend_factor[i] + noise[i]
        daily_sales = max(daily_sales, 1000)  # Minimum sales threshold
        
        # Add multiple records per day for different regions/products
        for _ in range(np.random.randint(5, 15)):
            sales_data.append({
                'Date': date,
                'Sales': daily_sales / np.random.randint(5, 15),
                'Region': np.random.choice(['North', 'South', 'East', 'West'], p=[0.3, 0.25, 0.25, 0.2]),
                'Product_Category': np.random.choice(['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books'], 
                                                   p=[0.3, 0.25, 0.2, 0.15, 0.1]),
                'Customer_Segment': np.random.choice(['Premium', 'Standard', 'Budget'], p=[0.25, 0.5, 0.25]),
                'Sales_Rep': f"Rep_{np.random.randint(1, 21):02d}",
                'Channel': np.random.choice(['Online', 'Retail', 'Partner'], p=[0.5, 0.35, 0.15])
            })
    
    sales_df = pd.DataFrame(sales_data)
    
    # Customer Data
    num_customers = 2500
    customer_data = []
    
    for i in range(1, num_customers + 1):
        age = max(18, int(np.random.normal(40, 15)))
        region = np.random.choice(['North', 'South', 'East', 'West'])
        segment = np.random.choice(['Premium', 'Standard', 'Budget'], p=[0.25, 0.5, 0.25])
        
        # Correlation between segment and purchases/satisfaction
        if segment == 'Premium':
            total_purchases = np.random.exponential(8) + 5
            base_satisfaction = 7.5
        elif segment == 'Standard':
            total_purchases = np.random.exponential(4) + 2
            base_satisfaction = 6.5
        else:  # Budget
            total_purchases = np.random.exponential(2) + 1
            base_satisfaction = 5.5
        
        satisfaction = min(10, max(1, np.random.normal(base_satisfaction, 1.5)))
        
        customer_data.append({
            'Customer_ID': f"CUST_{i:05d}",
            'Age': age,
            'Gender': np.random.choice(['Male', 'Female']),
            'Region': region,
            'Customer_Segment': segment,
            'Total_Purchases': round(total_purchases, 2),
            'Satisfaction_Score': round(satisfaction, 1),
            'Join_Date': start_date + timedelta(days=np.random.randint(0, 730)),
            'Last_Purchase': start_date + timedelta(days=np.random.randint(0, 730))
        })
    
    customer_df = pd.DataFrame(customer_data)
    
    # Product Data
    products = [
        'Smartphone Pro', 'Laptop Ultra', 'Wireless Headphones', 'Smart Watch',
        'Gaming Console', 'Tablet Plus', 'Camera DSLR', 'Bluetooth Speaker',
        'Designer Jacket', 'Running Shoes', 'Casual Shirt', 'Jeans Premium',
        'Garden Tools Set', 'Kitchen Mixer', 'Outdoor Furniture', 'LED TV',
        'Fitness Tracker', 'Desk Organizer', 'Travel Backpack', 'Coffee Maker'
    ]
    
    product_data = []
    for product in products:
        category = 'Electronics' if any(x in product.lower() for x in ['smartphone', 'laptop', 'headphones', 'watch', 'console', 'tablet', 'camera', 'speaker', 'tv', 'tracker']) else \
                  'Clothing' if any(x in product.lower() for x in ['jacket', 'shoes', 'shirt', 'jeans']) else \
                  'Home & Garden' if any(x in product.lower() for x in ['garden', 'kitchen', 'furniture', 'desk', 'coffee']) else \
                  'Sports' if any(x in product.lower() for x in ['fitness', 'running']) else 'Other'
        
        base_price = np.random.uniform(50, 500) if category == 'Electronics' else \
                    np.random.uniform(30, 200) if category == 'Clothing' else \
                    np.random.uniform(40, 300)
        
        units_sold = np.random.randint(100, 2000)
        revenue = base_price * units_sold
        profit_margin = np.random.uniform(0.15, 0.45)
        customer_rating = np.random.uniform(3.5, 5.0)
        
        product_data.append({
            'Product': product,
            'Category': category,
            'Revenue': round(revenue, 2),
            'Units_Sold': units_sold,
            'Avg_Price': round(base_price, 2),
            'Profit_Margin': round(profit_margin, 3),
            'Customer_Rating': round(customer_rating, 1),
            'Launch_Date': start_date + timedelta(days=np.random.randint(0, 365))
        })
    
    product_df = pd.DataFrame(product_data)
    
    # Save data to CSV files
    sales_df.to_csv('sales_data.csv', index=False)
    customer_df.to_csv('customer_data.csv', index=False)
    product_df.to_csv('product_data.csv', index=False)
    
    print("Data generation complete!")
    print(f"Generated {len(sales_df)} sales records")
    print(f"Generated {len(customer_df)} customer records")
    print(f"Generated {len(product_df)} product records")
    print(f"Total Revenue: ${sales_df['Sales'].sum():,.2f}")

if __name__ == "__main__":
    generate_business_data()
