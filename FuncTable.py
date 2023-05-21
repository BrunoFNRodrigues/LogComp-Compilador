
class FuncTable():
    table = {}
    
    def Getter(key):
        return FuncTable.table[key]
    
    def Setter(key, value):
        FuncTable.table[key] = value
