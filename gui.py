import tkinter as tk
from tkinter import ttk, messagebox
from budget_manager import BudgetManager
from stats_visualizer import show_expense_pie_chart, show_monthly_statistics, show_yearly_statistics


class SmartBudgetGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("💰 SmartBudget – Personal Finance Tracker")
        self.root.geometry("420x580")
        self.root.configure(bg="#f7f7f7")

        self.manager = BudgetManager()

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TLabel", font=("Segoe UI", 11), background="#f7f7f7")
        self.style.configure("TEntry", font=("Segoe UI", 11), padding=4)

        # Define colored styles using existing 'TButton' layout
        self.button_colors = [
            "#4caf50", "#f44336", "#2196f3",
            "#9c27b0", "#ff9800", "#3f51b5",
            "#795548", "#607d8b"
        ]
        for i, color in enumerate(self.button_colors):
            style_name = f"Colored{i}.TButton"
            self.style.configure(style_name,
                                 font=("Segoe UI", 11, "bold"),
                                 background=color,
                                 foreground="white")
            self.style.map(style_name,
                           background=[("active", "#333")],
                           foreground=[("disabled", "gray")])

        self.create_widgets()

    def create_widgets(self):
        input_frame = ttk.Frame(self.root, padding="20 10 20 10")
        input_frame.pack(fill=tk.X)

        ttk.Label(input_frame, text="💵 Amount:").grid(row=0, column=0, sticky=tk.W, pady=8)
        self.amount_entry = ttk.Entry(input_frame)
        self.amount_entry.grid(row=0, column=1, pady=8)

        ttk.Label(input_frame, text="📂 Category:").grid(row=1, column=0, sticky=tk.W, pady=8)
        self.category_entry = ttk.Entry(input_frame)
        self.category_entry.grid(row=1, column=1, pady=8)

        button_frame = ttk.Frame(self.root, padding="20")
        button_frame.pack(fill=tk.BOTH, expand=True)

        buttons = [
            ("➕ Add Income", self.add_income),
            ("➖ Add Expense", self.add_expense),
            ("📋 View All Entries", self.view_entries),
            ("📊 View Summary", self.view_summary),
            ("🥧 Show Expense Pie", self.show_expense_pie),
            ("📅 Monthly Bar Chart", self.show_monthly_bar),
            ("📈 Yearly Statistics", self.show_yearly_statistics),
            ("🚪 Exit", self.quit),
        ]

        for i, (text, command) in enumerate(buttons):
            style_name = f"Colored{i}.TButton"
            btn = ttk.Button(button_frame, text=text, command=command, style=style_name)
            btn.grid(row=i, column=0, pady=6, padx=10, sticky="ew")

    def add_income(self):
        try:
            amount = float(self.amount_entry.get())
            category = self.category_entry.get()
            if not category:
                messagebox.showerror("Error", "Category cannot be empty!")
                return
            self.manager.add_entry(amount, category, "income")
            messagebox.showinfo("Success", "Income added successfully!")
            self.clear_entries()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")

    def add_expense(self):
        try:
            amount = float(self.amount_entry.get())
            category = self.category_entry.get()
            if not category:
                messagebox.showerror("Error", "Category cannot be empty!")
                return
            self.manager.add_entry(amount, category, "expense")
            messagebox.showinfo("Success", "Expense added successfully!")
            self.clear_entries()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")

    def clear_entries(self):
        self.amount_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)

    def view_entries(self):
        entries = self.manager.list_entries()
        if not entries:
            messagebox.showinfo("All Entries", "No entries found.")
            return

        table_window = tk.Toplevel(self.root)
        table_window.title("📋 All Entries")
        table_window.geometry("500x400")

        columns = ("Date", "Type", "Category", "Amount")

        tree = ttk.Treeview(table_window, columns=columns, show="headings")
        tree.heading("Date", text="Date")
        tree.heading("Type", text="Type")
        tree.heading("Category", text="Category")
        tree.heading("Amount", text="Amount")

        # Add a scrollbar
        scrollbar = ttk.Scrollbar(table_window, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Insert data into the table
        for entry in entries:
            tree.insert("", "end", values=(
                entry["date"], entry["type"], entry["category"], f"${entry['amount']:.2f}"
            ))


    def view_summary(self):
        summary = self.manager.get_summary()

        summary_window = tk.Toplevel(self.root)
        summary_window.title("📊 Summary Overview")
        summary_window.geometry("350x200")
        summary_window.configure(bg="#f7f7f7")

        frame = ttk.Frame(summary_window, padding="20 10 20 10")
        frame.pack(fill="both", expand=True)

        # Labels with icons
        ttk.Label(frame, text="💰 Total Income:", font=("Segoe UI", 12, "bold")).grid(row=0, column=0, sticky="w", pady=10)
        ttk.Label(frame, text=f"${summary['total_income']:.2f}", font=("Segoe UI", 12)).grid(row=0, column=1, sticky="e")

        ttk.Label(frame, text="💸 Total Expense:", font=("Segoe UI", 12, "bold")).grid(row=1, column=0, sticky="w", pady=10)
        ttk.Label(frame, text=f"${summary['total_expense']:.2f}", font=("Segoe UI", 12)).grid(row=1, column=1, sticky="e")

        net = summary['net_savings']
        net_color = "#4caf50" if net >= 0 else "#f44336"
        net_label = ttk.Label(frame, text="💼 Net Savings:", font=("Segoe UI", 12, "bold"))
        net_label.grid(row=2, column=0, sticky="w", pady=10)

        net_value = ttk.Label(frame, text=f"${net:.2f}", font=("Segoe UI", 12))
        net_value.grid(row=2, column=1, sticky="e")

        # Manually apply color using regular tk.Label for colored value
        net_value.configure(foreground=net_color)


    def show_expense_pie(self):
        entries = self.manager.list_entries()
        show_expense_pie_chart(entries)

    def show_monthly_bar(self):
        entries = self.manager.list_entries()
        show_monthly_statistics(entries)

    def show_yearly_statistics(self):
        entries = self.manager.list_entries()
        show_yearly_statistics(entries)

    def quit(self):
        self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = SmartBudgetGUI(root)
    root.mainloop()
