import sys
from dataclasses import dataclass
from lexer.symbol_table import SymbolTable


@dataclass
class Token:
    """Representa um token valido identificado pelo scanner."""
    type: str
    value: str
    line: int
    column: int

    def __repr__(self):
        return f"<{self.type}, '{self.value}'>"


class LexicalError(Exception):
    """Classe de Exceção que representa um erro Léxico."""
    pass


class Scanner:
    # Conjunto das palavras reservadas da gramática, pontuação e operadores
    KEYWORDS = {'def', 'int', 'float', 'string', 'print', 'read', 'return',
                'if', 'else', 'for', 'new', 'break', 'null'}
    SINGLE_CHAR_TOKENS = {'+', '-', '*', '/', '%', '=', '<', '>', '(', ')', '{',
                          '}', '[', ']', ';', ','}
    REL_OPS = {'=', '!', '<', '>'}

    def __init__(self, source_code: str, symbol_table: SymbolTable):
        self.text = source_code
        self.symbol_table = symbol_table
        self.pos = 0
        self.line = 1
        self.col = 1
        self.current_char = self.text[0] if self.text else None

    def advance(self):
        """Avança para o próximo caractere, atualizando a posição."""
        if self.current_char == '\n':
            self.line += 1
            self.col = 0

        self.pos += 1
        self.col += 1
        self.current_char = self.text[self.pos] if self.pos < len(
            self.text) else None

    def peek(self) -> str | None:
        """
        'Espia' o caractere a frente sem consumi-lo.
        Útil para os tokens de operadores de comparação.
        """
        peek_pos = self.pos + 1
        return self.text[peek_pos] if peek_pos < len(self.text) else None

    def skip_whitespace(self):
        """Consome caracteres de espaço em branco, tabulações e nova linha."""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def scan_identifier_or_keyword(self) -> Token:
        """
        Diagrama de transição para idents e palavras reservadas:
        Aceita caracteres alfanumericos ou '_'.
        - q0: 'Aa..Zz' -> q1
        - q1: 'Aa..Zz'|0..9|'_' -> q1; 
              'outro' -> q2
        - q2: ACEITA token
        """
        start_col = self.col    # Guarda a coluna inicial do token
        result = ''

        # Concatena caracteres ao token enquanto é alfanumérico ou _
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()

        # Verifica se o token gerado é uma palavra reservada
        if result in self.KEYWORDS:
            return Token(result, result, self.line, start_col)

        # Se não for palavra reservada, é um 'ident'.
        # Adiciona à tabela de símbolos.
        self.symbol_table.add_occurrence(result, self.line, start_col)
        return Token('ident', result, self.line, start_col)

    def scan_number(self) -> Token:
        """
        Diagrama de transição para constantes numéricas (int_constant e float_constant).
        q0: 0..9 -> q1 (int)
        q1: 0..9 -> q1
            '.' -> q2
            'outro' -> ACEITA int
        q2: 0..9 -> q3 (float). 
            'outro' -> ACEITA float.
        q3: 0..9 -> q3
            'outro'-> ACEITA float
        """
        start_col = self.col    # Guarda a coluna inicial do token
        is_float = False        # Flag para determinar se número é int ou float
        result = ''

        # Concatena caracteres ao token enquanto é dígito
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        # Verifica se próximo caractere após os dígitos é '.'
        if self.current_char == '.':
            is_float = True             # Transforma em float
            result += self.current_char
            self.advance()

            # Continua lendo dígitos
            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()

        # Determina tipo do token
        token_type = 'float_constant' if is_float else 'int_constant'
        return Token(token_type, result, self.line, start_col)

    def scan_string(self) -> Token:
        """
        Diagrama de transição para constantes de caracteres (string_constant).
        q0: '"' -> q1
        q1: 'qualquer' -> q1. 
            '"' -> ACEITAR.
        """
        start_col = self.col    # Guarda a coluna inicial do token
        result = '"'            # Inicia o resultado com aspa dupla
        self.advance()          # Consome a aspa inicial da fonte

        # Lê quaisquer caracteres enquanto a aspa não é fechada
        while self.current_char is not None and self.current_char != '"':
            if self.current_char == '\n':
                raise LexicalError(
                    f"Erro léxico na linha {self.line}, coluna {self.col}: String não fechada.")
            result += self.current_char
            self.advance()

        if self.current_char == '"':
            result += '"'   # Fecha o resultado com aspa dupla
            self.advance()  # Consome a aspa final da fonte
        else:
            raise LexicalError(
                f"Erro léxico na linha {self.line}, coluna {self.col}: String não fechada.")

        return Token('string_constant', result, self.line, start_col)

    def scan_operator_or_punctuation(self) -> Token:
        """
        Diagrama de transição para operadores e pontuação.
        q0: '=' | '<' | '>' | '!' -> q1
        q1: se lookahead '=' -> consome '=' e ACEITA relop 
            'outro' -> ACEITA operador
        """
        start_col = self.col        # Guarda a coluna inicial do token
        char = self.current_char

        # Verifica operadores relacionais duplos (==, !=, <=, >=)
        if char in self.REL_OPS:
            next_char = self.peek()
            if next_char == '=':
                self.advance()  # Consome primeiro caractere
                self.advance()  # Consome '='
                return Token(char + '=', char + '=', self.line, start_col)

        # Verifica outros operadores simples e pontuação
        if char in self.SINGLE_CHAR_TOKENS:
            self.advance()
            return Token(char, char, self.line, start_col)

        # Neste ponto o caractere não é reconhecido na gramática
        raise LexicalError(
            f"Erro léxico na linha {self.line} e coluna {self.col}: Caractere inválido '{char}'.")

    def get_next_token(self) -> Token:
        """
        Lê um token iniciando o diagrama de transição adequado para seu tipo. 
        Considera que o estado inicial (q0) de cada diagrama é lido aqui.
        """
        while self.current_char is not None:

            # Verifica espaços em branco
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            # Verifica letra ou '_' -> ident ou palavra reservada
            if self.current_char.isalpha() or self.current_char == '_':
                return self.scan_identifier_or_keyword()

            # Verifica dígito -> constante numérica
            if self.current_char.isdigit():
                return self.scan_number()

            # Verifica aspas duplas -> constante string
            if self.current_char == '"':
                return self.scan_string()

            # Neste ponto apenas operadores e pontuação são possíveis
            return self.scan_operator_or_punctuation()

        return Token('EOF', 'EOF', self.line, self.col)

    def scan_all(self) -> list[Token]:
        """Verifica todos os tokens até o encontra EOF ou um erro."""
        tokens = []
        try:
            while True:
                token = self.get_next_token()
                tokens.append(token)
                if token.type == 'EOF':
                    break
            return tokens
        except LexicalError as e:
            print(str(e))
            sys.exit(1)  # Aborta a execução do programa
