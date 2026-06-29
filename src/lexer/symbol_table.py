class SymbolTable:
    """
    Mantém um registro de todos os identificadores no código fonte, gravando a 
    linha e a coluna onde ocorrem.
    """

    def __init__(self):
        """
        Mapeia o valor léxico do identifcador a uma lista de posições de suas ocorrências
        """
        self.table = {}

    def __repr__(self) -> str:
        """
        Formata a tablea de símbolos para exibição no terminal.
        """
        if not self.table:
            return "Tabela de Símbolos está vazia."

        result = ["--- Tabela de Símbolos ---"]
        for name, occurrences in self.table.items():
            occ_str = ", ".join(
                [f"({lin}, {col})" for lin, col in occurrences])
            result.append(f"{name}: {occ_str}")

        return "\n".join(result)

    def add_occurrence(self, name: str, line: int, column: int) -> None:
        """
        Adiciona uma ocorrência do identificador na tabela.
        Se o identificador ainda não existir, inicializa a lista de ocorrências.
        """
        if name not in self.table:
            self.table[name] = []
        self.table[name].append((line, column))

    def get_occurrences(self, name: str) -> list[tuple[int, int]]:
        """
        Acessa a lista de ocorrências de um identificador.
        Retorna uma lista vazia se o identificador não foi registrado.
        """
        return self.table.get(name, [])
