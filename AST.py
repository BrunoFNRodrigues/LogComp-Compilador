from abc import ABC, abstractmethod
from SymbolTable import SymbolTable
from FuncTable import FuncTable

class Node(ABC):
    def __init__(self, value=0, children=[]):
        self.value = value
        self.children = children

    @abstractmethod
    def Evaluate(self, table = []):
        None

class BinOp(Node):
    def Evaluate(self, table = []):
        if self.value == "==":
            res = self.children[1].Evaluate()[1] == self.children[0].Evaluate()[1]
        elif self.value == ">":
            res = self.children[1].Evaluate()[1]>self.children[0].Evaluate()[1]
        elif self.value == "<":
            res = self.children[1].Evaluate()[1]<self.children[0].Evaluate()[1]
        elif self.value == "||":
            res = self.children[1].Evaluate()[1] or self.children[0].Evaluate()[1]
        elif self.value == "&&":
            res = self.children[1].Evaluate()[1] and self.children[0].Evaluate()[1]  
        elif self.children[0].Evaluate()[0] != self.children[1].Evaluate()[0]:
            raise Exception("BinOP precisa que"+self.children[1].Evaluate()[0]+"="+self.children[0].Evaluate()[0])
        elif self.value == "-":
            res = self.children[1].Evaluate()[1]-self.children[0].Evaluate()[1]
        elif self.value == "+":
            res = self.children[1].Evaluate()[1]+self.children[0].Evaluate()[1]
        elif self.value == "*":
            res = self.children[1].Evaluate()[1]*self.children[0].Evaluate()[1]
        elif self.value == "/":
            res = self.children[1].Evaluate()[1]/self.children[0].Evaluate()[1]

        return ("Int", int(res))

class UnOp(Node):
    def Evaluate(self, table = []):
        if self.children.Evaluate()[0] != "Int":
            raise Exception("UnOP não aceita"+self.children.Evaluate()[0])
        if self.value == "-":
            return ("Int", -self.children.Evaluate()[1])
        if self.value == "+":
            return ("Int", self.children.Evaluate()[1])
        if self.value == "!":
            return ("Int", not self.children.Evaluate()[1])

class ConcatOp(Node):
    def Evaluate(self, table = []):
        return ("String" ,str(self.children[1].Evaluate()[1]) + str(self.children[0].Evaluate()[1]))

class IntVal(Node):
    def Evaluate(self, table = []):
        return ("Int", self.value)

class StringVal(Node):
    def Evaluate(self, table = []):
        return ("String", self.value)

class NoOp(Node):
    def Evaluate(self, table = []):
        return None

class Identifier(Node):
    def Evaluate(self, table = []):
        return table.Getter(self.value)
    
class Block(Node):
    def Evaluate(self, table = []):
        for child in self.children:
            child.Evaluate(table)
            if isinstance(child, Return):
                break

class Print(Node):
    def Evaluate(self, table = []):
            print(self.children.Evaluate()[1])

class Assignment(Node):
    def Evaluate(self, table = []):
        table.Setter(self.children[0].value, self.children[1].Evaluate())
    
class Read(Node):
    def Evaluate(self, table = []):
        return ("Int", int(input()))
    
class While(Node):
    def Evaluate(self, table = []):
        while self.children[1].Evaluate()[1]:
            self.children[0].Evaluate()

class If(Node):
    def Evaluate(self, table = []):
        if self.children[-1].Evaluate():
            self.children[-2].Evaluate()
        elif len(self.children) > 2:
            self.children[0].Evaluate()

class VarDec(Node):
    def Evaluate(self, table = []):
        if len(self.children) <= 1:
            if self.value == "Int":
                table.Create(self.children[0].value,["Int", 0])
            elif self.value == "String":
                table.Create(self.children[0].value, ["String", ""])
        else:
            table.Create(self.children[0].value, self.children[1].Evaluate())
        
class Return(Node):
    def Evaluate(self, table = []):
        return self.children[0].Evaluate()

class FuncDec(Node):
    def Evaluate(self, table = []):
        if len(self.children) != len(self.children[1]) + 2:
            raise Exception("func declarada errada")
        FuncTable.Setter(self.children[0].value, (self.value, self))

class FuncCall(Node):
    def Evaluate(self, table = []):
        func = FuncTable.Getter(self.value)
        if len(func[1].children[1]) != len(self.children):
            raise Exception("São "+str(len(func[1].children[1]))+" mas foram recebidos"+ str(len(self.children)))
        new_st = SymbolTable()
        for var in func[1].children[1]:
            var.Evaluate(new_st)    
        i = 0
        for key in new_st.table.keys():
            new_st.Setter(key, self.children[i].Evaluate())
            i+=1      
        self.children[3].Evaluate(new_st)   
        