import datetime as dt
import json
import tkinter as tk
from tkinter import messagebox, simpledialog
import re

filename = 'Expenses.json'

class Expense:
    def __init__(self, amount, category, description, date=None):
        self.amount = amount
        self.category = category
        self.description = description
        self.date = date if date else dt.datetime.now().strftime('%Y-%m-%d')

    def to_dict(self):
        return {
            'amount': self.amount,
            'category': self.category,
            'description': self.description,
            'date': self.date
        }
        
class ExpensesTracker:
    def __init__(self):
        self.expenses = self.load_expenses()
        self.root = tk.Tk()
        self.root.title('Expense Tracker')
        self.create_GUI()
        self.root.mainloop()


    def load_expenses(self):
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        
    def save_expense(self):
        with open(filename, 'w') as f:
            json.dump(self.expenses, f, indent=2)
    
    def view_expenses(self):
        try:
            with open(filename, 'r') as f:
                expenses_list = json.load(f)
                if not expenses_list:
                    messagebox.showinfo("No expenses in list")
                    return
                else:
                    expense_list = [
                        f"{idx}. Amount: £{float(exp['amount']):.2f}, Category: {exp['category']}, "
                        f"Description: {exp['description']}, Date: {exp['date']}"
                        for idx, exp in enumerate(self.expenses, start=1)
                    ]
        
                    messagebox.showinfo(f'\nExpenses List', '\n'.join(expense_list))
        except FileNotFoundError:
            messagebox.showerror('File not found')
            return
        
    def add_expense(self):
        try:
            amount = simpledialog.askfloat('Add Expense', "Enter expense amount (£XX.XX): ")
            if amount is None:
                return
            category = simpledialog.askstring('Add Expense', "Enter category (e.g. Food, Transport): ")
            if not category:
                return
            description = simpledialog.askstring('Add Expense', "Enter description of expense: ")
            if not description:
                return
            date = simpledialog.askstring("Add Expense", "Enter date (YYYY-MM-DD) or leave blank for today:")
            if date and not re.match(r"\d{4}-\d{2}-\d{2}", date):
                messagebox.showerror("Error", "Invalid date format. Using today's date.")
                date = None
        
            expense = Expense(amount, category, description, date)
            self.expenses.append(expense.to_dict())
            self.save_expense()
            messagebox.showinfo('Expense Saved', "Expense has been saved successfully")
        except ValueError:
            messagebox.showerror('Error', "Invalid input. Please enter a valid number for amount")

    def remove_expense(self):
        if not self.expenses:
            messagebox.showerror("Error", 'No expenses to delete')
            return
        
        self.view_expenses()
        try:
            idx = simpledialog.askinteger('Remove Expense', "Enter an expense to delete: ")
            if idx is None:
                return
            if 1 <= idx < len(self.expenses):
                deleted_expense = self.expenses.pop(idx-1)
                self.save_expense()
                messagebox.showinfo(title='Expense Removed', message=f"Deleted expense: {deleted_expense['category']} - £{deleted_expense['amount']}")
            else:
                messagebox.showerror(title='Error', message='Invalid Input Range')
                return
        except ValueError:
            messagebox.showerror(title='Error', message='Value Error. Enter an integer')

    def calculate_total(self):
        total = sum(float(expense['amount']) for expense in self.expenses)
        messagebox.showinfo(title='Total Expenses', message=f'Expenses add up to £{total:.2f}')

    def on_closing(self):
        if messagebox.askyesno(title='Quit?', message="Do you really want to quit?"):
            self.root.destroy()


    def create_GUI(self):
        tk.Button(self.root, text='Add Expense', font=('Arial', 18), command=self.add_expense).pack(padx=10, pady=10)
        tk.Button(self.root, text='View Expenses', font=('Arial', 18), command=self.view_expenses).pack(padx=10, pady=10)
        tk.Button(self.root, text='Delete Expense', font=('Arial', 18), command=self.remove_expense).pack(padx=10, pady=10)
        tk.Button(self.root, text='Calculate Total', font=('Arial', 18), command=self.calculate_total).pack(padx=10, pady=10)
        tk.Button(self.root, text='Exit', font=('Arial', 18), command=self.on_closing).pack(padx=10, pady=10)


if __name__ == "__main__":
    ExpensesTracker()
