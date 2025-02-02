# Importamos las bibliotecas necesarias
import tkinter as tk  # Biblioteca para crear interfaces gráficas
from tkinter import ttk, messagebox  # Widgets adicionales y mensajes emergentes
from googletrans import Translator, LANGUAGES  # Biblioteca para traducción y lista de idiomas
import pyperclip  # Biblioteca para el portapapeles
import pystray  # Biblioteca para crear iconos en la bandeja del sistema
from pystray import MenuItem as item  # Para crear elementos del menú de la bandeja
from PIL import Image, ImageDraw  # Biblioteca para manipulación de imágenes
import win32clipboard  # Biblioteca para interactuar con el portapapeles en Windows
import threading  # Biblioteca para manejar hilos de ejecución

# Crear objeto Translator
translator = Translator()

# Función para traducir texto
def translate_text():
    # Obtener el texto de entrada y el idioma de destino seleccionados
    source_text = text_input.get("1.0", tk.END).strip()
    target_language = lang_selector.get()

    # Mostrar advertencias si no hay texto de entrada o no se selecciona un idioma de destino
    if not source_text:
        messagebox.showwarning("Advertencia", "Por favor, ingresa texto para traducir.")
        return

    if target_language == "Seleccionar idioma":
        messagebox.showwarning("Advertencia", "Por favor, selecciona un idioma de destino.")
        return

    # Mostrar el indicador de progreso
    show_progress()

    try:
        # Obtener el código del idioma de destino y traducir el texto
        lang_code = lang_codes[target_language]
        translated = translator.translate(source_text, dest=lang_code)
        # Mostrar el texto traducido en el área de salida
        text_output.config(state=tk.NORMAL)
        text_output.delete("1.0", tk.END)
        text_output.insert("1.0", translated.text)
        text_output.config(state=tk.DISABLED)
    except Exception as e:
        # Mostrar un mensaje de error si la traducción falla
        messagebox.showerror("Error", f"No se pudo traducir el texto: {e}")
    finally:
        # Ocultar el indicador de progreso
        hide_progress()

# Función para mostrar el indicador de progreso
def show_progress():
    progress_label.grid(row=2, column=0, columnspan=2)
    root.update()

# Función para ocultar el indicador de progreso
def hide_progress():
    progress_label.grid_forget()

# Función para pegar texto desde el portapapeles
def paste_text():
    try:
        text_input.delete("1.0", tk.END)
        text_input.insert(tk.END, pyperclip.paste())
    except pyperclip.PyperclipException:
        messagebox.showerror("Error", "Error al pegar el texto del portapapeles.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo pegar el texto: {e}")

# Función para borrar texto
def clear_text():
    text_input.delete("1.0", tk.END)

# Función para traducir el texto desde el portapapeles
def translate_from_clipboard():
    try:
        # Leer el texto del portapapeles
        win32clipboard.OpenClipboard()
        clipboard_text = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()

        # Traducir el texto del portapapeles
        lang_code = lang_codes[lang_selector.get()]
        translated = translator.translate(clipboard_text, dest=lang_code)

        # Mostrar el texto traducido en una nueva ventana
        result_window = tk.Toplevel(root)
        result_window.title("Texto traducido")
        result_window.geometry("400x300")
        result_window.configure(bg='#f5f5f5')
        result_text = tk.Text(result_window, wrap=tk.WORD, height=10, width=50, font=('Helvetica', 12))
        result_text.insert("1.0", translated.text)
        result_text.pack(padx=10, pady=10)

        # Botones para copiar el texto traducido y abrir la interfaz principal
        tk.Button(result_window, text="Copiar", command=lambda: pyperclip.copy(translated.text), bg='#4CAF50', fg='white', font=('Helvetica', 10, 'bold')).pack(pady=5)
        tk.Button(result_window, text="Abrir interfaz", command=root.deiconify, bg='#2196F3', fg='white', font=('Helvetica', 10, 'bold')).pack(pady=5)
    except win32clipboard.error:
        messagebox.showerror("Error", "No se pudo leer el portapapeles.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo traducir el texto del portapapeles: {e}")

