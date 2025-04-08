# main.py

from budget_manager import BudgetManager

def print_menu():
    print("\n=== SmartBudget – Menu ===")
    print("1. Add Income")
    print("2. Add Expense")
    print("3. View All Entries")
    print("4. View Summary")
    print("5. Show Expense Pie Chart")
    print("6. Show Monthly Statistics")
    print("7. Show Yearly Statistics")
    print("8. Exit")

def main():
    manager = BudgetManager()

    while True:
        print_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            amount = float(input("Enter income amount: "))
            category = input("Enter income category (e.g., salary, freelance): ")
            manager.add_entry(amount, category, "income")
            print("Income added!")

        elif choice == "2":
            amount = float(input("Enter expense amount: "))
            category = input("Enter expense category (e.g., food, rent, travel): ")
            manager.add_entry(amount, category, "expense")
            print("Expense added!")

        elif choice == "3":
            entries = manager.list_entries()
            for e in entries:
                print(e)

        elif choice == "4":
            summary = manager.get_summary()
            print("\n=== Summary ===")
            print(f"Total Income: ${summary['total_income']}")
            print(f"Total Expenses: ${summary['total_expense']}")
            print(f"Net Savings: ${summary['net_savings']}")
        

        elif choice == "5":
            from stats_visualizer import show_expense_pie_chart
            show_expense_pie_chart(manager.list_entries())

        elif choice == "6":
            from stats_visualizer import show_monthly_statistics
            show_monthly_statistics(manager.list_entries())

        elif choice == "7":
            from stats_visualizer import show_yearly_statistics
            show_yearly_statistics(manager.list_entries())

        elif choice == "8":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
