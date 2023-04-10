from abc import ABC, abstractmethod
from SymbolTable import SymbolTable

class Node(ABC):
    def __init__(self, value=0, children=[]):
        self.value = value
        self.children = children

    @abstractmethod
    def Evaluate():
        None

class BinOp(Node):
    def Evaluate(self):
        if self.value == "-":
            return self.children[1].Evaluate()-self.children[0].Evaluate()
        elif self.value == "+":
            return self.children[1].Evaluate()+self.children[0].Evaluate()
        elif self.value == "*":
            return self.children[1].Evaluate()*self.children[0].Evaluate()
        elif self.value == "/":
            return self.children[1].Evaluate()/self.children[0].Evaluate()
        elif self.value == "==":
            return self.children[1].Evaluate() == self.children[0].Evaluate()
        elif self.value == ">":
            return self.children[1].Evaluate()>self.children[0].Evaluate()
        elif self.value == "<":
            return self.children[1].Evaluate()<self.children[0].Evaluate()
        elif self.value == "||":
            return self.children[1].Evaluate() or self.children[0].Evaluate()
        elif self.value == "&&":
            return self.children[1].Evaluate() and self.children[0].Evaluate()

class UnOp(Node):
    def Evaluate(self):
        if self.value == "-":
            return -self.children.Evaluate()
        return self.children.Evaluate()
        
class IntVal(Node):
    def Evaluate(self):
        return self.value
    
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
        print(int(self.children.Evaluate()))

class Assignment(Node):
    def Evaluate(self):
        SymbolTable.Setter(self.children[0].value, self.children[1].Evaluate())
    
class Read(Node):
    def Evaluate(self):
        return int(input())
    
class While(Node):
    def Evaluate(self):
        while self.children[1].Evaluate():
            self.children[0].Evaluate()

class If(Node):
    def Evaluate(self):
        if self.children[-1]:
            self.children[-2].Evaluate()
        elif len(self.children) > 2:
            self.children[0].Evaluate()
