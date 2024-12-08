import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3

def fetch_test_query(query):
    conn = sqlite3.connect("greek_mythology.db")
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        if query.strip().lower().startswith("select"): 
            results = cursor.fetchall()
            conn.close()
            return results
        else: 
            conn.commit()
            conn.close()
            return f"Query executed successfully: {cursor.rowcount} rows affected."
    except Exception as e:
        conn.close()
        return f"Error: {e}"

def show_query_results():
    query = query_entry.get()
    if not query:
        messagebox.showerror("Error", "Please enter a query.")
        return
    results = fetch_test_query(query)
    if isinstance(results, str): 
        if "Error" in results:
            messagebox.showerror("Error", results)
        else:
            messagebox.showinfo("Query Execution", results)
    else:  
        display = "\n".join([", ".join(map(str, row)) for row in results])
        messagebox.showinfo("Query Results", display if display else "No results found.")

def add_data(table):
    conn = sqlite3.connect("greek_mythology.db")
    cursor = conn.cursor()

    if table == "Deity":
        fields = {"moniker": "Name", "domain": "Domain", "parents": "Parents", "symbol": "Symbol"}
    elif table == "Hero":
        fields = {"moniker": "Name", "origin": "Origin", "parents": "Parents", "legacy": "Legacy"}
    elif table == "Legend":
        fields = {"title": "Title", "summary": "Summary", "time_period": "Time Period"}
    
    data = {}
    for field, label in fields.items():
        value = simpledialog.askstring("Input", f"Enter {label}:")
        if value:
            data[field] = value
        else:
            messagebox.showerror("Error", f"{label} is required.")
            conn.close()
            return

    try:
        placeholders = ", ".join(["?"] * len(data))
        columns = ", ".join(data.keys())
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        cursor.execute(query, tuple(data.values()))
        conn.commit()
        messagebox.showinfo("Success", f"{table} added successfully")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add {table}: {e}")
    conn.close()

def update_data(table):
    conn = sqlite3.connect("greek_mythology.db")
    cursor = conn.cursor()

    identifier = simpledialog.askstring("Input", f"Enter the name/title of the {table} to update:")
    if not identifier:
        messagebox.showerror("Error", "Identifier is required.")
        conn.close()
        return

    fields = {"Deity": {"domain": "Domain", "parents": "Parents", "symbol": "Symbol"},
              "Hero": {"origin": "Origin", "parents": "Parents", "legacy": "Legacy"},
              "Legend": {"summary": "Summary", "time_period": "Time Period"}}

    updates = []
    for field, label in fields[table].items():
        new_value = simpledialog.askstring("Input", f"Enter new {label} (leave blank to skip):")
        if new_value:
            updates.append(f"{field} = ?")

    if updates:
        query = f"UPDATE {table} SET {', '.join(updates)} WHERE moniker = ?" if table != "Legend" else f"UPDATE {table} SET {', '.join(updates)} WHERE title = ?"
        try:
            cursor.execute(query, (*[v for v in updates if v], identifier))
            conn.commit()
            messagebox.showinfo("Success", f"{table} '{identifier}' updated successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update {table}: {e}")
    else:
        messagebox.showerror("Error", "No updates provided.")
    conn.close()

def delete_data(table):
    conn = sqlite3.connect("greek_mythology.db")
    cursor = conn.cursor()

    identifier = simpledialog.askstring("Input", f"Enter the name/title of the {table} to delete:")
    if not identifier:
        messagebox.showerror("Error", "Identifier is required.")
        conn.close()
        return

    try:
        column = "moniker" if table != "Legend" else "title"
        cursor.execute(f"DELETE FROM {table} WHERE {column} = ?", (identifier,))
        conn.commit()
        if cursor.rowcount > 0:
            messagebox.showinfo("Success", f"{table} '{identifier}' deleted successfully")
        else:
            messagebox.showinfo("Not Found", f"No {table} named '{identifier}' found.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to delete {table}: {e}")
    conn.close()

root = tk.Tk()
root.title("Greek Mythology Database")

tk.Label(root, text="Enter your query:").pack(pady=5)
query_entry = tk.Entry(root, width=50)
query_entry.pack(pady=5)

tk.Button(root, text="Execute Query", command=show_query_results).pack(pady=10)

tk.Button(root, text="Add New Deity", command=lambda: add_data("Deity")).pack(pady=10)
tk.Button(root, text="Add New Hero", command=lambda: add_data("Hero")).pack(pady=10)
tk.Button(root, text="Add New Legend", command=lambda: add_data("Legend")).pack(pady=10)

tk.Button(root, text="Update Deity", command=lambda: update_data("Deity")).pack(pady=10)
tk.Button(root, text="Update Hero", command=lambda: update_data("Hero")).pack(pady=10)
tk.Button(root, text="Update Legend", command=lambda: update_data("Legend")).pack(pady=10)

tk.Button(root, text="Delete Deity", command=lambda: delete_data("Deity")).pack(pady=10)
tk.Button(root, text="Delete Hero", command=lambda: delete_data("Hero")).pack(pady=10)
tk.Button(root, text="Delete Legend", command=lambda: delete_data("Legend")).pack(pady=10)

root.mainloop()
