import sys
from lexer.scanner import Token
from parser.grammar import LL1_TABLE, TERMINALS


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current_idx = 0
        # Inicia pilha com EOF e Simbolo inicial
        self.stack = ['EOF', 'PROGRAM']
        self.table = LL1_TABLE
        self.terminals = TERMINALS

    def report_error(self, top_symbol: str, current_token: Token):
        """Cria e formata a mensagem de erro sintático."""
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

            # --- NOVA PROTEÇÃO ---
            if self.current_idx >= len(self.tokens):
                print("Erro Sintático: Fim de arquivo inesperado.")
                sys.exit(1)

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
                # É uma variável, busca a regra na tabela de parsing
                rule_dict = self.table.get(top, {})
                production = rule_dict.get(current_token.type)

                if production is None:
                    # Entrada na tabela está vazia, enviar mensagem de erro
                    self.report_error(top, current_token)
                else:
                    # Coloca a produção na pilha em ordem reversa
                    if production != ['epsilon']:
                        for symbol in reversed(production):
                            self.stack.append(symbol)

        # Se a pilha está vazia e chegamos no EOF, a análise foi bem-sucedida
        if self.current_idx == len(self.tokens):
            print("Mensagem de sucesso: Análise sintática concluída sem erros.")
        else:
            print(
                "Erro Sintático: Pilha vazia, mas a entrada não foi totalmente consumida.")
            sys.exit(1)


class SyntaxErrorLog(Exception):
    pass
