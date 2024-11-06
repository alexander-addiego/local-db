import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime

class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Database Manager")
        self.root.geometry("800x600")
        
        # Create database connection
        self.conn = sqlite3.connect('app_database.db')
        self.create_tables()
        
        self.setup_ui()
        
    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            tags TEXT,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        self.conn.commit()
        
    def setup_ui(self):
        # Search frame
        search_frame = ttk.Frame(self.root, padding="5")
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.search_entry.bind('<KeyRelease>', self.search_items)
        
        # Add item frame
        add_frame = ttk.LabelFrame(self.root, text="Add New Item", padding="5")
        add_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(add_frame, text="Title:").grid(row=0, column=0, sticky=tk.W)
        self.title_var = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.title_var).grid(row=0, column=1, sticky=tk.EW)
        
        ttk.Label(add_frame, text="Description:").grid(row=1, column=0, sticky=tk.W)
        self.desc_var = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.desc_var).grid(row=1, column=1, sticky=tk.EW)
        
        ttk.Label(add_frame, text="Tags:").grid(row=2, column=0, sticky=tk.W)
        self.tags_var = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.tags_var).grid(row=2, column=1, sticky=tk.EW)
        
        ttk.Button(add_frame, text="Add Item", command=self.add_item).grid(row=3, column=0, columnspan=2, pady=5)
        
        add_frame.grid_columnconfigure(1, weight=1)
        
        # Results frame
        results_frame = ttk.LabelFrame(self.root, text="Items", padding="5")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Treeview for displaying items
        self.tree = ttk.Treeview(results_frame, columns=('ID', 'Title', 'Description', 'Tags', 'Created'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Title', text='Title')
        self.tree.heading('Description', text='Description')
        self.tree.heading('Tags', text='Tags')
        self.tree.heading('Created', text='Created')
        
        # Column widths
        self.tree.column('ID', width=50)
        self.tree.column('Title', width=150)
        self.tree.column('Description', width=250)
        self.tree.column('Tags', width=150)
        self.tree.column('Created', width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack the tree and scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load initial data
        self.refresh_items()
        
    def add_item(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO items (title, description, tags)
        VALUES (?, ?, ?)
        ''', (self.title_var.get(), self.desc_var.get(), self.tags_var.get()))
        self.conn.commit()
        
        # Clear entry fields
        self.title_var.set('')
        self.desc_var.set('')
        self.tags_var.set('')
        
        self.refresh_items()
        
    def search_items(self, event=None):
        search_term = self.search_var.get().lower()
        cursor = self.conn.cursor()
        
        if search_term:
            cursor.execute('''
            SELECT * FROM items 
            WHERE lower(title) LIKE ? OR lower(description) LIKE ? OR lower(tags) LIKE ?
            ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
        else:
            cursor.execute('SELECT * FROM items')
            
        self.update_tree(cursor.fetchall())
        
    def refresh_items(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM items')
        self.update_tree(cursor.fetchall())
        
    def update_tree(self, rows):
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert('', 'end', values=row)

if __name__ == '__main__':
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()