from abc import ABC, abstractmethod
from SymbolTable import SymbolTable

class Node(ABC):
    def __init__(self, value=None, children=None):
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
        return self.children[1].Evaluate()/self.children[0].Evaluate()

class UnOp(Node):
    def Evaluate(self):
        if self.value == "-":
            return -self.children[0].Evaluate()
        return self.children[0].Evaluate()
        
class IntVal(Node):
    def Evaluate(self):
        return self.value
    
class NoOp(Node):
    def Evaluate():
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
        print(self.children.Evaluate())

class Assigment(Node):
    def Evaluate(self):
        SymbolTable.Setter(self.children[0].value, self.children[1].Evaluete())
    