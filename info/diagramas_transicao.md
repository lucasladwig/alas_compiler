# Diagramas de Transição - Analisador Léxico (AL)

Este documento detalha os diagramas de transição implementados no analisador léxico para a linguagem LCC-2026-1. O analisador processa a entrada caractere por caractere, mudando de estado com base nas regras abaixo.

---

## 1. Identificadores e Palavras-Reservadas (`ident` / keywords)

Captura de nomes de variáveis, funções ou palavras reservadas (como `def`, `int`, `if`, etc.).

* **Estado 0 (Inicial):**
    * Lê uma Letra (a-z, A-Z) ou sublinhado (`_`) $\rightarrow$ Vai para **Estado 1**
* **Estado 1:**
    * Lê uma Letra, Dígito (0-9) ou sublinhado (`_`) $\rightarrow$ Permanece no **Estado 1**
    * Lê qualquer outro caractere $\rightarrow$ Vai para **Estado Final (Aceitação)**
* **Ação de Aceitação:** O buffer acumulado é verificado contra a tabela de palavras-reservadas. Se existir, o token correspondente é emitido. Caso contrário, é classificado como `ident` e registrado na Tabela de Símbolos.

---

## 2. Constantes Numéricas (`int_constant` e `float_constant`)

Leitura de números inteiros ou de ponto flutuante.

* **Estado 0 (Inicial):**
    * Lê um Dígito (0-9) $\rightarrow$ Vai para **Estado 1**
* **Estado 1 (Inteiro):**
    * Lê um Dígito $\rightarrow$ Permanece no **Estado 1**
    * Lê um ponto (`.`) $\rightarrow$ Vai para **Estado 2**
    * Lê qualquer outro caractere $\rightarrow$ Vai para **Estado Final (Aceita `int_constant`)**
* **Estado 2 (Ponto Flutuante - Transição):**
    * Lê um Dígito $\rightarrow$ Vai para **Estado 3**
    * Lê qualquer outro caractere $\rightarrow$ Vai para **Estado Final (Aceita `float_constant`)** (exemplo: 123. = 123.0)
* **Estado 3 (Ponto Flutuante - Corpo):**
    * Lê um Dígito $\rightarrow$ Permanece no **Estado 3**
    * Lê qualquer outro caractere $\rightarrow$ Vai para **Estado Final (Aceita `float_constant`)**

---

## 3. Constantes de Texto (`string_constant`)

Processamento de strings literais delimitadas por aspas duplas. Aspas simples não são aceitas.

* **Estado 0 (Inicial):**
    * Lê aspas duplas (`"`) $\rightarrow$ Vai para **Estado 1**
* **Estado 1 (Corpo da String):**
    * Lê qualquer caractere (exceto `"` e `\n`) $\rightarrow$ Permanece no **Estado 1**
    * Lê aspas duplas (`"`) $\rightarrow$ Vai para **Estado Final (Aceita `string_constant`)**
    * Lê quebra de linha (`\n`) ou Fim de Arquivo (EOF) $\rightarrow$ **Erro Léxico** (String não fechada)

---

## 4. Operadores Compostos e Simples

Usa um *lookahead* ('espia' o próximo caractere) para diferenciar operadores de um caractere (ex: `=`) de operadores de dois caracteres (ex: `==`).

* **Estado 0 (Inicial):**
    * Lê `=`, `<`, `>`, ou `!` $\rightarrow$ Vai para **Estado 1**
* **Estado 1:**
    * Se o próximo caractere (lookahead) for `=` $\rightarrow$ Consome o `=` e vai para **Estado Final (Aceita operador duplo: `==`, `<=`, `>=`, `!=`)**
    * Se o próximo caractere não for `=` $\rightarrow$ Não consome o próximo caractere. Vai para **Estado Final (Aceita operador simples: `=`, `<`, `>`)**

---

## 5. Espaços em Branco
*O analisador foi programado para ignorar espaços em branco, tabulações e quebras de linha (mas incrementando o contador de linhas).*
