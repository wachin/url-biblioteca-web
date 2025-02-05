import tkinter as tk
from tkinter import ttk, messagebox
import json
import webbrowser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

# Archivo donde se almacenarán los enlaces
DATA_FILE = "links.json"

# Cargar enlaces guardados
def load_links():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {}

# Guardar enlaces en archivo
def save_links(links):
    with open(DATA_FILE, "w") as file:
        json.dump(links, file, indent=4)

# Obtener título de la URL
def get_page_title(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.title.string if soup.title else url
    except:
        return url

# Función para abrir URL en navegador predeterminado
def open_url(url):
    webbrowser.open(url)

# Agregar nueva URL
def add_link():
    url = entry.get().strip()
    if not url:
        return
    
    title = get_page_title(url)
    today = datetime.today().strftime("%Y-%m-%d")
    
    if today not in links:
        links[today] = []
    
    links[today].append({"url": url, "title": title})
    save_links(links)
    entry.delete(0, tk.END)
    display_links()

# Eliminar URL seleccionada
def delete_selected():
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showwarning("Advertencia", "Selecciona al menos un enlace para eliminar.")
        return
    
    for item in selected_items:
        values = tree.item(item, "values")
        date, url = values[0], values[1]
        links[date] = [link for link in links[date] if link["url"] != url]
        if not links[date]:
            del links[date]
    
    save_links(links)
    display_links()

# Mostrar enlaces en la interfaz
def display_links():
    tree.delete(*tree.get_children())
    for date, items in links.items():
        for link in items:
            tree.insert("", "end", values=(date, link["url"], link["title"]))

# Configuración de la GUI
root = tk.Tk()
root.title("Biblioteca de Enlaces")
root.geometry("600x600")

frame = ttk.Frame(root)
frame.pack(pady=10, padx=10, fill="x")

entry = ttk.Entry(frame, width=50)
entry.pack(side="left", padx=5)

btn_add = ttk.Button(frame, text="Agregar", command=add_link)
btn_add.pack(side="left", padx=5)

btn_delete = ttk.Button(frame, text="Eliminar", command=delete_selected)
btn_delete.pack(side="left", padx=5)

columns = ("Fecha", "URL", "Título")
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=200)

tree.pack(pady=10, padx=10, fill="both", expand=True)

tree.bind("<Double-1>", lambda event: open_url(tree.item(tree.selection(), "values")[1]))

links = load_links()
display_links()

root.mainloop()
