# Traductor de Texto

Esta es una aplicación de traducción de texto basada en la biblioteca `tkinter` de Python para crear una interfaz gráfica. Utiliza el servicio de traducción de Google para traducir texto a varios idiomas. Además, integra funcionalidades para trabajar con el portapapeles y la bandeja del sistema.

## Requisitos

Para ejecutar esta aplicación, necesitas tener instaladas las siguientes bibliotecas de Python:

- `tkinter`
- `googletrans`
- `pyperclip`
- `pystray`
- `Pillow`
- `pywin32`

Puedes instalarlas usando pip:

```sh
pip install googletrans==4.0.0-rc1 pyperclip pystray Pillow pywin32 tkinter
```

Interfaz de Usuario
La interfaz principal de la aplicación incluye las siguientes funcionalidades:

Área de texto de entrada: Donde puedes escribir o pegar el texto que deseas traducir.
Botón "Pegar": Pega el texto desde el portapapeles en el área de entrada.
Botón "Borrar": Borra el texto del área de entrada.
Selector de idioma: Permite seleccionar el idioma al que deseas traducir el texto.
Botón "Traducir": Traduce el texto del área de entrada al idioma seleccionado.
Área de texto de salida: Muestra el texto traducido.
Bandeja del Sistema
La aplicación también se integra con la bandeja del sistema, proporcionando las siguientes opciones:

Traducir texto seleccionado: Traduce el texto actualmente en el portapapeles.
Mostrar interfaz: Muestra la interfaz principal de la aplicación.
Salir: Cierra la aplicación.