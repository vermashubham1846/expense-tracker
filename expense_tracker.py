"""Expense Tracker: a command-line app with SQLite storage and matplotlib charts."""
import csv
import sqlite3
from datetime import datetime

import matplotlib.pyplot as plt

DB_NAME = "expenses.db"
CATEGORIES = ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Health", "Other"]


class ExpenseDB:
    """Handles all database operations."""

    def __init__(self, path=DB_NAME):
        self.conn = sqlite3.connect(path)
        self.conn.execute(
            """CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL CHECK(amount > 0),
                note TEXT
            )"""
        )
        self.conn.commit()

    def add(self, date, category, amount, note=""):
        self.conn.execute(
            "INSERT INTO expenses (date, category, amount, note) VALUES (?, ?, ?, ?)",
            (date, category, amount, note),
        )
        self.conn.commit()

    def get_all(self):
        return self.conn.execute(
            "SELECT id, date, category, amount, note FROM expenses ORDER BY date DESC"
        ).fetchall()

    def delete(self, expense_id):
        cur = self.conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        self.conn.commit()
        return cur.rowcount > 0

    def category_totals(self, month=None):
        """Total spent per category. month is 'YYYY-MM' or None for all time."""
        query = "SELECT category, SUM(amount) FROM expenses"
        params = ()
        if month:
            query += " WHERE substr(date, 1, 7) = ?"
            params = (month,)
        query += " GROUP BY category ORDER BY SUM(amount) DESC"
        return self.conn.execute(query, params).fetchall()

    def monthly_totals(self):
        return self.conn.execute(
            "SELECT substr(date, 1, 7) AS month, SUM(amount) FROM expenses "
            "GROUP BY month ORDER BY month"
        ).fetchall()

    def export_csv(self, filename="expenses_export.csv"):
        rows = self.get_all()
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Date", "Category", "Amount", "Note"])
            writer.writerows(rows)
        return filename, len(rows)


# ---------- Input helpers ----------

def ask_date():
    while True:
        value = input("Date (YYYY-MM-DD, press Enter for today): ").strip()
        if not value:
            return datetime.today().strftime("%Y-%m-%d")
        try:
            return datetime.strptime(value, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Try again.")


def ask_amount():
    while True:
        try:
            amount = float(input("Amount: ").strip())
            if amount > 0:
                return amount
            print("Amount must be greater than 0.")
        except ValueError:
            print("Please enter a valid number.")


def ask_category():
    print("Categories:")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"  {i}. {cat}")
    while True:
        choice = input("Choose category number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(CATEGORIES):
            return CATEGORIES[int(choice) - 1]
        print("Invalid choice. Try again.")


def ask_month():
    while True:
        value = input("Month (YYYY-MM, press Enter for current month): ").strip()
        if not value:
            return datetime.today().strftime("%Y-%m")
        try:
            return datetime.strptime(value, "%Y-%m").strftime("%Y-%m")
        except ValueError:
            print("Invalid format. Use YYYY-MM.")


# ---------- Features ----------

def add_expense(db):
    date = ask_date()
    category = ask_category()
    amount = ask_amount()
    note = input("Note (optional): ").strip()
    db.add(date, category, amount, note)
    print("Expense added.")


def view_expenses(db):
    rows = db.get_all()
    if not rows:
        print("No expenses recorded yet.")
        return
    print(f"\n{'ID':<5}{'Date':<13}{'Category':<15}{'Amount':>10}  Note")
    print("-" * 60)
    for eid, date, cat, amount, note in rows:
        print(f"{eid:<5}{date:<13}{cat:<15}{amount:>10.2f}  {note or ''}")
    print("-" * 60)
    print(f"{'Total':<33}{sum(r[3] for r in rows):>10.2f}")


def delete_expense(db):
    view_expenses(db)
    value = input("Enter ID to delete: ").strip()
    if value.isdigit() and db.delete(int(value)):
        print("Expense deleted.")
    else:
        print("No expense found with that ID.")


def monthly_summary(db):
    month = ask_month()
    totals = db.category_totals(month)
    if not totals:
        print(f"No expenses found for {month}.")
        return
    print(f"\nSummary for {month}")
    print("-" * 30)
    for cat, total in totals:
        print(f"{cat:<15}{total:>12.2f}")
    print("-" * 30)
    print(f"{'Total':<15}{sum(t for _, t in totals):>12.2f}")


def show_pie_chart(db):
    month = ask_month()
    totals = db.category_totals(month)
    if not totals:
        print(f"No expenses found for {month}.")
        return
    labels, values = zip(*totals)
    plt.figure(figsize=(7, 7))
    plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=140)
    plt.title(f"Spending by Category: {month}")
    plt.show()


def show_monthly_bar_chart(db):
    data = db.monthly_totals()
    if not data:
        print("No expenses recorded yet.")
        return
    months, totals = zip(*data)
    plt.figure(figsize=(9, 5))
    plt.bar(months, totals, color="steelblue")
    plt.xlabel("Month")
    plt.ylabel("Total Spent")
    plt.title("Monthly Spending Trend")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def export_data(db):
    filename, count = db.export_csv()
    print(f"Exported {count} records to {filename}")


MENU = """
===== EXPENSE TRACKER =====
1. Add expense
2. View all expenses
3. Delete expense
4. Monthly summary
5. Category pie chart
6. Monthly spending chart
7. Export to CSV
0. Exit
"""


def main():
    db = ExpenseDB()
    actions = {
        "1": add_expense,
        "2": view_expenses,
        "3": delete_expense,
        "4": monthly_summary,
        "5": show_pie_chart,
        "6": show_monthly_bar_chart,
        "7": export_data,
    }
    while True:
        print(MENU)
        choice = input("Enter choice: ").strip()
        if choice == "0":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action:
            action(db)
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
