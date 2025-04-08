from datetime import datetime
from data_handler import save_entry, load_entries

CATEGORIES = ["rent", "food", "entertainment", "travel", "other"]  # Added 'other' for uncategorized expenses

class BudgetManager:
    def __init__(self):
        # Load entries from the data file (assuming this loads a list of dictionaries)
        self.entries = load_entries()
        for e in self.entries:
            e["amount"] = float(e["amount"])  # Ensure amounts are floats for accurate calculations

    def add_entry(self, amount, category, entry_type, date=None):
        """ Adds a new income or expense entry """
        if date is None:
            date = datetime.today().strftime('%Y-%m-%d')  # Set date to today if not specified
        category = category.lower()  # Convert category to lowercase for consistency
        
        if entry_type == "expense" and category not in CATEGORIES:
            category = "other"  # Use 'other' for unrecognized categories
        
        entry = {
            "amount": float(amount),  # Ensure amount is a float
            "category": category,
            "type": entry_type,
            "date": date
        }
        self.entries.append(entry)  # Add the entry to the list
        save_entry(entry)  # Save the entry (presumably saves to a file or database)

    def list_entries(self):
        """ Returns a list of all entries """
        return self.entries

    def get_summary(self):
        """ Returns the total income, total expenses, and net savings """
        income = sum(e["amount"] for e in self.entries if e["type"] == "income")
        expense = sum(e["amount"] for e in self.entries if e["type"] == "expense")
        return {
            "total_income": income,
            "total_expense": expense,
            "net_savings": income - expense
        }

    def view_summary(self):
        """ Formats and returns a string summary of the budget """
        summary = self.get_summary()  # Get summary data
        formatted_summary = (
            f"Total Income: ${summary['total_income']:.2f}\n"
            f"Total Expenses: ${summary['total_expense']:.2f}\n"
            f"Net Savings: ${summary['net_savings']:.2f}"
        )
        return formatted_summary
