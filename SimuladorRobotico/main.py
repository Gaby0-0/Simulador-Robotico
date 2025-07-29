import tkinter as tk
from tkinter import ttk
from parser import analizar_linea
import ply.lex as lex
import lexer  # tu archivo lexer.py debe tener los tokens
from parser import reiniciar_estado
from codigo_intermedio import CodigoIntermedio




lexer_analizador = lex.lex(module=lexer)

def analisis_lexico(codigo):
    lexer_analizador.input(codigo)
    tokens = []
    while True:
        tok = lexer_analizador.token()
        if not tok:
            break
        tokens.append((tok.type, tok.value))
    return tokens

def analizar():
    reiniciar_estado()

    codigo = text_input.get("1.0", tk.END).strip()
    lineas = codigo.splitlines()

    # Limpiar tablas
    for fila in tabla_resultados.get_children():
        tabla_resultados.delete(fila)
    for fila in tabla_info.get_children():
        tabla_info.delete(fila)
    for fila in tabla_resumen.get_children():
        tabla_resumen.delete(fila)

    errores_sintacticos = False
    errores_semanticos = False
    info_temporal = []

    i = 0
    while i < len(lineas):
        linea = lineas[i].strip()
        numero_linea_actual = i + 1
        i += 1
        if not linea:
            continue

        # Análisis léxico
        tokens_lexico = analisis_lexico(linea)
        for tipo, valor in tokens_lexico:
            tabla_resumen.insert("", "end", values=(numero_linea_actual, tipo, valor))

        # Manejo de bloques repetir
        if ".repetir" in linea and "=" in linea and linea.endswith("{"):
            try:
                partes = linea.split(".")
                id_robot = partes[0].strip()
                _, valor_str = partes[1].split("=")
                repeticiones = int(valor_str.strip().replace("{", "").strip())

                bloque_codigo = []
                lineas_subbloque = []
                llave_cerrada = False
                while i < len(lineas):
                    lin = lineas[i].strip()
                    if lin == "}":
                        llave_cerrada = True
                        break
                    bloque_codigo.append(lin)
                    lineas_subbloque.append(i + 1)  # Guardar número real de línea
                    i += 1
                i += 1  # Para saltar la línea de la llave cerrada

                if not llave_cerrada:
                    errores_sintacticos = True
                    tabla_resultados.insert("", "end", values=(numero_linea_actual, linea, "❌ Inválida", "Falta llave de cierre '}'"), tags=("fila_invalida",))
                    continue

                acciones = []
                bloque_con_error_sintactico = False

                if repeticiones < 0 or repeticiones > 100:
                    errores_semanticos = True
                    tabla_resultados.insert("", "end", values=(
                        numero_linea_actual, linea, "❌ Inválida", "Repeticiones fuera de rango (0 a 100)"
                    ), tags=("fila_invalida",))

                info_temporal.append((id_robot, "repetir", "", str(repeticiones)))
                info_temporal.append(("{", "Apertura de bloque", "", ""))

                j = 0
                while j < len(bloque_codigo):
                    sub_linea = bloque_codigo[j]
                    numero_sublinea = lineas_subbloque[j]
                    resultado = analizar_linea(sub_linea)

                    if not resultado:
                        errores_sintacticos = True
                        bloque_con_error_sintactico = True
                        tabla_resultados.insert("", "end", values=(numero_sublinea, sub_linea, "❌ Inválida", "Sin resultado"), tags=("fila_invalida",))
                        j += 1
                        continue

                    if isinstance(resultado, tuple) and resultado[0] == "❌ Inválida":
                        tabla_resultados.insert("", "end", values=(numero_sublinea, sub_linea, resultado[0], resultado[1]), tags=("fila_invalida",))
                        if resultado[1] == "Sintaxis no reconocida":
                            errores_sintacticos = True
                            bloque_con_error_sintactico = True
                        else:
                            errores_semanticos = True
                            acciones.append((resultado[2], resultado[3], resultado[4], resultado[5]))
                        j += 1
                        continue

                    id_valor, metodo, parametros_list, valor = resultado
                    parametros = ", ".join(str(p) for p in parametros_list) if parametros_list else ""
                    acciones.append((id_valor, metodo, parametros, valor))

                    # Validar velocidad después de movimiento
                    if metodo in ("base", "codo", "garra", "brazo","cerrarGarra","abrirGarra"):
                        if j + 1 >= len(bloque_codigo) or ".velocidad" not in bloque_codigo[j + 1]:
                            errores_semanticos = True
                            tabla_resultados.insert("", "end", values=(numero_sublinea, sub_linea, "❌ Inválida", "Falta instrucción de velocidad después de movimiento"), tags=("fila_invalida",))
                    j += 1

                if not bloque_con_error_sintactico:
                    info_temporal.extend(acciones)
                    info_temporal.append(("}", "Termino de bloque", "", ""))

                continue

            except Exception as e:
                errores_sintacticos = True
                tabla_resultados.insert("", "end", values=(numero_linea_actual, linea, "❌ Inválida", f"Error en repetir: {e}"), tags=("fila_invalida",))
                continue

        # Análisis normal
        resultado = analizar_linea(linea)

        if not resultado:
            errores_sintacticos = True
            tabla_resultados.insert("", "end", values=(numero_linea_actual, linea, "❌ Inválida", "Sin resultado"), tags=("fila_invalida",))
            continue

        if isinstance(resultado, tuple) and resultado[0] == "❌ Inválida":
            tabla_resultados.insert("", "end", values=(numero_linea_actual, linea, resultado[0], resultado[1]), tags=("fila_invalida",))
            if resultado[1] == "Sintaxis no reconocida":
                errores_sintacticos = True
            else:
                errores_semanticos = True
                fila_info = (resultado[2], resultado[3], resultado[4], resultado[5])
                info_temporal.append(fila_info)
            continue

        # Línea válida
        id_valor, metodo, parametros_list, valor = resultado
        parametros = ", ".join(str(x) for x in parametros_list) if parametros_list else ""
        fila_info = (id_valor, metodo, parametros, valor)
        info_temporal.append(fila_info)

        # Verificar velocidad después de movimiento
        if metodo in ("base", "codo", "garra", "brazo", "hombro","cerrarGarra","abrirGarra"):
            siguiente_linea = ""
            k = i
            while k < len(lineas):
                siguiente_linea = lineas[k].strip()
                if siguiente_linea:
                    break
                k += 1
            if ".velocidad" not in siguiente_linea:
                errores_semanticos = True
                tabla_resultados.insert(
                    "", "end",
                    values=(numero_linea_actual, f"{id_valor}.{metodo} = {valor}", "❌ Inválida", "Falta instrucción de velocidad después de movimiento"),
                    tags=("fila_invalida",)
                )

    # Mostrar tabla_info si no hay errores sintácticos
    if not errores_sintacticos:
        for fila in info_temporal:
            tabla_info.insert("", "end", values=fila)

    # Mensaje final
    if not errores_sintacticos and not errores_semanticos:
        tabla_resultados.insert("", "end", values=("", "No se encontraron errores", "", ""), tags=("Sin errores",))
    elif errores_sintacticos:
        tabla_resultados.insert("", "end", values=("", "Errores sintácticos detectados", "", ""), tags=("fila_invalida",))
    else:
        tabla_resultados.insert("", "end", values=("", "Errores semánticos detectados", "", ""), tags=("fila_invalida",))

    if not errores_sintacticos and not errores_semanticos:
        codigo_intermedio_tab.reiniciar_tabla()
        codigo_intermedio_tab.mostrar_datos(info_temporal) 
    else:  
        codigo_intermedio_tab.reiniciar_tabla()


