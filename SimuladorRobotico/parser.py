import ply.yacc as yacc
from lexer import tokens
# Almacenamiento de robots declarados
robots_declarados = set()
resultados = []

rangos = {
    'codo': (-75, 75),
    'base': (-180, 180),
    'garra': (-45, 45),
    'brazo': (-90, 90),
    'velocidad' : (0,60),
    'repetir' : (0,100),
}

def p_declaracion_robot(p):
    '''linea : ROBOT IDENTIFICADOR
             | ROBOT NUMERO IDENTIFICADOR'''
    nombre_robot = p[2] if len(p) == 3 else p[3]

    # Agrega el error si ya está declarado
    if nombre_robot in robots_declarados:
        resultados.append(("❌ Inválida", f"Robot '{nombre_robot}' ya ha sido declarado.", nombre_robot, 'Declaración', [], 'Robot'))

    #Lo devuelve como resultado para la tabla_info, incluso si hay error o no.
    p[0] = (nombre_robot, 'Declaración', [], 'Robot')

    # Solo añade si no estaba antes
    if nombre_robot not in robots_declarados:
        robots_declarados.add(nombre_robot)


def reiniciar_estado():
    global robots_declarados, resultados
    robots_declarados = set()
    resultados = []


def p_accion_sin_parametro(p):
    '''linea : IDENTIFICADOR PUNTO INICIAR PARENTESIS_A PARENTESIS_C
             | IDENTIFICADOR PUNTO DETENER PARENTESIS_A PARENTESIS_C
             | IDENTIFICADOR PUNTO ACTIVAR PARENTESIS_A PARENTESIS_C
             | IDENTIFICADOR PUNTO MOVER PARENTESIS_A PARENTESIS_C
             | IDENTIFICADOR PUNTO CERRAR_GARRA PARENTESIS_A PARENTESIS_C
             | IDENTIFICADOR PUNTO ABRIR_GARRA PARENTESIS_A PARENTESIS_C
             | IDENTIFICADOR PUNTO FIN_REPETIR PARENTESIS_A PARENTESIS_C
             | IDENTIFICADOR PUNTO AGARRAROBJETO PARENTESIS_A PARENTESIS_C
             | IDENTIFICADOR PUNTO SOLTAROBJETO PARENTESIS_A PARENTESIS_C
             | IDENTIFICADOR PUNTO ALZARCODO PARENTESIS_A PARENTESIS_C
             | IDENTIFICADOR PUNTO BAJARCODO PARENTESIS_A PARENTESIS_C
             | IDENTIFICADOR PUNTO ALZARBRAZO PARENTESIS_A PARENTESIS_C
             | IDENTIFICADOR PUNTO BAJARBRAZO PARENTESIS_A PARENTESIS_C
             | IDENTIFICADOR PUNTO GIRAR PARENTESIS_A PARENTESIS_C
             '''
             
    
    if p[1] not in robots_declarados:
        resultados.append(("❌ Inválida", f"Robot '{p[1]}' no ha sido declarado."))
    else:
        p[0] = (p[1], p[3], [], None)

def p_accion_con_parametro(p):
    '''linea : IDENTIFICADOR PUNTO VELOCIDAD IGUAL NUMERO
             | IDENTIFICADOR PUNTO BASE IGUAL NUMERO
             | IDENTIFICADOR PUNTO CUERPO IGUAL NUMERO
             | IDENTIFICADOR PUNTO GARRA IGUAL NUMERO
             | IDENTIFICADOR PUNTO CODO IGUAL NUMERO
             | IDENTIFICADOR PUNTO HOMBRO IGUAL NUMERO
             | IDENTIFICADOR PUNTO BRAZO IGUAL NUMERO
             | IDENTIFICADOR PUNTO REPETIR IGUAL NUMERO
               | IDENTIFICADOR PUNTO REPETIR PARENTESIS_A NUMERO PARENTESIS_C'''
    
    identificador = p[1]
    accion = p[3].lower()
    valor = p[5]

    if identificador not in robots_declarados:
        resultados.append(("❌ Inválida", f"Robot '{identificador}' no ha sido declarado.", identificador, accion, [1], valor))
        return
    
    if accion in rangos:
        min_valor, max_valor = rangos[accion]
        if not (min_valor <= valor <= max_valor):
            resultados.append(("❌ Inválida", f"Valor fuera de rango para '{accion}': {valor}. Debe estar entre {min_valor} y {max_valor}.", identificador, accion, [1], valor))
            return

    p[0] = (identificador, accion, [1], valor)

def p_error(p):
    resultados.append(("❌ Inválida", "Sintaxis no reconocida"))

parser = yacc.yacc()

def analizar_linea(linea):
    global resultados
    resultados = []
    resultado = parser.parse(linea)
    if resultados:
        return resultados[0]  # Devuelve el primer error si lo hay
    return resultado
