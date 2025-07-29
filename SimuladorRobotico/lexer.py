import ply.lex as lex

tokens = (
    'IDENTIFICADOR',
    'PUNTO',
    'IGUAL',
    'NUMERO',
    'PARENTESIS_A',
    'PARENTESIS_C',
    
)

reservadas = {
    'iniciar': 'INICIAR',
    'detener': 'DETENER',
    'activar': 'ACTIVAR',
    'mover': 'MOVER',
    'agarrarObjeto': 'AGARRAROBJETO',
    'soltarObjeto':'SOLTAROBJETO',
    'bajarCodo':'BAJARCODO',
    'alzarCodo':'ALZARCODO',
    'bajarBrazo':'BAJARBRAZO',
    'AlzarBrazo':'ALZARBRAZO',
    'cerrarGarra': 'CERRAR_GARRA',
    'abrirGarra': 'ABRIR_GARRA',
    'girar': 'GIRAR',
    'repetir': 'REPETIR',
    'finRepetir': 'FIN_REPETIR',
    'Robot': 'ROBOT',
    'velocidad': 'VELOCIDAD',
    'base': 'BASE',
    'cuerpo': 'CUERPO',
    'garra': 'GARRA',
    'codo' : 'CODO',
    'hombro' : 'HOMBRO',
    'brazo' : 'BRAZO'
    
}

tokens += tuple(reservadas.values())

t_PUNTO = r'\.'
t_IGUAL = r'='
t_PARENTESIS_A = r'\('
t_PARENTESIS_C = r'\)'


def t_NUMERO(t):
    r'-?\d+'
    t.value = int(t.value)
    return t


# def t_ROB(t):
#     r'Robot(?!.*[%@#])[A-Za-z0-9]*'
#     return t



def t_IDENTIFICADOR(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    t.type = reservadas.get(t.value, 'IDENTIFICADOR')
    return t





t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    # Devuelve el carácter desconocido como un token "DESCONOCIDO"
    t.type = "DESCONOCIDO"
    t.value = t.value[0]  # Solo el carácter inválido
    t.lexer.skip(1)
    return t

lexer = lex.lex()