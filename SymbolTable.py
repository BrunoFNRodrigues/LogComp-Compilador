
class SymbolTable():
    table = {}
    reserved = ["println"]
        
    def Getter(key):
        if key in reversed:
            raise Exception("Palavra reservada")
        if key in SymbolTable.table.keys():
            return SymbolTable.table[key]
        raise Exception("Variável não incializada")
    
    def Setter(key, value):
        SymbolTable.table[key] = value