from abc import ABC, abstractmethod
from SymbolTable import SymbolTable

class Node(ABC):
    def __init__(self, value=0, children=[]):
        self.value = value
        self.children = children

    @abstractmethod
    def Evaluate(self):
        None

class BinOp(Node):
    def Evaluate(self):
        if self.children[0].Evaluate()[0] != self.children[1].Evaluate()[0]:
            raise Exception("BinOP precisa que"+self.children[1].Evaluate()[0]+"="+self.children[0].Evaluate()[0])
        if self.value == "-":
            res = self.children[1].Evaluate()[1]-self.children[0].Evaluate()[1]
        elif self.value == "+":
            res = self.children[1].Evaluate()[1]+self.children[0].Evaluate()[1]
        elif self.value == "*":
            res = self.children[1].Evaluate()[1]*self.children[0].Evaluate()[1]
        elif self.value == "/":
            res = self.children[1].Evaluate()[1]/self.children[0].Evaluate()[1]
        elif self.value == "==":
            res = self.children[1].Evaluate()[1] == self.children[0].Evaluate()[1]
        elif self.value == ">":
            res = self.children[1].Evaluate()[1]>self.children[0].Evaluate()[1]
        elif self.value == "<":
            res = self.children[1].Evaluate()[1]<self.children[0].Evaluate()[1]
        elif self.value == "||":
            res = self.children[1].Evaluate()[1] or self.children[0].Evaluate()[1]
        elif self.value == "&&":
            res = self.children[1].Evaluate()[1] and self.children[0].Evaluate()[1]
        return ("Int", int(res))

class UnOp(Node):
    def Evaluate(self):
        if self.children.Evaluate()[0] != "Int":
            raise Exception("UnOP não aceita"+self.children.Evaluate()[0])
        if self.value == "-":
            return ("Int", -self.children.Evaluate()[1])
        if self.value == "+":
            return ("Int", self.children.Evaluate()[1])
        if self.value == "!":
            return ("Int", not self.children.Evaluate()[1])

class ConcatOp(Node):
    def Evaluate(self):
        return ("String" ,str(self.children[1].Evaluate()[1]) + str(self.children[0].Evaluate()[1]))

class IntVal(Node):
    def Evaluate(self):
        return ("Int", self.value)

class StringVal(Node):
    def Evaluate(self):
        return ("String", self.value)

class NoOp(Node):
    def Evaluate(self):
        return None

class Identifier(Node):
    def Evaluate(self):
        return SymbolTable.Getter(self.value)
    
class Block(Node):
    def Evaluate(self):
        for child in self.children:
            child.Evaluate()

class Print(Node):
    def Evaluate(self):
            print(self.children.Evaluate()[1])

class Assignment(Node):
    def Evaluate(self):
        SymbolTable.Setter(self.children[0].value, self.children[1].Evaluate())
    
class Read(Node):
    def Evaluate(self):
        return ("Int", int(input()))
    
class While(Node):
    def Evaluate(self):
        while self.children[1].Evaluate()[1]:
            self.children[0].Evaluate()

class If(Node):
    def Evaluate(self):
        if self.children[-1].Evaluate():
            self.children[-2].Evaluate()
        elif len(self.children) > 2:
            self.children[0].Evaluate()

class VarDec(Node):
    def Evaluate(self):
        if len(self.children) <= 1:
            if self.value == "Int":
                SymbolTable.Create(self.children[0].value,["Int", 0])
            elif self.value == "String":
                SymbolTable.Create(self.children[0].value, ["String", ""])
        else:
            SymbolTable.Create(self.children[0].value, self.children[1].Evaluate())
        