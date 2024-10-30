import streamlit as st
import requests
import matplotlib.pyplot as plt
from datetime import datetime

# Set up the Streamlit app
st.set_page_config(page_title="Smart Price Tracker", layout="centered")
st.title("Smart Price Tracker 📉")

# Search input
st.write("Enter a product URL or keyword to track its price:")
search_term = st.text_input("Product URL or keyword")

# Mock data function to simulate an API call (Replace with a real API in production)
def fetch_product_data(search_term):
    # Mock response simulating product details and price history
    return {
        "title": f"Sample Product for '{search_term}'",
        "currentPrice": 25900,
        "prices": [
            {"date": "2023-01-01", "price": 30000},
            {"date": "2023-02-01", "price": 28000},
            {"date": "2023-03-01", "price": 27000},
            {"date": "2023-04-01", "price": 25900},
        ]
    }

# Fetch data when search term is provided
if search_term:
    with st.spinner("Fetching product data..."):
        product_data = fetch_product_data(search_term)  # Using mock data

    if product_data:
        st.header(product_data["title"])

        # Display price statistics
        prices = [price['price'] for price in product_data['prices']]
        current_price = product_data['currentPrice']
        min_price = min(prices)
        max_price = max(prices)

        st.write("### Price Statistics")
        st.metric(label="Current Price", value=f"{current_price:,}원")
        st.metric(label="Lowest Price", value=f"{min_price:,}원")
        st.metric(label="Highest Price", value=f"{max_price:,}원")

        # Lowest price check
        if current_price == min_price:
            st.success("⚡️ Now is the best time to buy at the lowest price! ⚡️")

        # Price history chart
        st.write("### Price History")
        dates = [datetime.strptime(price['date'], "%Y-%m-%d") for price in product_data['prices']]
        
        plt.figure(figsize=(10, 5))
        plt.plot(dates, prices, marker='o', color='b', label='Price')
        plt.fill_between(dates, min(prices), max(prices), color='b', alpha=0.1)
        plt.xlabel("Date")
        plt.ylabel("Price (₩)")
        plt.title("Price Trend Over Time")
        plt.legend()
        st.pyplot(plt)

        # Price alert input
        st.write("### Set Price Alert")
        target_price = st.number_input("Enter your target price (₩)", min_value=0)
        
        # Price alert logic
        if target_price:
            if current_price <= target_price:
                st.success("🎉 The current price is already below your target!")
            else:
                st.info("Alert set! You'll be notified when the price drops.")
    else:
        st.warning("No product data found. Try a different keyword or URL.")
