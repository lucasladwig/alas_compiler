import sys
import time
from lexer.symbol_table import SymbolTable
from lexer.scanner import Scanner
from parser.analyzer import Parser


def main():
    # Validação da chamada no terminal (Exigência: receber um único caminho de arquivo)
    if len(sys.argv) != 2:
        print("Uso correto: python3 src/main.py <caminho_do_arquivo.lcc>")
        sys.exit(1)

    filepath = sys.argv[1]

    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            source_code = file.read()
    except FileNotFoundError:
        print(f"Erro: O arquivo '{filepath}' não foi encontrado.")
        sys.exit(1)

    print(f"--- Iniciando compilação: {filepath} ---")

    # Iniciar o relógio para verificar desempenho
    start_time = time.perf_counter()

    # === FASE 1: Análise Léxica (Tarefa AL) ===
    symbol_table = SymbolTable()
    scanner = Scanner(source_code, symbol_table)
    tokens = scanner.scan_all()

    # === FASE 2: Análise Sintática (Tarefa AS) ===
    parser = Parser(tokens)
    parser.parse()

    # Parar o relógio e calcula o tempo
    end_time = time.perf_counter()
    execution_time = end_time - start_time

    # === SAÍDAS BEM-SUCEDIDAS ===
    # (A mensagem de sucesso da análise sintática já é impressa pelo parser.parse())

    print("\n--- Lista de Tokens ---")
    # Imprimindo a lista de tokens na ordem em que ocorrem (Exigência da Tarefa AL)
    token_list_str = "[" + ", ".join([t.type for t in tokens]) + "]"

    # Limitando a exibição no terminal se for muito grande para não travar a tela,
    # mas garantindo que a estrutura está correta.
    if len(token_list_str) > 500:
        print(token_list_str[:500] + " ... (truncado para exibição)]")
    else:
        print(token_list_str)

    print("\n" + str(symbol_table))

    print(f"\nTempo total de compilação: {execution_time:.6f} segundos")


if __name__ == "__main__":
    main()
