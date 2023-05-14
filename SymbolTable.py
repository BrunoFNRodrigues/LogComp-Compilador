
class SymbolTable():
    table = {"0":0}
    reserved = ["println", "readline", "while", "if", "else"]
        
    def Getter(key):
        if key in SymbolTable.reserved:
            raise Exception("Palavra reservada")
        if key in SymbolTable.table.keys():
            return SymbolTable.table[key]
    
    def Setter(key, value):
        if value[0] != SymbolTable.table[key][0]:
            raise Exception("Tipo não combina: "+value[0]+"!="+SymbolTable.table[key][0]) 
        SymbolTable.table[key] = value

    def Create(key, value):
        if key in SymbolTable.table.keys():
            raise Exception("Variavel já existe")
        else:
            SymbolTable.table[key] = value

