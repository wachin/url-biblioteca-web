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
    return {"Pestaña 1": {}}

# Guardar enlaces en archivo
def save_links(links):
    with open(DATA_FILE, "w") as file:
        json.dump(links, file, indent=4)

# Obtener título de la URL
def get_page_title(url):
    if url.lower().endswith(".pdf"):
        return os.path.basename(url)
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.title.string if soup.title else url
    except:
        return url

# Función para abrir URL en navegador predeterminado
def open_url(event):
    selected_item = tree.focus()
    if selected_item:
        url = tree.item(selected_item, "values")[1]
        webbrowser.open(url)

# Agregar nueva URL
def add_link():
    url = entry.get().strip()
    if not url:
        return
    
    title = get_page_title(url)
    today = datetime.today().strftime("%Y-%m-%d")
    
    current_tab = notebook.tab(notebook.select(), "text")
    if today not in links[current_tab]:
        links[current_tab][today] = []
    
    links[current_tab][today].append({"url": url, "title": title})
    save_links(links)
    entry.delete(0, tk.END)
    display_links()
    
    # Seleccionar automáticamente la última URL añadida
    last_item = tree.get_children()[-1]
    tree.selection_set(last_item)
    tree.focus(last_item)

# Eliminar URL seleccionada
def delete_selected():
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showwarning("Advertencia", "Selecciona al menos un enlace para eliminar.")
        return
    
    current_tab = notebook.tab(notebook.select(), "text")
    for item in selected_items:
        values = tree.item(item, "values")
        date, url = values[0], values[1]
        links[current_tab][date] = [link for link in links[current_tab][date] if link["url"] != url]
        if not links[current_tab][date]:
            del links[current_tab][date]
    
    save_links(links)
    display_links()

# Mostrar enlaces en la interfaz
def display_links():
    tree.delete(*tree.get_children())
    current_tab = notebook.tab(notebook.select(), "text")
    if current_tab in links:
        for date, items in links[current_tab].items():
            for link in items:
                tree.insert("", "end", values=(date, link["url"], link["title"]))

# Agregar nueva pestaña
def add_tab():
    new_tab_number = len(notebook.tabs())
    new_tab_name = f"Pestaña {new_tab_number}"
    links[new_tab_name] = {}
    save_links(links)
    frame = ttk.Frame(notebook)
    notebook.add(frame, text=new_tab_name)
    notebook.select(frame)
    display_links()

# Ventana "Acerca de"
class AboutWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Acerca de url-biblioteca-web")
        self.geometry("420x450")
        self.resizable(False, False)

        text = tk.Text(self, wrap=tk.WORD, padx=10, pady=10, relief=tk.FLAT)
        text.pack(expand=True, fill=tk.BOTH)

        text.tag_configure("bold", font=("TkDefaultFont", 10, "bold"))
        text.tag_configure("italic", font=("TkDefaultFont", 10, "italic"))

        text.insert(tk.END, "xsct_gui\n\n", "bold")
        text.insert(tk.END, "Una ")
        text.insert(tk.END, "GUI ", "italic")
        text.insert(tk.END, "url-biblioteca-web es una aplicación en Tkinter.\n\n")
        text.insert(tk.END, "Copyright 2025 \uE020 Washington Indacochea Delgado.\n")
        text.insert(tk.END, "wachin.id@gmail.com\n")
        text.insert(tk.END, "Licencia: GNU GPL3. \n\n")
        text.insert(tk.END, "Te permite almacenar, organizar y abrir enlaces web. Al pegar una URL, se guarda junto con su título, \n")
        text.insert(tk.END, "ícono y la fecha de adición. Los enlaces se agrupan por días para facilitar la navegación.\n\n")
        text.insert(tk.END, "Para más información, visite: \n\n", "italic")
        text.insert(tk.END, "url-biblioteca-web\n")
        text.insert(tk.END, "https://github.com/wachin/url-biblioteca-web\n\n")

        text.config(state=tk.DISABLED)
        close_button = ttk.Button(self, text="Cerrar", command=self.destroy)
        close_button.pack(pady=10)

# Configuración de la GUI
root = tk.Tk()
root.title("Biblioteca de Enlaces")
root.geometry("600x400")

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

frame = ttk.Frame(notebook)
notebook.add(frame, text="Pestaña 1")

frame_top = ttk.Frame(root)
frame_top.pack(pady=10, padx=10, fill="x")

entry = ttk.Entry(frame_top, width=50)
entry.pack(side="left", padx=5)

btn_add = ttk.Button(frame_top, text="Agregar", command=add_link)
btn_add.pack(side="left", padx=5)

btn_delete = ttk.Button(frame_top, text="Eliminar", command=delete_selected)
btn_delete.pack(side="left", padx=5)

btn_about = ttk.Button(frame_top, text="Acerca de", command=lambda: AboutWindow(root))
btn_about.pack(side="left", padx=5)

btn_new_tab = ttk.Button(frame_top, text="+", command=add_tab)
btn_new_tab.pack(side="left", padx=5)

columns = ("Fecha", "URL", "Título")
tree = ttk.Treeview(frame, columns=columns, show="headings")

# Ajustar el tamaño de las columnas
tree.heading("Fecha", text="Fecha")
tree.column("Fecha", width=100, stretch=False)

tree.heading("URL", text="URL")
tree.column("URL", width=200, stretch=True)

tree.heading("Título", text="Título")
tree.column("Título", width=300, stretch=True)

tree.pack(pady=10, padx=10, fill="both", expand=True)
tree.bind("<Double-1>", open_url)

links = load_links()
display_links()

root.mainloop()
