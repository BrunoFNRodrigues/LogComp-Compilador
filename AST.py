from abc import ABC, abstractmethod
from SymbolTable import SymbolTable

class Assembler():
    file = ""

    def write(string):
        with open(Assembler.file, "a") as f:
            f.write(string+"\n")

class Node(ABC):
    i = 0
    
    def __init__(self, value=0, children=[]):
        self.value = value
        self.children = children
        self.id = Node.newId()
        Node.i += 1

    @abstractmethod
    def Evaluate(self):
        None
        
    @staticmethod
    def newId():
        return Node.i 

class BinOp(Node):
    def Evaluate(self):
        id = str(self.id)
        self.children[1].Evaluate()
        Assembler.write("PUSH EBX ;")
        self.children[0].Evaluate()
        Assembler.write("POP EAX ;")
        
        if self.value == "==":
            Assembler.write("CMP EAX, EBX ;")
            Assembler.write("JE IGUAL"+id+" ;")
            Assembler.write("MOV EBX, 0 ;")
            Assembler.write("JMP FIM"+id+" ;")
            Assembler.write("IGUAL"+id+":")
            Assembler.write("MOV EBX, 1 ;")
            Assembler.write("FIM"+id+":")
            
        elif self.value == ">":
            Assembler.write("CMP EAX, EBX ;")
            Assembler.write("JG MAIOR"+id+" ;")
            Assembler.write("MOV EBX, 0 ;")
            Assembler.write("JMP FIM"+id+" ;")
            Assembler.write("MAIOR"+id+":")
            Assembler.write("MOV EBX, 1 ;")
            Assembler.write("FIM"+id+":")
            
        elif self.value == "<":
            Assembler.write("CMP EAX, EBX ;")
            Assembler.write("JL MENOR"+id+" ;")
            Assembler.write("MOV EBX, 0 ;")
            Assembler.write("JMP FIM"+id+" ;")
            Assembler.write("MENOR"+id+":")
            Assembler.write("MOV EBX, 1 ;")
            Assembler.write("FIM"+id+":")
            
        elif self.value == "||":
            Assembler.write("OR EAX, EBX ;")

        elif self.value == "&&":
            Assembler.write("AND EAX, EBX ;")
      
        elif self.value == "-":
            Assembler.write("SUB EAX, EBX ;")

        elif self.value == "+":
            Assembler.write("ADD EAX, EBX ;")

        elif self.value == "*":
            Assembler.write("IMUL EBX ;")

        elif self.value == "/":
            Assembler.write("DIV EBX ;")

        return None

        

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
        Assembler.write("MOV EBX, "+str(self.value)+" ;")
        return None
    

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
            print(self.children.Evaluate())

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
        