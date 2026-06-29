# Makefile para Analisador Léxico e Sintático LCC-2026-1
# Versão Python Requerida: 3.11.2

# Define o executável Python 3.11 conforme especificado
PYTHON = python3.11

.PHONY: all clean run test test-errors

all: 
	@echo "Construção do compilador LCC-2026-1 concluída."
	@echo "Use 'make run FILE=<caminho>' para analisar um arquivo."
	@echo "Use 'make test' para validar os algoritmos obrigatórios."
	@echo "Use 'make test-errors' para validar o tratamento de erros."

# Executa o compilador em um arquivo específico
run:
	@if [ -z "$(FILE)" ]; then \
		echo "Erro: Forneça o arquivo de entrada. Ex: make run FILE=tests/programa1.lcc"; \
		exit 1; \
	fi
	$(PYTHON) src/main.py $(FILE)

# Executa os 3 algoritmos de teste (100+ linhas cada)
test:
	@echo "--- Executando testes de performance e corretude ---"
	$(PYTHON) src/main.py tests/program_1_a_star.lcc
	$(PYTHON) src/main.py tests/program_2_sudoku.lcc
	$(PYTHON) src/main.py tests/program_3_dh.lcc

# Executa os arquivos de erro para validar o relatório de falhas
test-errors:
	@echo "--- Validando tratamento de erros ---"
	@echo "Esperado: Erro Léxico na linha 5"
	-$(PYTHON) src/main.py tests/program_4_lex_error.lcc
	@echo "\nEsperado: Erro Sintático na tabela (TERM, *)"
	-$(PYTHON) src/main.py tests/program_5_syn_error.lcc

# Limpeza de arquivos temporários de compilação
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	@echo "Limpeza concluída."