# Función para agregar la opción al menú contextual
def add_to_context_menu():
    def quit_app(icon, item):
        icon.stop()

    def show_app(icon, item):
        root.deiconify()

    # Crear una imagen para el icono de la bandeja del sistema
    image = Image.new('RGB', (64, 64), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 64, 64), fill=(100, 149, 237))

    # Crear el menú de la bandeja del sistema
    menu = (item('Traducir texto seleccionado', translate_from_clipboard),
            item('Mostrar interfaz', show_app),
            item('Salir', quit_app))

    # Inicializar y ejecutar el icono de la bandeja del sistema
    icon = pystray.Icon("Traductor", image, "Traductor", menu)
    icon.run()

# Crear la interfaz principal
root = tk.Tk()
root.title("Traductor")
root.geometry("700x500")
root.configure(bg='#fafafa')  # Color de fondo suave

# Crear un diccionario de códigos de idioma y una lista de idiomas comunes
lang_codes = {v.capitalize(): k for k, v in LANGUAGES.items()}
common_languages = sorted(["Español", "Inglés", "Francés", "Alemán", "Italiano", "Portugués", "Ruso", "Chino", "Japonés", "Árabe"])

# Layout con grid
frame_input = tk.Frame(root, bg='#fafafa', bd=10, relief="solid", borderwidth=1)
frame_input.grid(row=0, column=0, padx=20, pady=20, sticky="nsew", ipadx=10, ipady=10)

# Área de texto de entrada
text_input = tk.Text(frame_input, wrap=tk.WORD, height=15, width=40, font=('Helvetica', 12), bd=2, relief="solid", bg="#fff3e6", insertbackground='gray')
text_input.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

# Botones para pegar y borrar texto
btn_paste = tk.Button(frame_input, text="Pegar", command=paste_text, bg='#FF5722', fg='white', font=('Helvetica', 12, 'bold'), relief="raised", bd=0, padx=20, pady=10)
btn_paste.grid(row=1, column=0, padx=5, pady=5)

btn_clear = tk.Button(frame_input, text="Borrar", command=clear_text, bg='#FF5722', fg='white', font=('Helvetica', 12, 'bold'), relief="raised", bd=0, padx=20, pady=10)
btn_clear.grid(row=1, column=1, padx=5, pady=5)

# Área de texto de salida
frame_output = tk.Frame(root, bg='#fafafa', bd=10, relief="solid", borderwidth=1)
frame_output.grid(row=0, column=1, padx=20, pady=20, sticky="nsew", ipadx=10, ipady=10)

text_output = tk.Text(frame_output, wrap=tk.WORD, height=15, width=40, state=tk.DISABLED, font=('Helvetica', 12), bd=2, relief="solid", bg="#e6f7ff")
text_output.grid(row=0, column=0, padx=5, pady=5)

# Controles adicionales
frame_controls = tk.Frame(root, bg='#fafafa', bd=10)
frame_controls.grid(row=1, column=0, columnspan=2, pady=20)

# Selector de idioma y botón de traducir
lang_selector = ttk.Combobox(frame_controls, values=common_languages, state="readonly", font=('Helvetica', 12), height=10)
lang_selector.set("Seleccionar idioma")
lang_selector.grid(row=0, column=0, padx=5, pady=5)

btn_translate = tk.Button(frame_controls, text="Traducir", command=translate_text, bg='#4CAF50', fg='white', font=('Helvetica', 12, 'bold'), relief="raised", bd=0, padx=20, pady=10)
btn_translate.grid(row=0, column=1, padx=5, pady=5)

# Indicador de progreso
progress_label = tk.Label(frame_controls, text="Traduciendo...", fg="blue", bg='#fafafa', font=('Helvetica', 12, 'italic'))
progress_label.grid(row=2, column=0, columnspan=2)
progress_label.grid_forget()

# Hacer que las filas y columnas se expandan correctamente
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Integrar con el menú contextual en segundo plano
threading.Thread(target=add_to_context_menu, daemon=True).start()

# Ejecutar la interfaz gráfica
if __name__ == "__main__":
    root.mainloop()