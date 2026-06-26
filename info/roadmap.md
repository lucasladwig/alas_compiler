### Phase 1: Grammar Engineering (The Foundation)

You cannot write the parser until the grammar is mathematically sound. This must happen first.

- **Step 1: EBNF to Conventional BNF:** Convert all the `?`, `*`, and `+` operators in the CC-2026-1 grammar into standard recursive production rules using $\epsilon$.
- **Step 2: Left-Factoring:** Resolve the $FIRST/FIRST$ conflicts. Specifically, factor the `ATRIBSTAT` rule (the right-hand side `ident` conflict) and the parameter/function lists.
- **Step 3: Eliminate Left Recursion:** Rewrite the expression rules (like `NUMEXPRESSION`) to use right recursion instead, ensuring the top-down parser won't enter an infinite loop.
- **Step 4: The $LL(1)$ Proof:** Calculate the $FIRST$ and $FOLLOW$ sets for every non-terminal in your new LCC-2026-1 grammar to prove it is officially an $LL(1)$ grammar.


### Phase 2: The Lexical Analyzer (Task AL)

With the grammar’s terminals defined, you can build the scanner.

- **Step 5: Transition Diagrams & Scanner:** Implement the core loop that reads the input file strictly character by character to identify tokens.
- **Step 6: The Symbol Table:** Create the data structure specifically for tracking the `ident` tokens. Ensure it records every line and column occurrence of each identifier.
- **Step 7: Error Handling:** Implement the logic to catch invalid characters and output the required simple lexical error message containing the line and column.


### Phase 3: The Syntactic Analyzer (Task AS)

This is where the grammar math from Phase 1 turns into code.

- **Step 8: Parsing Table Construction:** Hardcode or write a script to generate the $LL(1)$ parsing table based on your $FIRST$ and $FOLLOW$ sets. Ensure your code only builds this table once per execution.
- **Step 9: Stack-Based Parser:** Implement the main parsing algorithm. It will read the token stream from Phase 2, compare it against the parsing table, and manage the stack.
- **Step 10: Syntax Error Reporting:** Build the specific error output required: if an error occurs, the parser must report the empty table entry, the sentential form, the leftmost non-terminal, and the current token.


### Phase 4: Deliverables & Testing

Do not leave the administrative requirements for the last minute.

- **Step 11: The Test Programs:** Write the three required `.lcc` test programs. They must be at least 100 lines each, with absolutely zero lexical or syntactic errors. *Tip: Write a quick Python script to generate valid 100-line blocks of repetitive math or variable declarations to save time.*
- **Step 12: Build the Makefile:** Create the `Makefile` ensuring you explicitly state it runs on Python 3.11.2.
- **Step 13: Documentation:** Draft the `README` with clear execution instructions and ensure all group members' names are in the file headers.


### Phase 5: Final Review

- **Step 14: End-to-End Validation:** Run the entire suite using your `Makefile`. Ensure there are absolutely no compilation warnings, as they will reduce your grade. Package and upload to Moodle before 23:55h.