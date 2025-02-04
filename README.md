# Tutorial de Instalación y Uso de "url-biblioteca.py"

## Introducción
"url-biblioteca.py" es una aplicación en Tkinter que permite almacenar, organizar y abrir enlaces web. Al pegar una URL, se guarda junto con su título, ícono y la fecha de adición. Los enlaces se agrupan por días para facilitar la navegación.

---

## Instalación de Dependencias
Antes de ejecutar el programa, asegúrate de tener instalados los siguientes paquetes en Debian 10.

### 1. **Actualizar los repositorios**
Ejecuta el siguiente comando en la terminal:
```bash
sudo apt update
```

### 2. **Instalar los paquetes necesarios**
Ejecuta este comando para instalar todas las dependencias:
```bash
sudo apt install python3-tk python3-bs4 python3-pil.imagetk python3-requests xdg-utils
```

- `python3-tk`: Proporciona soporte para interfaces gráficas con Tkinter.
- `python3-bs4`: Biblioteca BeautifulSoup para extraer el título de la página web.
- `python3-pil.imagetk`: Módulo de imágenes para manejar favicons.
- `python3-requests`: Permite realizar solicitudes HTTP para obtener contenido web.
- `xdg-utils`: Necesario para abrir URLs con el navegador predeterminado.

---

## Uso del Programa

### **1. Ejecutar el script**
Si el archivo `url-biblioteca.py` está en tu carpeta de usuario, navega hasta su ubicación y ejecútalo con:
```bash
python3 url-biblioteca.py
```

### **2. Agregar un enlace**
1. Copia la URL que deseas guardar.
2. Pega la URL en la barra de entrada superior.
3. Haz clic en el botón "Agregar".
4. La URL se guardará con su título y favicon bajo la fecha actual.

### **3. Abrir un enlace guardado**
- Haz clic en el enlace dentro de la interfaz y se abrirá en tu navegador predeterminado.

### **4. Guardado automático**
- Todos los enlaces se almacenan en un archivo `links.json` y se cargarán automáticamente cuando abras la aplicación nuevamente.

---

## Solución de Problemas

### **1. No se abre el navegador correcto**
Si el programa abre Chrome en lugar de Firefox, verifica cuál es tu navegador predeterminado ejecutando:
```bash
xdg-settings get default-web-browser
```
Si el resultado es `chrome.desktop` y quieres cambiarlo a Firefox, usa:
```bash
xdg-settings set default-web-browser firefox.desktop
```

### **2. Error "Módulo no encontrado"**
Si el programa indica que falta un módulo, intenta reinstalarlo. Por ejemplo:
```bash
pip3 install beautifulsoup4 pillow requests
```

---

## Conclusión
Con este tutorial, ahora puedes instalar y utilizar "url-biblioteca.py" en Debian 10 sin problemas. Disfruta organizando tus enlaces de forma sencilla y eficiente.

