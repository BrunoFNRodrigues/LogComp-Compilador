from abc import ABC, abstractmethod
from SymbolTable import SymbolTable
from FuncTable import FuncTable

class Node(ABC):
    def __init__(self, value=0, children=[]):
        self.value = value
        self.children = children

    @abstractmethod
    def Evaluate(self, table = 0):
        None

class BinOp(Node):
    def Evaluate(self, table = 0):
        if self.value == "==":
            res = self.children[1].Evaluate(table)[1] == self.children[0].Evaluate(table)[1]
        elif self.value == ">":
            res = self.children[1].Evaluate(table)[1]>self.children[0].Evaluate(table)[1]
        elif self.value == "<":
            res = self.children[1].Evaluate(table)[1]<self.children[0].Evaluate(table)[1]
        elif self.value == "||":
            res = self.children[1].Evaluate(table)[1] or self.children[0].Evaluate(table)[1]
        elif self.value == "&&":
            res = self.children[1].Evaluate(table)[1] and self.children[0].Evaluate(table)[1]  
        elif self.children[0].Evaluate(table)[0] != self.children[1].Evaluate(table)[0]:
            raise Exception("BinOP precisa que"+self.children[1].Evaluate(table)[0]+"="+self.children[0].Evaluate(table)[0])
        elif self.value == "-":
            res = self.children[1].Evaluate(table)[1]-self.children[0].Evaluate(table)[1]
        elif self.value == "+":
            res = self.children[1].Evaluate(table)[1]+self.children[0].Evaluate(table)[1]
        elif self.value == "*":
            res = self.children[1].Evaluate(table)[1]*self.children[0].Evaluate(table)[1]
        elif self.value == "/":
            res = self.children[1].Evaluate(table)[1]/self.children[0].Evaluate(table)[1]

        return ("Int", int(res))

class UnOp(Node):
    def Evaluate(self, table = 0):
        if self.children.Evaluate(table)[0] != "Int":
            raise Exception("UnOP não aceita"+self.children.Evaluate(table)[0])
        if self.value == "-":
            return ("Int", -self.children.Evaluate(table)[1])
        if self.value == "+":
            return ("Int", self.children.Evaluate(table)[1])
        if self.value == "!":
            return ("Int", not self.children.Evaluate(table)[1])

class ConcatOp(Node):
    def Evaluate(self, table = 0):
        return ("String" ,str(self.children[1].Evaluate(table)[1]) + str(self.children[0].Evaluate(table)[1]))

class IntVal(Node):
    def Evaluate(self, table = 0):
        return ("Int", self.value)

class StringVal(Node):
    def Evaluate(self, table = 0):
        return ("String", self.value)

class NoOp(Node):
    def Evaluate(self, table = 0):
        return None

class Identifier(Node):
    def Evaluate(self, table = 0):
        return table.Getter(self.value)
    
class Block(Node):
    def Evaluate(self, table = 0):
        for child in self.children:
            child.Evaluate(table)
            if isinstance(child, Return):
                return child.Evaluate(table)

class Print(Node):
    def Evaluate(self, table = 0):
            print(self.children.Evaluate(table)[1])

class Assignment(Node):
    def Evaluate(self, table = 0):
        table.Setter(self.children[0].value, self.children[1].Evaluate(table))
    
class Read(Node):
    def Evaluate(self, table = 0):
        return ("Int", int(input()))
    
class While(Node):
    def Evaluate(self, table = 0):
        while self.children[1].Evaluate(table)[1]:
            self.children[0].Evaluate(table)

class If(Node):
    def Evaluate(self, table = 0):
        if self.children[-1].Evaluate(table):
            self.children[-2].Evaluate(table)
        elif len(self.children) > 2:
            self.children[0].Evaluate(table)

class VarDec(Node):
    def Evaluate(self, table = 0):
        if len(self.children) <= 1:
            if self.value == "Int":
                table.Create(self.children[0].value, ["Int", 0])
            elif self.value == "String":
                table.Create(self.children[0].value, ["String", ""])
        else:
            table.Create(self.children[0].value, self.children[1].Evaluate(table))
        
class Return(Node):
    def Evaluate(self, table = 0):
        return self.children.Evaluate(table)

class FuncDec(Node):
    def Evaluate(self, table = 0):
        if len(self.children) != 3:
            raise Exception("func declarada errada")
        FuncTable.Setter(self.children[0].value, (self.value, self))

class FuncCall(Node):
    def Evaluate(self, table = 0):
        func = FuncTable.Getter(self.value.value)
        if len(func[1].children[1]) != len(self.children):
            raise Exception("São "+str(len(func[1].children[1]))+" mas foram recebidos"+ str(len(self.children)))
        new_st = SymbolTable()
        for var in func[1].children[1]:
            var.Evaluate(new_st)    
        i = 0
        for key in new_st.table.keys():
            new_st.Setter(key, self.children[i].Evaluate(table))
            i+=1      
        return func[1].children[2].Evaluate(new_st)   
        