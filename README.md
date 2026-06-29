# Exercício-Programa: ALAS

Este projeto consiste na implementação de um analisador léxico e sintático completo para a linguagem `LCC-2026-1`, desenvolvido como parte da disciplina de Introdução a Compiladores. O compilador inclui um analisador léxico baseado em diagrmas de transição e um analisador sintático para uma gramática em $LL(1)$.

## Integrantes do Grupo
* Carlos Eduardo Amâncio Botelho (20104214)
* Lucas Ladwig (22100910)

## Estrutura do Projeto
* `/info`: Detalhamento sobre conversão da gramática para $LL(1)$ e os diagramas de transição do *scanner* de tokens.
* `/src`: Código-fonte do projeto.
    * `/lexer`: Implementação do Analisador Léxico.
    * `/parser`: Implementação do Analisador Sintático.
* `/tests`: Conjunto de testes contendo os programas exemplo e casos de erro (`.lcc`).
* `Makefile`: Automação para compilação, testes e limpeza.

## Requisitos
* **Linguagem:** Python 3.11.2 ou superior.

## Instalação
Não é necessária instalação de bibliotecas externas. Certifique-se de ter o Python 3.11 instalado:
```bash
python3.11 --version
```

## Execução
Para executar os testes dos programas **válidos** na linguagem (`.lcc`):
```bash
make test
```

Para executar os testes dos programas **inválidos** na linguagem (`.lcc`):
```bash
make test-errors
```

Para efetuar limpeza de cache e arquivos temporários:
```bash
make clean
```