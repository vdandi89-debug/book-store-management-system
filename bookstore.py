import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

# =========================================================
# MYSQL DATABASE SETTINGS
# =========================================================
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "vedant123"
DB_NAME = "bookstore_db"

# =========================================================
# INITIALIZE DATABASE
# =========================================================
def init_db():
    try:
        # Connect to MySQL
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        
        
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        
        
        cursor.execute(f"USE {DB_NAME}")
        
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                book_id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                author VARCHAR(255) NOT NULL,
                genre VARCHAR(100),
                price DECIMAL(10, 2) NOT NULL,
                quantity INT NOT NULL
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Error as err:
        messagebox.showerror("Database Error", f"Could not connect to MySQL.\n\n{err}")
        return False

# =========================================================
# DATABASE CONNECTION
# =========================================================
def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

# =========================================================
# MAIN APPLICATION
# =========================================================
class BookstoreApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Book Store Management System")
        self.geometry("1000x650")
        self.resizable(True, True)
        self.configure(bg="#f0f2f5")
        
        self.selected_book_id = None
        
        # Initialize database
        if not init_db():
            self.destroy()
            return
            
        # Show login page
        self.show_login_page()

   
    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    # =====================================================
    # LOGIN PAGE
    # =====================================================
    def show_login_page(self):
        self.clear_window()
        
        login_frame = tk.Frame(self, bg="white", bd=2, relief="groove", padx=40, pady=40)
        login_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(login_frame, text="Admin Login", font=("Arial", 24, "bold"), bg="white", fg="#333333").grid(row=0, column=0, columnspan=2, pady=(0, 30))
        
        # Username
        tk.Label(login_frame, text="Username:", font=("Arial", 12), bg="white").grid(row=1, column=0, sticky="w", pady=10)
        self.username_entry = tk.Entry(login_frame, font=("Arial", 12), width=25)
        self.username_entry.grid(row=1, column=1, pady=10)
        
        # Password
        tk.Label(login_frame, text="Password:", font=("Arial", 12), bg="white").grid(row=2, column=0, sticky="w", pady=10)
        self.password_entry = tk.Entry(login_frame, font=("Arial", 12), width=25, show="*")
        self.password_entry.grid(row=2, column=1, pady=10)
        
        # Login button
        tk.Button(login_frame, text="Login", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", width=18, cursor="hand2", command=self.validate_login).grid(row=3, column=0, columnspan=2, pady=(25, 10))
        
        tk.Label(login_frame, text="Login: admin / admin123", font=("Arial", 9), bg="white", fg="gray").grid(row=4, column=0, columnspan=2, pady=5)
        
        self.username_entry.focus()
        self.bind("<Return>", lambda event: self.validate_login())

    # =====================================================
    # LOGIN VALIDATION
    # =====================================================
    def validate_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if username == "admin" and password == "admin123":
            messagebox.showinfo("Login Successful", "Welcome to the Book Store Management System!")
            self.show_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid Username or Password.")

    # =====================================================
    # DASHBOARD
    # =====================================================
    def show_dashboard(self):
        self.clear_window()
        
        # ---------------- HEADER ----------------
        header_frame = tk.Frame(self, bg="#333333", height=60)
        header_frame.pack(fill="x", side="top")
        
        tk.Label(header_frame, text="Book Store Dashboard", font=("Arial", 18, "bold"), fg="white", bg="#333333").pack(side="left", padx=20, pady=15)
        tk.Button(header_frame, text="Logout", font=("Arial", 10, "bold"), bg="#f44336", fg="white", command=self.show_login_page).pack(side="right", padx=20, pady=12)
        
        # ---------------- BOOK INFORMATION ----------------
        form_frame = tk.LabelFrame(self, text="Book Information", font=("Arial", 12, "bold"), bg="#f0f2f5", padx=15, pady=15)
        form_frame.pack(fill="x", padx=20, pady=15)
        
        # Title
        tk.Label(form_frame, text="Title:", bg="#f0f2f5", font=("Arial", 11)).grid(row=0, column=0, padx=5, pady=8, sticky="w")
        self.title_entry = tk.Entry(form_frame, font=("Arial", 11), width=25)
        self.title_entry.grid(row=0, column=1, padx=5, pady=8)
        
        # Author
        tk.Label(form_frame, text="Author:", bg="#f0f2f5", font=("Arial", 11)).grid(row=0, column=2, padx=5, pady=8, sticky="w")
        self.author_entry = tk.Entry(form_frame, font=("Arial", 11), width=25)
        self.author_entry.grid(row=0, column=3, padx=5, pady=8)
        
        # Genre
        tk.Label(form_frame, text="Genre:", bg="#f0f2f5", font=("Arial", 11)).grid(row=1, column=0, padx=5, pady=8, sticky="w")
        self.genre_entry = tk.Entry(form_frame, font=("Arial", 11), width=25)
        self.genre_entry.grid(row=1, column=1, padx=5, pady=8)
        
        # Price
        tk.Label(form_frame, text="Price:", bg="#f0f2f5", font=("Arial", 11)).grid(row=1, column=2, padx=5, pady=8, sticky="w")
        self.price_entry = tk.Entry(form_frame, font=("Arial", 11), width=25)
        self.price_entry.grid(row=1, column=3, padx=5, pady=8)
        
        # Quantity
        tk.Label(form_frame, text="Quantity:", bg="#f0f2f5", font=("Arial", 11)).grid(row=2, column=0, padx=5, pady=8, sticky="w")
        self.quantity_entry = tk.Entry(form_frame, font=("Arial", 11), width=25)
        self.quantity_entry.grid(row=2, column=1, padx=5, pady=8)
        
        # ---------------- BUTTONS ----------------
        button_frame = tk.Frame(self, bg="#f0f2f5")
        button_frame.pack(fill="x", padx=20, pady=5)
        
        tk.Button(button_frame, text="Add Book", font=("Arial", 10, "bold"), bg="#4CAF50", fg="white", width=15, command=self.add_book).pack(side="left", padx=5)
        tk.Button(button_frame, text="Update Book", font=("Arial", 10, "bold"), bg="#2196F3", fg="white", width=15, command=self.update_book).pack(side="left", padx=5)
        tk.Button(button_frame, text="Delete Book", font=("Arial", 10, "bold"), bg="#f44336", fg="white", width=15, command=self.delete_book).pack(side="left", padx=5)
        tk.Button(button_frame, text="Clear", font=("Arial", 10, "bold"), bg="#777777", fg="white", width=15, command=self.clear_entries).pack(side="left", padx=5)
        
        
        table_frame = tk.Frame(self, bg="#f0f2f5")
        table_frame.pack(fill="both", expand=True, padx=20, pady=15)
        
        columns = ("ID", "Title", "Author", "Genre", "Price", "Quantity")
        self.book_table = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        
        for column in columns:
            self.book_table.heading(column, text=column)
            
        
        self.book_table.column("ID", width=50, anchor="center")
        self.book_table.column("Title", width=220)
        self.book_table.column("Author", width=180)
        self.book_table.column("Genre", width=120)
        self.book_table.column("Price", width=100, anchor="center")
        self.book_table.column("Quantity", width=100, anchor="center")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.book_table.yview)
        self.book_table.configure(yscrollcommand=scrollbar.set)
        
        self.book_table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.book_table.bind("<<TreeviewSelect>>", self.select_book)
        
        
        self.load_books()

    
    def load_books(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT book_id, title, author, genre, price, quantity FROM books ORDER BY book_id")
            books = cursor.fetchall()
            
            
            for item in self.book_table.get_children():
                self.book_table.delete(item)
            # Add books to table
            for book in books:
                self.book_table.insert("", "end", values=book)
            cursor.close()
            conn.close()
        except Error as err:
            messagebox.showerror("Database Error", str(err))

    # =====================================================
    # ADD BOOK
    # =====================================================
    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        price = self.price_entry.get().strip()
        quantity = self.quantity_entry.get().strip()
        
        if not title or not author or not price or not quantity:
            messagebox.showwarning("Missing Information", "Please enter Title, Author, Price and Quantity.")
            return
            
        try:
            price = float(price)
            quantity = int(quantity)
            if price < 0 or quantity < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Price must be a positive number and Quantity must be a positive integer.")
            return
            
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                INSERT INTO books (title, author, genre, price, quantity) 
                VALUES (%s, %s, %s, %s, %s)
            """
            values = (title, author, genre, price, quantity)
            cursor.execute(query, values)
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Success", "Book added successfully.")
            self.clear_entries()
            self.load_books()
        except Error as err:
            messagebox.showerror("Database Error", str(err))

    # =====================================================
    # SELECT BOOK
    # =====================================================
    def select_book(self, event=None):
        selected = self.book_table.selection()
        if not selected:
            return
        values = self.book_table.item(selected[0], "values")
        if not values:
            return
        self.clear_entries()
        self.selected_book_id = values[0]
        self.title_entry.insert(0, values[1])
        self.author_entry.insert(0, values[2])
        self.genre_entry.insert(0, values[3])
        self.price_entry.insert(0, values[4])
        self.quantity_entry.insert(0, values[5])

    # =====================================================
    # UPDATE BOOK
    # =====================================================
    def update_book(self):
        if self.selected_book_id is None:
            messagebox.showwarning("No Selection", "Please select a book from the table first.")
            return
            
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        price = self.price_entry.get().strip()
        quantity = self.quantity_entry.get().strip()
        
        if not title or not author or not price or not quantity:
            messagebox.showwarning("Missing Information", "Please fill in all required fields.")
            return
            
        try:
            price = float(price)
            quantity = int(quantity)
            if price < 0 or quantity < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Price must be a positive number and Quantity must be a positive integer.")
            return
            
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            values = (title, author, genre, price, quantity, self.selected_book_id)
            cursor.execute("UPDATE books SET title=%s, author=%s, genre=%s, price=%s, quantity=%s WHERE book_id=%s", values)
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Success", "Book updated successfully.")
            self.clear_entries()
            self.load_books()
        except Error as err:
            messagebox.showerror("Database Error", str(err))

    # =====================================================
    # DELETE BOOK
    # =====================================================
    def delete_book(self):
        if self.selected_book_id is None:
            messagebox.showwarning("No Selection", "Please select a book from the table first.")
            return
            
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this book?")
        if not confirm:
            return
            
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM books WHERE book_id=%s", (self.selected_book_id,))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Success", "Book deleted successfully.")
            self.clear_entries()
            self.load_books()
        except Error as err:
            messagebox.showerror("Database Error", str(err))

    
    def clear_entries(self):
        self.selected_book_id = None
        if hasattr(self, "title_entry"):
            self.title_entry.delete(0, tk.END)
            self.author_entry.delete(0, tk.END)
            self.genre_entry.delete(0, tk.END)
            self.price_entry.delete(0, tk.END)
            self.quantity_entry.delete(0, tk.END)
        if hasattr(self, "book_table"):
            for item in self.book_table.selection():
                self.book_table.selection_remove(item)


if __name__ == "__main__":
    app = BookstoreApp()
    app.mainloop()
