import sys
import re

class Token():
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Tokenizer():
    def __init__(self, source, position, next):
        self.source = source
        self.position = position
        self.next = next

    def selectNext(self):
        l = self.source.replace(" ", "")
        num = re.split("[+-]", l)
        sin = re.split("[0123456789]", l)
        sin = [x for x in sin if x != '']
        if (self.position)%2:
            if sin[int(self.position/2//1)] == "-":
                self.next = Token("NEG", -1)
            else:
                self.next = Token("POS", 1)
        else:
            self.next = Token("INT",int(num[int(self.position/2)]))
        self.position += 1
        if (self.position >= len(num)+len(sin)):
            self.position = -1 
            return


class Parser():
    tokenizer = None

    def parseExpression():
        # Da erro sintatico
        a = Parser.tokenizer.next.value

        while Parser.tokenizer.position > 0:
            Parser.tokenizer.selectNext()
            sinal = Parser.tokenizer.next.value
            Parser.tokenizer.selectNext()
            b =  Parser.tokenizer.next.value
            a = a + b*sinal
        return a

    
    def run(code):
        lexico(code)
        sintatico(code)
        Parser.tokenizer = Tokenizer(code,1,Token("INT", int(re.split("[+-]", code.replace(" ", ""))[0])))
        return Parser.parseExpression()


def lexico(arg):
    alfabeto = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "+", " "]
    for i in arg:
        if i not in alfabeto:
            raise Exception("Invalid Argument")

def sintatico(arg):   
    if arg.strip()[0] == "+" or arg.strip()[0] == "-":
        raise Exception("Invalid starter character")

    if arg.strip()[-1] == "+" or arg.strip()[-1] == "-":
        raise Exception("Invalid end character")

    l = re.split("[+-]", arg)
    for i in l:
        if " " in i.strip():
            raise Exception("Space between numbers")

if __name__ == "__main__":
    res = Parser.run(sys.argv[1])
    print(res)