# Expense Tracker

A command-line expense tracker built with Python, SQLite, and Matplotlib. Record your daily spending, view monthly summaries, and visualize where your money goes.

## Features
- Add, view, and delete expenses (date, category, amount, note)
- Persistent storage using SQLite (no setup needed)
- Monthly summary with category-wise totals
- Category-wise pie chart for any month
- Monthly spending trend bar chart
- Export all data to CSV
- Input validation for dates, amounts, and menu choices

## Tech Stack
Python 3, SQLite3, Matplotlib

## How to Run
```bash
git clone https://github.com/<your-username>/expense-tracker.git
cd expense-tracker
pip install -r requirements.txt
python expense_tracker.py
```

## Project Structure
```
expense-tracker/
├── expense_tracker.py   # main application
├── requirements.txt
└── README.md
```

## Screenshots
_Add screenshots of the menu, monthly summary, and pie chart here._

## Future Improvements
- Tkinter GUI
- Budget limits with alerts
- Recurring expenses