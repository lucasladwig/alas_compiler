# Conversão da Gramática CC-2026-1 para LL(1)

Aqui é documentado como cada regra da gramática original **CC-2026-1** (em formato BNF) foi reescrita para a forma convencional e após convertida para $LL(1)$, podendo assim produzir a linguagem **LCC-2026-1**.

A conversão tem como foco principal a **remoção dos operadores BNF** (como `?` e `*`), **eliminar a recursão à esquerda** para evitar loops infinitos do *parser*, e **fatorar à esquerda** para resolver conflitos do tipo $FIRST/FIRST$ e $FIRST/FOLLOW$.

---

## 1. Ponto de Entrada

### `PROGRAM`
* **Original:** `PROGRAM -> (STATEMENT | FUNCLIST)?`
* **Conversão:** O operador BNF `?` (opcional) foi removido expandindo suas produções e incluindo `ε` (cadeia vazia).
* **Final:**
    ```text
    PROGRAM -> STATEMENT 
             | FUNCLIST 
             | ε
    ```

### `FUNCLIST`
* **Original:** `FUNCLIST -> FUNCDEF FUNCLIST | FUNCDEF`
* **Conversão:** Esta regra apresentava um conflito do tipo $FIRST/FIRST$ pois ambas produções começam com `FUNCDEF`. A regra foi fatorada à esquerda extraindo `FUNCDEF` e criando uma nova regra (`FUNCLIST_TAIL`).
* **Final:**
    ```text
    FUNCLIST      -> FUNCDEF FUNCLIST_TAIL
    FUNCLIST_TAIL -> FUNCLIST 
                   | ε
    ```

### `FUNCDEF`
* **Original:** `FUNCDEF -> def ident ( PARAMLIST ) { STATELIST }`
* **Conversão:** Não foi necessária pois inicia no terminal `def` e não apresenta outras ramificações.

---

## 2. Parâmetros e Listas

### `PARAMLIST`
* **Original:** `PARAMLIST -> ( (int | float | string) ident , PARAMLIST | (int | float | string) ident )?`
* **Conversão:** O identificador de tipo `(int | float | string)` foi agrupado em uma nova variável `TYPE`. A regra original apresentava ambiguidade pois ambas produções começam com `TYPE ident`, então `TYPE ident` foi extraído para a nova regra `PARAMLIST_TAIL`. Foi também adicionado `ε` para manter o caráter opcional da regra.
* **Final:**
    ```text
    PARAMLIST      -> TYPE ident PARAMLIST_TAIL
                    | ε
    PARAMLIST_TAIL -> , PARAMLIST
                    | ε
    TYPE           -> int | float | string
    ```

### `PARAMLISTCALL`
* **Original:** `PARAMLISTCALL -> (ident , PARAMLISTCALL | ident)?`
* **Conversão:** Mesmo caso da regra anterior `PARAMLIST`. O prefixo `ident` foi fatorado para resolver a ambiguidade.
* **Final:**
    ```text
    PARAMLISTCALL      -> ident PARAMLISTCALL_TAIL
                        | ε
    PARAMLISTCALL_TAIL -> , PARAMLISTCALL
                        | ε
    ```

---

## 3. Comandos (*Statements* e *Declarations*)

### `STATEMENT`
* **Original:** `STATEMENT -> VARDECL ; | ATRIBSTAT ; | PRINTSTAT ; | READSTAT ; | RETURNSTAT ; | IFSTAT | FORSTAT | { STATELIST } | break ; | ;`
* **Conversão:** Nenhuma alteração foi necessária para esta regra, pois cada produção começa com um símbolo distinto sem conflitos aparentes.

### `STATELIST`
* **Original:** `STATELIST -> STATEMENT ( STATELIST )?`
* **Conversão:** A regra opcional `?` foi convertida em uma nova regra `STATELIST_TAIL` com `ε`.
* **Final:**
    ```text
    STATELIST      -> STATEMENT STATELIST_TAIL
    STATELIST_TAIL -> STATELIST
                    | ε
    ```

### `VARDECL`
* **Original:** `VARDECL -> (int | float | string) ident ( [ int.constant ] )*`
* **Conversão:** O operador `*` foi substituído por uma recursão à direita com o símbolo `VARINDEXLIST`. Os tipos foram agrupados em `TYPE`.
* **Final:**
    ```text
    VARDECL      -> TYPE ident VARINDEXLIST
    VARINDEXLIST -> [ int_constant ] VARINDEXLIST
                  | ε
    ```

### `IFSTAT` (Resolução do *Dangling Else*)
* **Original:** `IFSTAT -> if ( EXPRESSION ) STATEMENT ( else STATEMENT )?`
* **Conversão:** O bloco opcional `( else ... )?` foi substituído por uma regra de cauda `IFSTAT_TAIL`.
* **Final:**
    ```text
    IFSTAT      -> if ( EXPRESSION ) STATEMENT IFSTAT_TAIL
    IFSTAT_TAIL -> else STATEMENT 
                 | ε
    ```

