
class SymbolTable():
    reserved = ["println", "readline", "while", "if", "else"]
        
    def __init__(self):
        self.table = {}
        
    def Getter(self, key):
        if key in SymbolTable.reserved:
            raise Exception("Palavra reservada")
        if key in self.table.keys():
            return self.table[key]
    
    def Setter(self, key, value):
        if value[0] != self.table[key][0]:
            raise Exception("Tipo não combina: "+value[0]+"!="+self.table[key][0]) 
        self.table[key] = value

    def Create(self, key, value):
        if key in self.table.keys():
            raise Exception("Variavel já existe")
        else:
            self.table[key] = value

