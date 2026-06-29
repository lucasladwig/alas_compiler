import sys
from src.lexer.scanner import Token
from src.parser.grammar import LL1_TABLE, TERMINALS


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current_idx = 0
        self.stack = ['EOF', 'PROGRAM']

        # Attach the imported data
        self.table = LL1_TABLE
        self.terminals = TERMINALS

    def report_error(self, top_symbol: str, current_token: Token):
        """Formats and outputs the strict syntax error message required by the specification."""
        sentential_form = " ".join(reversed(self.stack + [top_symbol]))

        error_msg = (
            f"--- ERRO SINTÁTICO ---\n"
            f"Mensagem de insucesso: Entrada na tabela de reconhecimento sintático vazia.\n"
            f"Tabela[ {top_symbol} , {current_token.type} ] está VAZIA.\n"
            f"Forma sentencial atual (Pilha): {sentential_form}\n"
            f"Símbolo não-terminal mais à esquerda: {top_symbol}\n"
            f"Token da entrada atual: {current_token.type} (Valor: '{current_token.value}' na Linha {current_token.line}, Coluna {current_token.column})\n"
        )
        print(error_msg)
        sys.exit(1)

    def parse(self):
        """Loop principal do analisador sintático."""
        while len(self.stack) > 0:
            top = self.stack.pop()
            current_token = self.tokens[self.current_idx]

            if top == 'epsilon':
                continue

            if top in self.terminals:
                if top == current_token.type:
                    self.current_idx += 1
                else:
                    print(
                        f"Erro Sintático: Esperado terminal '{top}', mas encontrou '{current_token.type}' na linha {current_token.line}.")
                    sys.exit(1)
            else:
                # It's a non-terminal, look up the rule in the parsing table
                rule_dict = self.table.get(top, {})
                production = rule_dict.get(current_token.type)

                if production is None:
                    # Table entry is empty! Trigger the required error report.
                    self.report_error(top, current_token)
                else:
                    # Push production to stack in reverse order
                    if production != ['epsilon']:
                        for symbol in reversed(production):
                            self.stack.append(symbol)

        # If stack is empty and we reached EOF, parsing is successful
        if self.tokens[self.current_idx].type == 'EOF':
            print("Mensagem de sucesso: Análise sintática concluída sem erros.")
        else:
            print(
                "Erro Sintático: Pilha vazia, mas a entrada não foi totalmente consumida.")
            sys.exit(1)


class SyntaxErrorLog(Exception):
    pass
