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
            Assembler.write("CALL binop_je ;")
            
        elif self.value == ">":
            Assembler.write("CMP EAX, EBX ;")
            Assembler.write("CALL binop_jg ;")
            
        elif self.value == "<":
            Assembler.write("CMP EAX, EBX ;")
            Assembler.write("CALL binop_jl ;")
            
        elif self.value == "||":
            Assembler.write("OR EAX, EBX ;")
            Assembler.write("MOV EBX, EAX ;")

        elif self.value == "&&":
            Assembler.write("AND EAX, EBX ;")
            Assembler.write("MOV EBX, EAX ;")
      
        elif self.value == "-":
            Assembler.write("SUB EAX, EBX ;")
            Assembler.write("MOV EBX, EAX ;")

        elif self.value == "+":
            Assembler.write("ADD EAX, EBX ;")
            Assembler.write("MOV EBX, EAX ;")

        elif self.value == "*":
            Assembler.write("IMUL EBX ;")
            Assembler.write("MOV EBX, EAX ;")

        elif self.value == "/":
            Assembler.write("DIV EBX ;")
            Assembler.write("MOV EBX, EAX ;")
            
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
        Assembler.write("MOV EBX, [EBP-"+str(SymbolTable.table[self.value])+"] ;")
    
class Block(Node):
    def Evaluate(self):
        for child in self.children:
            child.Evaluate()

class Print(Node):
    def Evaluate(self):
        self.children.Evaluate()
        Assembler.write("PUSH EBX ;")
        Assembler.write("CALL print ;")
        Assembler.write("POP EBX ;")

class Assignment(Node):
    def Evaluate(self):
        key = self.children[0].value
        if key in SymbolTable.table.keys():
            self.children[1].Evaluate()
            Assembler.write("MOV [EBP-"+str(SymbolTable.table[key])+"], EBX;")
        else:
            Assembler.write("PUSH DWORD 0 ;")
            Desloc = max(SymbolTable.table.values()) + 4
            SymbolTable.table[self.children[0].value] = Desloc
    
class Read(Node):
    def Evaluate(self):
        return ("Int", int(input()))
    
class While(Node):
    def Evaluate(self):
        id = str(self.id)
        Assembler.write("LOOP_"+id+": ; ")
        self.children[1].Evaluate()
        Assembler.write("CMP EBX, False ;")
        Assembler.write("JE EXIT_"+id+" ; ")
        self.children[0].Evaluate()
        Assembler.write("JMP LOOP_"+id+" ;")
        Assembler.write("EXIT_"+id+":")
        

class If(Node):
    def Evaluate(self):
        id = str(self.id)
        Assembler.write("IF_"+id+": ; ")
        self.children[-1].Evaluate()
        Assembler.write("CMP EBX, False ;")
        Assembler.write("JE ELSE_"+id+" ; ")
        self.children[-2].Evaluate()
        Assembler.write("ELSE_"+id+":")
        if len(self.children) > 2:
            self.children[0].Evaluate()

class VarDec(Node):
    def Evaluate(self):
        Assembler.write("PUSH DWORD 0 ;")
        Desloc = max(SymbolTable.table.values()) + 4
        SymbolTable.table[self.children[0].value] = Desloc

        