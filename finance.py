import sqlite3
from tkinter import *
from tkinter import messagebox

# DB setup
def init_db():
    conn = sqlite3.connect("finance.db")
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY,
            type TEXT,
            category TEXT,
            amount REAL,
            note TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert(type_, category, amount, note):
    conn = sqlite3.connect("finance.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO transactions VALUES (NULL, ?, ?, ?, ?)", (type_, category, amount, note))
    conn.commit()
    conn.close()
    view_all()

def view_all():
    listbox.delete(0, END)
    conn = sqlite3.connect("finance.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM transactions")
    rows = cur.fetchall()
    conn.close()
    for row in rows:
        listbox.insert(END, row)
    update_summary()

def delete():
    if selected_transaction:
        conn = sqlite3.connect("finance.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM transactions WHERE id=?", (selected_transaction[0],))
        conn.commit()
        conn.close()
        view_all()

def update_summary():
    conn = sqlite3.connect("finance.db")
    cur = conn.cursor()
    cur.execute("SELECT SUM(amount) FROM transactions WHERE type='Income'")
    income = cur.fetchone()[0] or 0

    cur.execute("SELECT SUM(amount) FROM transactions WHERE type='Expense'")
    expense = cur.fetchone()[0] or 0

    balance = income - expense
    summary_label.config(text=f"💵 Income: ₹{income:.2f} | 💸 Expense: ₹{expense:.2f} | 🧾 Balance: ₹{balance:.2f}")
    conn.close()

def on_select(event):
    global selected_transaction
    index = listbox.curselection()
    if index:
        selected_transaction = listbox.get(index[0])
        type_var.set(selected_transaction[1])
        category_entry.delete(0, END)
        category_entry.insert(END, selected_transaction[2])
        amount_entry.delete(0, END)
        amount_entry.insert(END, selected_transaction[3])
        note_entry.delete(0, END)
        note_entry.insert(END, selected_transaction[4])

# GUI setup
init_db()
window = Tk()
window.title("Personal Finance Tracker")
window.geometry("600x500")

type_var = StringVar(value="Expense")

Label(window, text="Type").grid(row=0, column=0)
OptionMenu(window, type_var, "Income", "Expense").grid(row=0, column=1)

Label(window, text="Category").grid(row=1, column=0)
category_entry = Entry(window)
category_entry.grid(row=1, column=1)

Label(window, text="Amount").grid(row=2, column=0)
amount_entry = Entry(window)
amount_entry.grid(row=2, column=1)

Label(window, text="Note").grid(row=3, column=0)
note_entry = Entry(window)
note_entry.grid(row=3, column=1)

Button(window, text="Add Transaction", command=lambda: insert(
    type_var.get(), category_entry.get(), float(amount_entry.get()), note_entry.get())
).grid(row=4, column=0, columnspan=2, pady=10)

listbox = Listbox(window, height=10, width=70)
listbox.grid(row=5, column=0, columnspan=3, rowspan=6, padx=10)
listbox.bind('<<ListboxSelect>>', on_select)

Button(window, text="Delete", width=12, command=delete).grid(row=5, column=3)
Button(window, text="View All", width=12, command=view_all).grid(row=6, column=3)
Button(window, text="Exit", width=12, command=window.destroy).grid(row=7, column=3)

summary_label = Label(window, text="💵 Income: ₹0 | 💸 Expense: ₹0 | 🧾 Balance: ₹0", font=('Arial', 12, 'bold'))
summary_label.grid(row=12, column=0, columnspan=4, pady=20)

view_all()
window.mainloop()
