import tkinter as tk
from tkinter import ttk, messagebox
import re

# Analizador sintáctico de múltiples líneas
def analizar_sintactico_lineas(texto):
    lineas = texto.strip().splitlines()
    resultados = []

    for i, linea in enumerate(lineas, start=1):
        linea = linea.strip()
        if not linea:
            continue

        if re.match(r'^Robot\s\w+$', linea):

            #resultados.append((i, linea, "✅ Válida", "Declaración de robot"))
            pass
        # elif re.match(r'^Robot', linea):
        #     #resultados.append((i, linea, "✅ Válida", "Declaración de robot"))
        #     pass
        elif re.match(r'^\w+\.(iniciar|detener|activar|mover)\(\)$', linea):
            #resultados.append((i, linea, "✅ Válida", "Acción sin parámetro"))
            pass
        elif re.match(r'^\w+\.(cerrarGarra|abrirGarra)\(\)$', linea):
            #resultados.append((i, linea, "✅ Válida", "Acción sin parámetro"))
            pass
        elif re.match(r'^\w+\.(repetir|finRepetir)\(\)$', linea):
            #resultados.append((i, linea, "✅ Válida", "Acción sin parámetro"))
            pass
        elif re.match(r'^\w+\.(velocidad|base|cuerpo|garra)=\d+$', linea):
            #resultados.append((i, linea, "✅ Válida", "Acción con parámetro"))
            pass
        else:
            resultados.append((i, linea, "❌ Inválida", "Sintaxis no reconocida"))

    return resultados

# Acción al presionar el botón
def analizar():
    codigo = text_input.get("1.0", tk.END)
    resultados = analizar_sintactico_lineas(codigo)

    # Limpiar tabla anterior
    for fila in tabla_resultados.get_children():
        tabla_resultados.delete(fila)

    # Insertar nuevos resultados
    for linea_num, contenido, estado, tipo in resultados:
        tabla_resultados.insert("", "end", values=(linea_num, contenido, estado, tipo))


def actualizar_numeros_linea(event=None):
    text_lineas.config(state='normal')
    # Guardar la posición actual del scroll para no "regresar"
    pos = text_lineas.yview()

    text_lineas.delete("1.0", "end")

    num_lineas = int(text_input.index('end-1c').split('.')[0])
    lineas = "\n".join(str(i) for i in range(1, num_lineas + 1))
    text_lineas.insert("1.0", lineas)
    text_lineas.config(state='disabled')

    # Restaurar la posición del scroll
    text_lineas.yview_moveto(pos[0])


def on_scroll(*args):
    if args[0] == "moveto":
        fraction = float(args[1])
        text_input.yview_moveto(fraction)
        text_lineas.yview_moveto(fraction)
    elif args[0] == "scroll":
        text_input.yview_scroll(int(args[1]), args[2])
        text_lineas.yview_scroll(int(args[1]), args[2])


def on_textscroll(first, last):
    scrollbar.set(first, last)
    text_lineas.yview_moveto(float(first))


# GUI
ventana = tk.Tk()
ventana.title("Analizador Sintáctico con PLY")
ventana.geometry("800x800")
ventana.configure(bg="#f0f0f0")

tk.Label(ventana, text="Ingresa tu código:", font=("Segoe UI", 11), bg="#f0f0f0").pack(pady=(10, 0))

frame_texto = tk.Frame(ventana)
frame_texto.pack(padx=20, pady=2, fill=tk.BOTH, expand=False)

text_lineas = tk.Text(frame_texto, width=4, padx=5, font=("Consolas", 11),
                      spacing1=0, spacing3=0, takefocus=0, border=0,
                      bg='lightgray', state='disabled', wrap='none')
text_lineas.pack(side=tk.LEFT, fill=tk.Y)

text_input = tk.Text(frame_texto, height=5, font=("Consolas", 11), wrap='none')
text_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(frame_texto, orient='vertical', command=on_scroll)
scrollbar.pack(side=tk.RIGHT, fill='y')

text_input.config(yscrollcommand=on_textscroll)
text_lineas.config(yscrollcommand=scrollbar.set)

# Actualizar numeración de línea cuando cambia el texto o se mueve el cursor
text_input.bind("<KeyRelease>", actualizar_numeros_linea)
text_input.bind("<MouseWheel>", actualizar_numeros_linea)
text_input.bind("<Button-1>", actualizar_numeros_linea)
text_input.bind("<Configure>", actualizar_numeros_linea)

actualizar_numeros_linea()

btn_analizar = tk.Button(ventana, text="Analizar", command=analizar,
                        font=("Segoe UI", 10), bg="#4CAF50", fg="white", padx=10, pady=5)
btn_analizar.pack(pady=5)

frame_tabla = tk.Frame(ventana)
frame_tabla.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

tabla_resultados = ttk.Treeview(frame_tabla, columns=("Línea", "Contenido", "Estado", "Tipo"),
                                show="headings", height=10)
tabla_resultados.heading("Línea", text="Línea")
tabla_resultados.heading("Contenido", text="Código")
tabla_resultados.heading("Estado", text="Estado")
tabla_resultados.heading("Tipo", text="Tipo")

tabla_resultados.column("Línea", width=60, anchor="center")
tabla_resultados.column("Contenido", width=300)
tabla_resultados.column("Estado", width=100, anchor="center")
tabla_resultados.column("Tipo", width=200)

scrollbar_result = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla_resultados.yview)
tabla_resultados.configure(yscroll=scrollbar_result.set)
scrollbar_result.pack(side="right", fill="y")
tabla_resultados.pack(fill=tk.BOTH, expand=True)

ventana.mainloop()