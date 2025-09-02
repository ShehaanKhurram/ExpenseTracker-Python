import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style
import sqlite3

# ---------- Database Handling ----------
def create_db():
    conn = sqlite3.connect("ExpenseTracker.db")
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS expenses(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATE, 
        amount REAL, 
        category TEXT, 
        description TEXT)""")
    conn.commit()
    conn.close()

def insert_expense(date, amount, category, description):
    conn = sqlite3.connect("ExpenseTracker.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO expenses (date, amount, category, description) VALUES (?,?,?,?)",
                (date, amount, category, description))
    conn.commit()
    conn.close()

def delete_expense(expense_id):
    conn = sqlite3.connect("ExpenseTracker.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    conn.commit()
    conn.close()

def fetch_expense():
    conn = sqlite3.connect("ExpenseTracker.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM expenses")
    rows = cur.fetchall()
    conn.close()
    return rows

# ---------- GUI ----------
class ExpenseTracker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Expense Tracker")
        self.geometry("1000x500")
        style = Style("darkly")

        # ---------- MenuBar ----------
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        about_menu = tk.Menu(menubar, tearoff=0)
        about_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "Expense Tracker made by Shehaan Khurram!"))
        menubar.add_cascade(label="About", menu=about_menu)

        # ---------- Labels and Entries ----------
        ttk.Label(self,text="Date:").grid(row=0, column=0, pady=10, sticky="e")
        self.date_entry = ttk.Entry(self)
        self.date_entry.grid(row=0,column=1,padx=5,pady=10, sticky="w")

        ttk.Label(self,text="Category:").grid(row=0, column=2, pady=10, sticky="e")
        self.category_entry = ttk.Entry(self)
        self.category_entry.grid(row=0,column=3,padx=5,pady=10, sticky="w")

        ttk.Label(self,text="Amount:").grid(row=1, column=0, pady=10, sticky="e")
        self.amount_entry = ttk.Entry(self)
        self.amount_entry.grid(row=1,column=1,padx=5,pady=10, sticky="w")

        ttk.Label(self,text="Description:").grid(row=1, column=2, pady=10, sticky="e")
        self.desc_entry = ttk.Entry(self)
        self.desc_entry.grid(row=1,column=3,padx=5,pady=10, sticky="w")

        # ---------- Treeview ----------
        table_frame = tk.Frame(self)
        table_frame.grid(row=2,column=0, columnspan=4, padx=5, pady=5, sticky="nsew")
        self.grid_rowconfigure(2, weight=1)  
        for col in range(4):
            self.grid_columnconfigure(col, weight=1)   
        
        scroll = ttk.Scrollbar(table_frame, orient="vertical")
        columns = ("ID", "Date", "Amount", "Category", "Description")
        self.tree = ttk.Treeview(table_frame,columns=columns, show="headings", yscrollcommand=scroll.set)

        self.tree.column("ID", width=0,stretch=False)

        for i in columns:
            self.tree.heading(i, text=i)
            self.tree.column(i, anchor="center")

        scroll.config(command=self.tree.yview)
        scroll.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

        # ---------- Buttons ----------
        button_frame = tk.Frame(self)
        button_frame.grid(row=3,column=0, columnspan=4, pady=10)

        ttk.Button(button_frame, text="Add Expense", command=self.add_expense).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Remove Expense", command=self.remove_expense).pack(side="left", padx=5)

        self.load_expense()  
    # ---------- Methods ----------
    def load_expense(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in fetch_expense():
            self.tree.insert("", tk.END, values=row)

    def add_expense(self):
        date = self.date_entry.get()
        amount = self.amount_entry.get()
        category = self.category_entry.get()
        desc = self.desc_entry.get()

        if not (date and amount and category):
            messagebox.showwarning("Input Error", "Please fill Date, Amount, and Category!")
            return

        insert_expense(date, amount, category, desc)
        self.load_expense()

        self.date_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)

    def remove_expense(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Selection Error", "Please select an entry to remove!")
            return

        for item in selection:
            values = self.tree.item(item, "values")
            expense_id = values[0] 
            delete_expense(expense_id)
            self.tree.delete(item)


create_db()
app = ExpenseTracker()
app.mainloop()
