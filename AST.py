from abc import ABC, abstractmethod


class Node(ABC):
    def __init__(self, value, children):
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

class Iden(Node):
    def Evaluate(self):
        return SymbolTable.getter(self.value)
    
class Block(Node):
    def Evaluate():
        pass

class Print(Node):
    def Evaluate(self):
        print(self.children.Evaluate())
        return