---

## 4. O Conflito Crítico do `ident` (Atribuições e Expressões)

Esta seção exigiu a refatoração mais pesada devido aos conflitos $FIRST/FIRST$.

### `ATRIBSTAT`
* **Original:** `ATRIBSTAT -> LVALUE = (EXPRESSION | ALLOCEXPRESSION | FUNCCALL)`
* **Lógica de Conversão:**
    1. Primeiro, `LVALUE =` foi fatorada em uma nova regra `ATRIBSTAT_RHS`.
    2. Como `EXPRESSION` e `FUNCCALL` podem começar com um token `ident`, um analisador $LL(1)$ não consegue decidir qual ramo seguir. Depois `ATRIBSTAT_RHS` foi nivelada. Se o analisador vir um `ident`, ele é roteado para `IDENT_ATRIB_TAIL`, que então verifica o *próximo* token (ex: um `(` significa uma chamada de função; operadores significam uma expressão).
    3. `FACTOR_NO_IDENT` foi adicionado para lidar com expressões que *não* começam com um identificador, preservando a precedência matemática.
* **Final:**
    ```text
    ATRIBSTAT        -> LVALUE = ATRIBSTAT_RHS
    
    ATRIBSTAT_RHS    -> ALLOCEXPR
                      | + FACTOR UNEXPRLIST TERMLIST EXPRESSION_TAIL
                      | - FACTOR UNEXPRLIST TERMLIST EXPRESSION_TAIL
                      | FACTOR_NO_IDENT UNEXPRLIST TERMLIST EXPRESSION_TAIL
                      | ident IDENT_ATRIB_TAIL
                      
    IDENT_ATRIB_TAIL -> ( PARAMLISTCALL )
                      | NUMEXPRLIST UNEXPRLIST TERMLIST EXPRESSION_TAIL
    ```

### `LVALUE`
* **Original:** `LVALUE -> ident ( [ NUMEXPRESSION ] )*`
* **Lógica de Conversão:** O operador `()*` foi substituído por recursão à direita `NUMEXPRLIST`.
* **Final:**
    ```text
    LVALUE      -> ident NUMEXPRLIST
    NUMEXPRLIST -> [ NUMEXPR ] NUMEXPRLIST
                 | ε
    ```

---

## 5. Expressões (Eliminação da Recursão à Esquerda)

Operadores `*` podem gerar recursão à esquerda, portanto foram usadas listas estritamente recursivas à direita para impor a conformidade $LL(1)$.

### `EXPRESSION`
* **Original:** `EXPRESSION -> NUMEXPRESSION ( (< | > | <= | >= | == | !=) NUMEXPRESSION )?`
* **Lógica de Conversão:** `NUMEXPRESSION` (encurtado para `NUMEXPR`) foi extraído e os operadores condicionais movidos para uma regra de cauda.
* **Final:**
    ```text
    EXPRESSION      -> NUMEXPR EXPRESSION_TAIL
    EXPRESSION_TAIL -> < NUMEXPR | > NUMEXPR | <= NUMEXPR | >= NUMEXPR | == NUMEXPR | != NUMEXPR | ε
    ```

### `NUMEXPRESSION` (NUMEXPR) & `TERM`
* **Original `NUMEXPRESSION`:** `TERM ( (+ | -) TERM )*`
* **Original `TERM`:** `UNARY_EXPR ( (* | / | %) UNARY_EXPR )*`
* **Lógica de Conversão:** Ambas as formas requerem recursão à direita em vez de Fechos de Kleene para evitar loops infinitos na descida recursiva (top-down).
* **Final:**
    ```text
    NUMEXPR    -> TERM TERMLIST
    TERMLIST   -> + TERM TERMLIST | - TERM TERMLIST | ε
    
    TERM       -> UNEXPR UNEXPRLIST
    UNEXPRLIST -> * UNEXPR UNEXPRLIST | / UNEXPR UNEXPRLIST | % UNEXPR UNEXPRLIST | ε
    ```

### `UNARY_EXPR` (UNEXPR) & `FACTOR`
* **Original `UNEXPR`:** `(+ | -)? FACTOR`
* **Lógica de Conversão:** O operador opcional foi expandido em derivações explícitas.
* **Final:**
    ```text
    UNEXPR -> + FACTOR | - FACTOR | FACTOR
    ```

* **Original `FACTOR`:** `(int.constant | float.constant | string.constant | null | LVALUE | ( NUMEXPRESSION ))`
* **Lógica de Conversão:** Convertido para um formato de regra vertical padrão. `FACTOR_NO_IDENT` também foi introduzido especificamente para resolver o conflito `ATRIBSTAT` mencionado anteriormente.
* **Final:**
    ```text
    FACTOR          -> int_constant | float_constant | string_constant | null | LVALUE | ( NUMEXPR )
    FACTOR_NO_IDENT -> int_constant | float_constant | string_constant | null | ( NUMEXPR )
    ```
