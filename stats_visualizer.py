import matplotlib
matplotlib.use('TkAgg')  # Force TkAgg backend to avoid errors
import matplotlib.pyplot as plt
import pandas as pd

import pandas as pd
import matplotlib.pyplot as plt

def show_expense_pie_chart(entries):
    # Convert entries to a DataFrame for easier manipulation
    df = pd.DataFrame(entries)
    df["date"] = pd.to_datetime(df["date"])

    # Grouping by expense type
    expense_data = df[df["type"] == "expense"].groupby("category")["amount"].sum()

    # Aesthetic colors for the pie chart
    colors = [
        '#66b3ff', '#99ff99', '#ffcc99', '#ff6666',  # Soft pastel shades
        '#c2c2f0', '#ffb3e6', '#c2f0c2', '#ffb366'   # More pastel colors
    ]
    
    # Plotting the pie chart
    plt.figure(figsize=(7, 7))
    plt.pie(expense_data, labels=expense_data.index, autopct="%1.1f%%", startangle=140, colors=colors)
    plt.title("Expense Pie Chart", fontsize=16, fontweight='bold')
    plt.axis('equal')  # Equal aspect ratio ensures the pie is drawn as a circle.
    plt.show()


def show_monthly_statistics(entries):
    # Convert entries to a DataFrame for easier manipulation
    df = pd.DataFrame(entries)
    df["date"] = pd.to_datetime(df["date"])
    
    # Extract month and year for aggregation
    df["month"] = df["date"].dt.to_period("M").astype(str)
    df["year"] = df["date"].dt.year

    # Summarize by month
    monthly_data = df.groupby(["month", "type"])["amount"].sum().unstack().fillna(0)

    # Plot Monthly Income vs Expenses
    monthly_data.plot(kind="bar", figsize=(10, 6))
    plt.title("Monthly Income vs Expenses")
    plt.xlabel("Month")
    plt.ylabel("Amount")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def show_yearly_statistics(entries):
    # Convert entries to a DataFrame for easier manipulation
    df = pd.DataFrame(entries)
    df["date"] = pd.to_datetime(df["date"])

    # Extract year for aggregation
    df["year"] = df["date"].dt.year

    # Summarize by year
    yearly_data = df.groupby(["year", "type"])["amount"].sum().unstack().fillna(0)

    # Plot Yearly Income vs Expenses Pie Chart
    yearly_data = yearly_data.sum(axis=0)  # Sum total income and expenses for the year
    labels = yearly_data.index
    values = yearly_data.values

    plt.figure(figsize=(7, 7))
    plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=140, colors=["#66b3ff", "#ff6666"])
    plt.title("Yearly Income vs Expenses")
    plt.show()
