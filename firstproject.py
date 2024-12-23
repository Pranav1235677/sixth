import streamlit as st
import pandas as pd
import sqlite3
import random
import datetime

# Database connection
conn = sqlite3.connect("expense_tracker.db")
cursor = conn.cursor()

# Create tables for each month
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
for month in months:
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {month} (
            Date TEXT,
            Category TEXT,
            Payment_Mode TEXT,
            Description TEXT,
            Amount_Paid REAL,
            Cashback REAL
        )
    """)
conn.commit()

# Generate random descriptions
descriptions = {
    "Investments": ["Invested in mutual funds", "Bought stocks", "Investment in gold"],
    "Bills": ["Paid electricity bill", "Paid water bill", "Paid internet bill"],
    "Groceries": ["Bought vegetables", "Bought fruits", "Supermarket shopping"],
    "Dining": ["Dinner at a restaurant", "Ordered online food", "Coffee shop visit"],
    "School FEES": ["School admission fees", "Monthly tuition fees"],
    "Sports & Fitness": ["Gym membership", "Bought sports equipment", "Yoga class fee"],
    "Fruits & Vegetables": ["Weekly vegetable shopping", "Bought organic fruits"],
    "Stationery": ["Bought notebooks", "Bought pens and pencils", "School supplies shopping"],
    "Subscriptions": ["Netflix subscription", "Spotify premium", "Amazon Prime renewal"],
    "Home Essentials": ["Bought cleaning supplies", "Kitchen essentials shopping"],
}

# Generate random expense data for a month
def generate_expense_data(month):
    data = []
    for _ in range(30):  # Generating 30 random entries
        date = datetime.date(2024, months.index(month) + 1, random.randint(1, 28))
        category = random.choice(list(descriptions.keys()))
        description = random.choice(descriptions[category])
        payment_mode = random.choice(["Cash", "Credit Card", "Debit Card", "UPI", "Net Banking", "Wallet"])
        amount_paid = round(random.uniform(50, 500), 2)
        cashback = round(amount_paid * random.uniform(0.01, 0.05), 2)
        data.append((date, category, payment_mode, description, amount_paid, cashback))
    return data

# Insert generated data into the database
def insert_data(month, data):
    cursor.executemany(f"INSERT INTO {month} VALUES (?, ?, ?, ?, ?, ?)", data)
    conn.commit()

# Query data
def query_data(query):
    return pd.read_sql_query(query, conn)

# Streamlit app
def main():
    st.title("Personal Expense Tracker")

    # Section to generate expense data
    st.header("Generate Expense Data")
    selected_month = st.selectbox("Select a month to generate data for:", months)
    if st.button("Generate Data"):
        data = generate_expense_data(selected_month)
        insert_data(selected_month, data)
        st.success(f"Data for {selected_month} generated and loaded into the database!")

    # Section to view data
    st.header("View Data")
    view_month = st.selectbox("Select a month to view data:", months, key="view_month")
    if st.button("View Data"):
        query = f"SELECT * FROM {view_month}"
        data = query_data(query)
        st.write(data)

    # Predefined SQL Queries
    st.header("Predefined SQL Queries")
    predefined_queries = {
        "Total Expense by Month": "SELECT SUM(Amount_Paid) AS Total_Expense FROM {month}",
        "Average Cashback by Category": "SELECT Category, AVG(Cashback) AS Avg_Cashback FROM {month} GROUP BY Category",
        "Highest Spending Category": "SELECT Category, SUM(Amount_Paid) AS Total_Spending FROM {month} GROUP BY Category ORDER BY Total_Spending DESC LIMIT 1",
        "Payment Mode Distribution": "SELECT Payment_Mode, COUNT(*) AS Count FROM {month} GROUP BY Payment_Mode"
    }
    query_name = st.selectbox("Select a query to run:", list(predefined_queries.keys()))
    query_month = st.selectbox("Select a month for the query:", months, key="query_month")
    
    if st.button("Run Query"):
        query = predefined_queries[query_name].format(month=query_month)
        result = query_data(query)
        st.write(result)

# Entry point
if "__name__" == "__main__":
    main()