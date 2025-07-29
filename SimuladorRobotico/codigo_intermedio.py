# codigo_intermedio.py

import tkinter as tk
from tkinter import ttk
from robot import Robot

#from generador_asm import generar_codigo_componente
import subprocess
class CodigoIntermedio:
    def __init__(self, notebook):
        self.frame = tk.Frame(notebook)
        notebook.add(self.frame, text="Código Intermedio")

        tk.Label(self.frame, text="Tabla de Código Intermedio", font=("Segoe UI", 11, "bold")).pack(pady=5)

        self.tabla = ttk.Treeview(self.frame, columns=("ID", "Acción", "Parámetros", "Resultado"), show="headings")
        self.tabla.heading("ID", text="Operador")
        self.tabla.heading("Acción", text="Operando 1")
        self.tabla.heading("Parámetros", text="Operando 2")
        self.tabla.heading("Resultado", text="Resultado")

        self.tabla.column("ID", width=60)
        self.tabla.column("Acción", width=120)
        self.tabla.column("Parámetros", width=180)
        self.tabla.column("Resultado", width=120)

        self.tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def mostrar_datos(self, datos):
        componente_actual = "" 
        restas  = [0,0,0]
        codigo_ex=[]
        cont_rep_componentes = [0,0,0,0]
        bucle_instrucciones_robot = []
        
        robot = Robot()
        bucle = False
        numero_ciclos = 0

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        i = 1  # empieza desde 1 para que el primero sea temp1
        j = 1
        elementos_asm = []
        elementos_robot = []
       
        for d in datos:

            if d[1] == "Declaración":
                self.tabla.insert("", "end", values=(d[1], d[3], "-",d[0] ))
        
            if d[1] in {"garra", "brazo", "base","codo", "cerrarGarra","abrirGarra"}:
                self.tabla.insert("", "end", values=("asignar componente", d[0], d[1], f"temp{i}"))
                self.tabla.insert("", "end", values=("=", f"temp{i}",d[3], f"{d[0]}_{d[1]}"))
                componente_actual = d[1]
                if d[1] == "garra":
                    cont_rep_componentes [0] += 1
                    elementos_asm.append(d[1])
                    elementos_asm.append(d[3])

                if d[1] == "brazo":
                    cont_rep_componentes [1] += 1
                    elementos_asm.append(d[1])
                    elementos_asm.append(d[3])
               
                if d[1] == "base":
                    cont_rep_componentes [2] += 1
                    elementos_asm.append(d[1])
                    elementos_asm.append(d[3])

                if d[1] == "codo":
                    cont_rep_componentes [3] += 1
                    elementos_robot.append(d[1])
                    elementos_robot.append(d[3])
                    
                
                print(d[1])
                
                i += 1 

            if d[1] == "velocidad":  
                self.tabla.insert("", "end", values=("asignar velocidad", d[0], d[1], f"temp{i}"))
                self.tabla.insert("", "end", values=("=", f"temp{i}",d[3], f"{d[0]}_{d[1]}"))

                
                if cont_rep_componentes [0] == 2 and componente_actual == "garra":
                    aux = restas[0]-elementos_asm[1] 
                    print(aux)
                    codigo_ex.append(generar_puerto_izquierda(elementos_asm[0], aux,  d[3]))
                    cont_rep_componentes[0] = 0
                    restas[0] = elementos_asm[1]
                     #codigo necesario para mover la garra del robot
                    if not bucle :
                        robot.mueveGarra(elementos_asm[1],d[3])  
                    else:
                        bucle_instrucciones_robot.append(f"{elementos_asm[0]},{elementos_asm[1] },{d[3]}")                 
                elif componente_actual == "garra":
                    print(elementos_asm[1], restas[0])
                    aux = elementos_asm[1] - restas[0]
                    print(aux)
                    codigo_ex.append(generar_puerto_derecha(elementos_asm[0], aux, d[3]))
                    restas[0] = elementos_asm[1]
                    #codigo necesario para mover la garra del robot
                    if not bucle :
                        robot.mueveGarra(elementos_asm[1],d[3])  
                    else:
                        bucle_instrucciones_robot.append(f"{elementos_asm[0]},{elementos_asm[1] },{d[3]}")   

                if cont_rep_componentes [1] == 2 and componente_actual == "brazo":
                    aux = restas [1]-elementos_asm[1] 
                    print(aux)
                    codigo_ex.append(generar_puerto_izquierda(elementos_asm[0], aux,  d[3]) )
                    cont_rep_componentes[1] = 0
                    restas[1] = elementos_asm[1]
                    #codigo necesario para mover el brazo de retorno del robot
                    if not bucle :
                        robot.mueveBrazo(elementos_asm[1],d[3])  
                    else:
                        bucle_instrucciones_robot.append(f"{elementos_asm[0]},{elementos_asm[1] },{d[3]}")  
                elif  componente_actual == "brazo" :
                    aux = int(elementos_asm[1]) - int(restas[1])
                    codigo_ex.append(generar_puerto_derecha(elementos_asm[0], aux, d[3]))
                    restas[1] =elementos_asm[1]
                    #codigo necesario para mover el brazo  del robot
                    if not bucle :
                        robot.mueveBrazo(elementos_asm[1],d[3])  
                    else:
                        bucle_instrucciones_robot.append(f"{elementos_asm[0]},{elementos_asm[1] },{d[3]}")  
                    
                if cont_rep_componentes [2] == 2 and componente_actual == "base":
                    aux = restas [2]-elementos_asm[1]
                    print(aux)
                    codigo_ex.append(generar_puerto_izquierda(elementos_asm[0],aux, d[3]))
                    cont_rep_componentes[2] = 0
                    restas [2]  = elementos_asm[1]
                    #codigo necesario para mover el brazo  del robot
                    if not bucle :
                        robot.mueveBase(elementos_asm[1],d[3])  
                    else:
                        bucle_instrucciones_robot.append(f"{elementos_asm[0]},{elementos_asm[1] },{d[3]}")  
                elif componente_actual == "base":
                    aux = int(elementos_asm[1]) - int(restas[2])
                    codigo_ex.append(generar_puerto_derecha(elementos_asm[0], aux, d[3]))
                    restas[2] = elementos_asm[1]
                    #codigo necesario para mover el brazo  del robot
                    if not bucle :
                        robot.mueveBase(elementos_asm[1],d[3])  
                    else:
                        bucle_instrucciones_robot.append(f"{elementos_asm[0]},{elementos_asm[1] },{d[3]}")  

                if cont_rep_componentes [3] == 2 and componente_actual == "codo":
                    
                    if not bucle :
                        robot.mueveCodo(elementos_robot[1],d[3])  
                    else:
                        bucle_instrucciones_robot.append(f"{elementos_robot[0]},{elementos_robot[1]},{d[3]}") 
                    cont_rep_componentes[3] = 0
                elif componente_actual == "codo":
                    if not bucle :
                        robot.mueveCodo(elementos_robot[1],d[3])  
                    else:
                        bucle_instrucciones_robot.append(f"{elementos_robot[0]},{elementos_robot[1]},{d[3]}")
 
                

                elementos_robot.clear()
                elementos_asm.clear()
                i += 1 

            if d[1] == "repetir":  
                self.tabla.insert("", "end", values=("repeticion", d[0], d[1], f"{d[0]}_{d[1]}"))
                self.tabla.insert("", "end", values=("asignar", d[3],"-", f"cont{j}"))  
                self.tabla.insert("", "end", values=("<", f"cont{j}","0", f"ejecutar"))
                codigo_ex.append(f"{d[1]},{d[3]}") 
                numero_ciclos = d[3]
                j +=1
                bucle = True


            if d[0] == "}":
                print(d[0])
                codigo_ex.append(f"{d[0]}") 
                bucle = False
                robot.ejecutar_ciclo(bucle_instrucciones_robot, numero_ciclos)

        generar_codigo_completo(codigo_ex) 
        

    def reiniciar_tabla(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

#genera los valores para mover los numeros a la derecha
def generar_puerto_derecha(nombre, angulos, velocidad):
    nombre = nombre.lower()
    #sirve para modificar los angulos que necesitan ser restados en cada vuelta
    angulosMod =angulos
    
    if nombre == "garra":
        puerto = "PORTA"
        angulosMod = angulos +1
    elif nombre == "brazo":
        puerto = "PORTB"
        angulosMod = angulos +1
    elif nombre == "base":
        puerto = "PORTC"
        angulosMod = angulos +1
    else:
        return f"; Componente '{nombre}' no reconocido"

    codigo = []
    codigo.append(f";--------código a la derecha de: {puerto}: {nombre}")
    codigo.append(f"MOV DX, {puerto}")
    codigo.append(f"MOV CX,{angulosMod}")
    codigo.append("MOV BL, 0  ; Dirección: 0=derecha, 1=izquierda")
    codigo.append(f"MOV retardo,{ obtener_retardo(velocidad)}")
    codigo.append("CALL MOVER_MOTOR")

    

    return "\n".join(codigo)



def generar_puerto_izquierda(nombre, angulos, velocidad):
    nombre = nombre.lower()
 

    angulosMod =angulos 
    if nombre == "garra":
        if angulos>1:
            angulosMod = angulos -1
        puerto = "PORTA"
    elif nombre == "brazo":
        angulosMod = angulos + 1
        puerto = "PORTB"
    elif nombre == "base":
        puerto = "PORTC"
        angulosMod = angulos + 1
    else:
        return f"; Componente '{nombre}' no reconocido"

    codigo = []
    codigo.append(f";--------código a la izquierda de: {puerto}: {nombre}")
    codigo.append(f"MOV DX, {puerto}")
    codigo.append(f"MOV CX,{angulosMod}")
    codigo.append("MOV BL, 1  ; Dirección:  1=izquierda")
    codigo.append(f"MOV retardo,{ obtener_retardo(velocidad)}")
    codigo.append("CALL MOVER_MOTOR")

    return "\n".join(codigo)


def obtener_retardo(velocidad):
    
    retardo = [
        "2000h", "2400h", "2800h", "2C00h", "3000h", "3400h", "3800h", "3C00h", "4000h", "4400h",
        "4800h", "4C00h", "5000h", "5400h", "5800h", "5C00h", "6000h", "6400h", "6800h", "6C00h",
        "7000h", "7400h", "7800h", "7C00h", "8000h", "8400h", "8800h", "8C00h", "9000h", "9400h",
        "9800h", "9C00h", "A000h", "A400h", "A800h", "AC00h", "B000h", "B400h", "B800h", "BC00h",
        "C000h", "C400h", "C800h", "CC00h", "D000h", "D400h", "D800h", "DC00h", "E000h", "E400h",
        "E800h", "EC00h", "F000h", "F400h", "F800h", "FC00h", "FD00h", "FE00h", "FF00h", "0FFFFh"
    ]

    if 1 <= velocidad <= 60:
        return retardo[velocidad-1]
    else:
        return "Fuera de rango"
    

    

def generar_codigo_completo(codigo_extra):
    codigo = []

    codigo.append(".model tiny")
    codigo.append(".code")
    codigo.append("ORG 100h")
    codigo.append("PORTA   EQU 00h")
    codigo.append("PORTB   EQU 02h")
    codigo.append("PORTC   EQU 04h")
    codigo.append("CONFIG  EQU 06h")
    codigo.append("")
    codigo.append("")
    
    codigo.append("")
    codigo.append("retardo DW 0000h")
    codigo.append("; Tabla de secuencias para motores paso a paso")
    codigo.append("TABLA_PASOS DB 00001001b, 00001100b, 00000110b, 00000011b")
    codigo.append("")
    codigo.append("START:")

    codigo.append("    ; Inicializar 8255")
    codigo.append("    MOV DX, CONFIG")
    codigo.append("    MOV AL, 10000000b      ; Todos los puertos en salida, modo 0")
    codigo.append("    OUT DX, AL")


 
    # Agregar líneas pares (índices 0, 2, 4...) en orden normal
    cont_repetir = 0
    for i in range(len(codigo_extra)):
        if codigo_extra[i].startswith("repetir"):
            cont_repetir += 1
            lista = codigo_extra[i].split(",")
            codigo.append(";-------- Comienza logica para la funcion repetir------")
            codigo.append(f"mov CX, {lista[1]}")
            codigo.append(f"BUCLE_REPETIR{cont_repetir}:")
            codigo.append(f"push CX")
        elif codigo_extra[i] == "}":
            codigo.append(f"pop CX")
            codigo.append(f"loop BUCLE_REPETIR{cont_repetir}")
            codigo.append(f";-------- termina logica para el bucle repetir-------")
        else:    
            codigo.append(codigo_extra[i])

    

    
    
    codigo.append("MOV AL, 0")
    codigo.append("MOV DX, PORTA")
    codigo.append("OUT DX, AL")
    codigo.append("MOV DX, PORTB")
    codigo.append("OUT DX, AL")
    codigo.append("MOV DX, PORTC")
    codigo.append("OUT DX, AL")
    codigo.append("")
    codigo.append("HLT")
    codigo.append("; Terminar el programa correctamente")
    codigo.append("MOV AX, 4C00h          ; Función DOS para terminar programa")
    codigo.append("INT 21h")
    

    codigo.append("")
    
    

    
    
    codigo.append("; -------- SUBRUTINA PARA MOVER MOTOR --------")
    codigo.append("; Entrada: DX = Puerto del motor, CX = Número de pasos, BL = Dirección (0=der, 1=izq)")
    codigo.append("; Modifica: AL, BH (índice de secuencia)")
    codigo.append("MOVER_MOTOR:")
    codigo.append("    PUSH BX")
    codigo.append("    PUSH CX")
    codigo.append("    PUSH SI")
    codigo.append("")
    codigo.append("    MOV BH, 0              ; Índice de secuencia (0-3)")
    codigo.append("")
    codigo.append("BUCLE_MOTOR:")
    codigo.append("    ; Obtener el paso de la tabla")
    codigo.append("    MOV SI, OFFSET TABLA_PASOS")
    codigo.append("    MOV AL, BH")
    codigo.append("    MOV AH, 0")
    codigo.append("    ADD SI, AX")
    codigo.append("    MOV AL, [SI]")
    codigo.append("")
    codigo.append("    ; Enviar paso al puerto")
    codigo.append("    OUT DX, AL")
    codigo.append("    CALL DELAY")
    codigo.append("")
    codigo.append("    ; Calcular siguiente índice según dirección")
    codigo.append("    CMP BL, 0              ; ¿Dirección derecha?")
    codigo.append("    JE INCREMENTAR_INDICE")
    codigo.append("")
    codigo.append("    ; Dirección izquierda: decrementar índice")
    codigo.append("    DEC BH")
    codigo.append("    AND BH, 03h            ; Mantener BH entre 0-3")
    codigo.append("    JMP CONTINUAR_BUCLE")
    codigo.append("")
    codigo.append("INCREMENTAR_INDICE:")
    codigo.append("    ; Dirección derecha: incrementar índice")
    codigo.append("    INC BH")
    codigo.append("    AND BH, 03h            ; Mantener BH entre 0-3")
    codigo.append("")
    codigo.append("CONTINUAR_BUCLE:")
    codigo.append("    LOOP BUCLE_MOTOR")
    codigo.append("")
    codigo.append("    POP SI")
    codigo.append("    POP CX")
    codigo.append("    POP BX")
    codigo.append("    RET")
    codigo.append("")
    

    codigo.append("")
    codigo.append("; -------- RETARDO --------")
    codigo.append("DELAY:")
    codigo.append("    PUSH CX")
    codigo.append("    MOV CX, [retardo]")
    codigo.append("D_LOOP:")
    codigo.append("    LOOP D_LOOP")
    codigo.append("    POP CX")
    codigo.append("    RET")

    codigo.append(".code ends")
    codigo.append(" end START")
    
   

    contenido = "\n".join(codigo)

    # Ruta donde deseas guardar el archivo
    ruta_archivo = "C:/DOSBox2/Tasm/PROG/programa.asm"  

    # Guardar en el archivo
    with open(ruta_archivo, "w") as archivo:
        archivo.write(contenido)

    ruta_batch = "C:/DOSBox2/Tasm/PROG/compilar.bat"

    with open(ruta_batch, "w") as f:
            f.write("""@echo off
BIN\TASM programa.asm
BIN\TLINK programa.obj
programa
pause
""")

    comando_dosbox = [
        r"C:\DOSBox2\dosbox.exe",
        "-c", "mount c C:\\DOSBox2\\Tasm",
        "-c", "c:",
        "-c", "cd PROG",
        "-c", "compilar.bat",
        "-c", "exit"
    ]

    #subprocess.run(comando_dosbox)


    print(f"Archivo guardado en: {ruta_archivo}")