def actualizar_numeros_linea(event=None):
    text_lineas.config(state='normal')
    pos = text_lineas.yview()
    text_lineas.delete("1.0", "end")

    num_lineas = int(text_input.index('end-1c').split('.')[0])
    lineas = "\n".join(str(i) for i in range(1, num_lineas + 1))
    text_lineas.insert("1.0", lineas)
    text_lineas.config(state='disabled')
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
ventana.geometry("1200x700")
ventana.configure(bg="#f0f0f0")

# --- CONTENEDOR PRINCIPAL ---
notebook = ttk.Notebook(ventana)
notebook.pack(fill=tk.BOTH, expand=True)

frame_analizador = tk.Frame(notebook)
notebook.add(frame_analizador, text="Analizador")

# Así el resto del código sigue funcionando igual
frame_principal = frame_analizador


# === COLUMNA IZQUIERDA: Entrada de texto + resultados ===
frame_izquierda = tk.Frame(frame_principal)
frame_izquierda.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 5), pady=10)

tk.Label(frame_izquierda, text="Ingresa tu código:", font=("Segoe UI", 11), bg="#f0f0f0").pack(anchor="w")

frame_texto = tk.Frame(frame_izquierda)
frame_texto.pack(pady=2, fill=tk.BOTH, expand=False)

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

