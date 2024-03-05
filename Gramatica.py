import re

class TablaPredectiva:
    def __init__(self):
        self.stack = []
        self.table = {
            ('E', 'DELETE'): ['DELETE', 'D1'],
            ('D1', 'FROM'): ['FROM', 'I', 'O'],
            ('I', 'LETTER'): ['L', 'R'],
            ('R', 'LETTER'): ['L', 'R'],
            ('R', 'WHERE'):['epsilon'],
            ('R', '"'):['epsilon'],
            ('R', '$'):['epsilon'],
            ('R', 'EQUALS'):['epsilon'],
            ('L', 'LETTER'): ['LETTER'],
            ('O', 'WHERE'): ['WHERE', 'C'],
            ('O', 'MAN'): ['epsilon'],  
            ('C', 'LETTER'): ['I', 'EQUALS', 'V'],
            ('V', 'NUM'): ['D', 'RE'],
            ('V', 'COM'): ['COM', 'I', "COM"],
            ('RE', 'NUM'): ['D', 'RE'],
            ('RE', '$'): ['epsilon'],
            ('D', 'NUM'): ['NUM']
        }
        
    def parse(self, tokens):
        self.tokens = tokens
        self.stack = ['$', 'E']
        self.cursor = 0
        output = []
        
        while self.stack:
            print(f"Pila: {self.stack}")
            output.append(f"Pila: {self.stack}")
            top = self.stack[-1]
            current_token = self.tokens[self.cursor][0] if self.cursor < len(self.tokens) else '$'
            
       
            
            if top == current_token:
                self.stack.pop()
                self.cursor += 1
            elif (top, current_token) in self.table:
                self.stack.pop()
                symbols = self.table[(top, current_token)]
                if symbols != ['epsilon']:
                    for symbol in reversed(symbols):
                        self.stack.append(symbol)
            else:
                print(f"La entrada De la tabla no se encontro: {top}, {current_token}")
                raise Exception("Hubo un error en la sintaxis")
        
        if self.cursor != len(self.tokens):
            print("El Analasis Paso Con Exito")
            output.append("El Analisis se completo exitosamente")
        else:
            raise Exception("Error La Entrada No es Valida")
        
        return "\n".join(output)

def lexer(input_string):
    tokens = []
    token_specs = [
        ('DELETE', r'\bdelete\b'),
        ('FROM', r'\bfrom\b'),
        ('WHERE', r'\bwhere\b'),
        ('LETTER', r'[a-z]'),
        ('STRING', r'[a-zA-Z]+'),
        ('NUM', r'\d[0-9]+'),
        ('EQUALS', r'\='),
        ('COM', r'\"'),
        ('MAN', r'\$'),
        ('IGNORE', r'[ \t\n]+'),
        ('MISMATCH', r'.'),
    ]
    token_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specs)
    for match in re.finditer(token_regex, input_string):
        type = match.lastgroup
        if type == 'IGNORE':
            continue
        elif type == 'MISMATCH':
            raise RuntimeError(f'El Caracter No es Valido: {match.group(0)}')
        else:
            tokens.append((type, match.group(0)))
    return tokens

def analizar_entrada(input_string):
    try:
        tokens = lexer(input_string)
        parser = TablaPredectiva()
        estado_pila = parser.parse(tokens)  
        return f"Análisis completado con éxito.\n pila: {estado_pila}"
    except Exception as e:
        return str(e)