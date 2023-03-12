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
        print("Token: Value:{} Type:{}".format(self.next.value, self.next.type))
        nums = ["0","1","2","3","4","5","6","7","8","9"]
        sym = ["+","-","/","*","(",")"]
        start_positon = self.position
        if start_positon == len(self.source):
            self.next = Token("EOF", 0)
            
        elif self.source[self.position] in nums:
            PARSING = 1
            while PARSING:
                if self.source[self.position] in sym:
                    value = self.source[start_positon:self.position]
                    if " " in value.strip():
                        raise Exception("Space between numbers")
                    else:
                        self.next = Token("INT", int(value.replace(" ", "")))
                        PARSING = 0
                else:
                    self.position += 1   
                    if self.position == len(self.source):
                        if " " in self.source[start_positon:self.position].strip():
                            raise Exception("Space between numbers")
                        else:
                            self.next = Token("INT", int(self.source[start_positon:self.position].replace(" ", "")))
                            PARSING = 0
                
        elif self.source[self.position] in sym:
            PARSING = 1
            while PARSING:
                if self.source[self.position] in nums:
                    sinal = self.source[start_positon:self.position].replace(" ", "")
                    if sinal == "-":
                        self.next = Token("NEG", -1)
                    elif sinal == "+":
                        self.next = Token("POS", 1)
                    elif sinal == "/":
                        self.next = Token("DIV", 1)
                    elif sinal == "*":
                        self.next = Token("MULT", 1)
                    elif sinal == "(":
                        self.next = Token("OP", 0)
                    elif sinal == ")":
                        self.next = Token("CP", 0)
                    PARSING = 0
                elif self.source[self.position+1] in sym:
                    sinal = self.source[start_positon:self.position+1]
                    if " " in sinal.strip():
                        raise Exception("Space between symbols")
                    else:
                        if sinal == "-":
                            self.next = Token("NEG", -1)
                        elif sinal == "+":
                            self.next = Token("POS", 1)
                        else:
                            raise Exception("Wrong symbol combination")
                        self.position += 1
                        PARSING = 0
                else:
                    self.position += 1
        else:
            self.position += 1

class Parser():
    tokenizer = None

    def parseFactor():
        if Parser.tokenizer.next.type != "CP":
            res = Parser.tokenizer.next.value
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "POS":
                res = Parser.parseFactor()
            elif Parser.tokenizer.next.type == "NEG":
                res = Parser.parseFactor * -1
            elif Parser.tokenizer.next.type == "CP":
                res = Parser.parseExpression 
            return res
        else:
            raise Exception("Valor inicial inválido")


    def parseTerm():
        res = Parser.parseFactor()
        while Parser.tokenizer.next.type == "MULT" or Parser.tokenizer.next.type == "DIV":
            if Parser.tokenizer.next.type == "MULT":
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type == "INT":
                    res *= Parser.tokenizer.next.value
                else:
                    raise Exception("Erro sintático: sinais consecutivos")    
            elif Parser.tokenizer.next.type == "DIV":
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type == "INT":
                    res /= Parser.tokenizer.next.value
                else:
                    raise Exception("Erro sintático: sinais consecutivos")  
            Parser.tokenizer.selectNext()
        return res
                    
    def parseExpression():
        Parser.tokenizer.selectNext()
        res = Parser.parseTerm()
        while Parser.tokenizer.next.type == "POS" or Parser.tokenizer.next.type == "NEG":
            if Parser.tokenizer.next.type == "POS":
                Parser.tokenizer.selectNext()
                res += Parser.parseTerm()
                  
            elif Parser.tokenizer.next.type == "NEG":
                Parser.tokenizer.selectNext()
                res -= Parser.parseTerm()

        return int(res)

    def run(code):
        line = comments(code)
        lexicon(line)
        Parser.tokenizer = Tokenizer(line,0,Token("INT", 0))
        return Parser.parseExpression()


def lexicon(arg):
    alfabeto = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "+", "*", "/", " ", "(", ")"]
    for i in arg:
        if i not in alfabeto:
            raise Exception("Invalid Argument")
        
def comments(arg):
    if "#" in arg:
        return arg[0:arg.index("#")]
    else:
        return arg

if __name__ == "__main__":
    #res = Parser.run(sys.argv[1])
    res = Parser.run("5+5")
    print(res)