text_input.bind("<KeyRelease>", actualizar_numeros_linea)
text_input.bind("<MouseWheel>", actualizar_numeros_linea)
text_input.bind("<Button-1>", actualizar_numeros_linea)
text_input.bind("<Configure>", actualizar_numeros_linea)

actualizar_numeros_linea()

# Crear un frame horizontal para el botón y las etiquetas
frame_superior = tk.Frame(frame_izquierda)
frame_superior.pack(fill=tk.X, pady=5)

# Botón de análisis
btn_analizar = tk.Button(frame_superior, text="Analizar", command=analizar,
                         font=("Segoe UI", 10), bg="#4CAF50", fg="white", padx=30, pady=5)
btn_analizar.pack(side=tk.LEFT)




frame_tabla = tk.Frame(frame_izquierda)
frame_tabla.pack(fill=tk.BOTH, expand=True)

tabla_resultados = ttk.Treeview(frame_tabla, columns=("Línea", "Contenido", "Estado", "Tipo"),
                                show="headings", height=7)
tabla_resultados.tag_configure("fila_invalida", foreground="red")
tabla_resultados.tag_configure("Sin errores", foreground="green")
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

# === COLUMNA DERECHA: Tabla de información ===
frame_derecha = tk.Frame(frame_principal)
frame_derecha.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 10), pady=5)

tk.Label(frame_derecha, text="Información", font=("Segoe UI", 11, "bold")).pack()

tabla_info = ttk.Treeview(frame_derecha,
                          columns=( "ID", "Método", "Parámetros", "Valor"),
                          show="headings",
                          height=3)

tabla_info.heading("ID", text="ID")
tabla_info.heading("Método", text="Método")
tabla_info.heading("Parámetros", text="Parámetros")
tabla_info.heading("Valor", text="Valor")

tabla_info.column("ID", width=50, anchor="center")
tabla_info.column("Método", width=100)
tabla_info.column("Parámetros", width=150)
tabla_info.column("Valor", width=80)

tabla_info.pack(fill=tk.BOTH, expand=True)

# === NUEVA TABLA EN LA ESQUINA DERECHA INFERIOR ===
tk.Label(frame_derecha, text="Analizador Léxico:", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(10, 0))

frame_resumen = tk.Frame(frame_derecha)
frame_resumen.pack(fill=tk.X)

tabla_resumen = ttk.Treeview(frame_resumen, columns=("Línea", "Descripcion","Token"), show="headings", height=12)
tabla_resumen.heading("Línea", text="Línea")
tabla_resumen.heading("Descripcion", text="Token")
tabla_resumen.heading("Token", text="Valor")

tabla_resumen.column("Línea", width=5)
tabla_resumen.column("Descripcion", width=20)
tabla_resumen.column("Token", width=20)

tabla_resumen.pack(side=tk.LEFT, fill=tk.X, expand=True)

scroll_resumen = ttk.Scrollbar(frame_resumen, orient="vertical", command=tabla_resumen.yview)
tabla_resumen.configure(yscrollcommand=scroll_resumen.set)
scroll_resumen.pack(side=tk.RIGHT, fill=tk.Y)

codigo_intermedio_tab = CodigoIntermedio(notebook)


ventana.mainloop()
