
class SymbolTable():
    table = {}
    reserved = ["println", "while", "if", "else"]
        
    def Getter(key):
        if key in SymbolTable.reserved:
            raise Exception("Palavra reservada")
        if key in SymbolTable.table.keys():
            return SymbolTable.table[key]
        raise Exception("Variável não incializada")
    
    def Setter(key, value):
        SymbolTable.table[key] = value