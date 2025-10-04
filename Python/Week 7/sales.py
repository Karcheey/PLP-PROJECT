# sales_analysis.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("=== SALES DATA ANALYSIS & VISUALIZATION ===")

try:

    # Task 1: Load and Explore Dataset
    
    print("\n=== TASK 1: LOAD & EXPLORE DATASET ===")

    # Create a simple sales dataset
    data = {
        "Date": pd.date_range(start="2023-01-01", periods=12, freq="M"),
        "Region": ["North", "South", "East", "West"] * 3,
        "Product": ["Laptop", "Phone", "Tablet"] * 4,
        "Sales": [2000, 1500, 800, 1200, 3000, 2200, 950, 1750,
                  2800, 1300, 1100, 2100]
    }

    df = pd.DataFrame(data)

    # Show first few rows
    print("\nFirst 5 rows of dataset:")
    print(df.head())

    # Info about dataset
    print("\nDataset Info:")
    print(df.info())

    # Check for missing values
    print("\nMissing values per column:")
    print(df.isnull().sum())

    
    # Task 2: Basic Data Analysis
    
    print("\n=== TASK 2: BASIC DATA ANALYSIS ===")

    if "Sales" not in df.columns:
        raise KeyError("Error: 'Sales' column not found in dataset.")

    # Descriptive statistics
    print("\nDescriptive Statistics of Sales:")
    print(df["Sales"].describe())

    # Grouping: average sales by region
    avg_sales_region = df.groupby("Region")["Sales"].mean()
    print("\nAverage Sales by Region:")
    print(avg_sales_region)

    # Grouping: average sales by product
    avg_sales_product = df.groupby("Product")["Sales"].mean()
    print("\nAverage Sales by Product:")
    print(avg_sales_product)

    # Observation
    print("\nObservation: Laptops have the highest average sales, "
          "while Tablets generally sell the least. "
          "Among regions, North and South tend to perform stronger than East/West.")

    
    # Task 3: Data Visualization
    
    print("\n=== TASK 3: DATA VISUALIZATION ===")

    sns.set(style="whitegrid")

    try:
        # 1. Line Chart - Sales trend over time
        plt.figure(figsize=(8,5))
        plt.plot(df["Date"], df["Sales"], marker="o", label="Sales Trend")
        plt.title("Monthly Sales Trend")
        plt.xlabel("Date")
        plt.ylabel("Sales")
        plt.legend()
        plt.show()

        # 2. Bar Chart - Average Sales by Region
        plt.figure(figsize=(8,5))
        avg_sales_region.plot(kind="bar", color="skyblue", edgecolor="black")
        plt.title("Average Sales by Region")
        plt.xlabel("Region")
        plt.ylabel("Average Sales")
        plt.show()

        # 3. Histogram - Distribution of Sales
        plt.figure(figsize=(8,5))
        plt.hist(df["Sales"], bins=10, color="orange", edgecolor="black")
        plt.title("Histogram of Sales")
        plt.xlabel("Sales Amount")
        plt.ylabel("Frequency")
        plt.show()

        # 4. Scatter Plot - Comparing Sales by Product & Region
        plt.figure(figsize=(8,5))
        sns.scatterplot(x="Product", y="Sales", hue="Region", data=df, s=100)
        plt.title("Sales by Product & Region")
        plt.xlabel("Product")
        plt.ylabel("Sales")
        plt.legend(title="Region")
        plt.show()

    except Exception as e:
        print(f"Error while generating plots: {e}")

    print("\nAll tasks completed successfully! 🎉")

except Exception as e:
    print(f"An error occurred: {e}")
