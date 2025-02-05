import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
import json
from io import BytesIO
from PIL import Image, ImageTk

# Archivo para almacenar los enlaces
DATA_FILE = "links.json"

def save_links(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_links():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def fetch_page_info(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string if soup.title else url
        
        # Obtener el ícono de la página
        icon_url = url.rstrip("/") + "/favicon.ico"
        icon_response = requests.get(icon_url, headers=headers, timeout=5)
        icon_image = None
        if icon_response.status_code == 200:
            image_data = BytesIO(icon_response.content)
            icon_image = Image.open(image_data)
            icon_image = icon_image.resize((16, 16), Image.ANTIALIAS)
        
        return title, icon_image
    except:
        return url, None

def add_link():
    url = entry.get().strip()
    if not url:
        messagebox.showwarning("Entrada vacía", "Por favor ingrese una URL.")
        return
    
    if not (url.startswith("http://") or url.startswith("https://")):
        url = "https://" + url
    
    title, icon_image = fetch_page_info(url)
    today = datetime.now().strftime("%Y-%m-%d")
    
    if today not in links:
        links[today] = []
    
    links[today].append({"url": url, "title": title})
    save_links(links)
    
    entry.delete(0, tk.END)
    display_links()

def display_links():
    for widget in frame_links.winfo_children():
        widget.destroy()
    
    for date, url_list in sorted(links.items(), reverse=True):
        ttk.Label(frame_links, text=date, font=("Arial", 10, "bold")).pack(anchor="w", pady=2)
        
        for link in url_list:
            frame_item = ttk.Frame(frame_links)
            frame_item.pack(anchor="w", fill="x", pady=1)
            
            btn = ttk.Button(frame_item, text=link["title"], cursor="hand2", command=lambda url=link["url"]: webbrowser.open(url))
            btn.pack(side="left", padx=5)

def on_closing():
    save_links(links)
    root.destroy()

# Cargar datos almacenados
links = load_links()

# Configurar GUI
root = tk.Tk()
root.title("Biblioteca de Enlaces")
root.geometry("500x600")

frame_top = ttk.Frame(root)
frame_top.pack(fill="x", padx=10, pady=5)

entry = ttk.Entry(frame_top, width=50)
entry.pack(side="left", padx=5)

btn_add = ttk.Button(frame_top, text="Agregar", command=add_link)
btn_add.pack(side="right")

canvas = tk.Canvas(root)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
frame_links = ttk.Frame(canvas)

frame_links.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=frame_links, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

display_links()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
