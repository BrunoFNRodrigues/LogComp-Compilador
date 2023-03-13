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
                if self.position+1 == len(self.source):
                    sinal = self.source[self.position]
                    if sinal == "-":
                        self.next = Token("NEG", -1)
                    elif sinal == "+":
                        self.next = Token("POS", 1)
                    elif sinal == "/":
                        self.next = Token("DIV", 0)
                    elif sinal == "*":
                        self.next = Token("MULT", 0)
                    elif sinal == "(":
                        self.next = Token("OP", 0)
                        Parser.stack += 1
                    elif sinal == ")":
                        self.next = Token("CP", 0)
                        Parser.stack -= 1
                    PARSING = 0   
                elif self.source[self.position+1] in nums:
                    sinal = self.source[start_positon:self.position+1].replace(" ", "")
                    if sinal == "-":
                        self.next = Token("NEG", -1)
                    elif sinal == "+":
                        self.next = Token("POS", 1)
                    elif sinal == "/":
                        self.next = Token("DIV", 0)
                    elif sinal == "*":
                        self.next = Token("MULT", 0)
                    elif sinal == "(":
                        self.next = Token("OP", 0)
                        Parser.stack += 1
                    elif sinal == ")":
                        self.next = Token("CP", 0)
                        Parser.stack -= 1
                    PARSING = 0
                elif self.source[self.position+1] in sym:
                    sinal = self.source[start_positon:self.position+1]
                    sinal2 = self.source[start_positon:self.position+2]
                    if " " in sinal2 and (not "(" in sinal2) and (not ")" in sinal2) and start_positon != 0:
                        raise Exception("Space between symbols")
                    elif (sinal2[0] == "*" or sinal2[0] == "/") and (sinal2[-1] == "*" or sinal2[-1] == "/"):
                        raise Exception("Too Many symbols")
                    
                    sinal = sinal.replace(" ", "")
                    if sinal == "-":
                        self.next = Token("NEG", -1)
                    elif sinal == "+":
                        self.next = Token("POS", 1)
                    elif sinal == "/":
                        self.next = Token("DIV", 0)
                    elif sinal == "*":
                        self.next = Token("MULT", 0)
                    elif sinal == "(":
                        self.next = Token("OP", 0)
                        Parser.stack += 1
                    elif sinal == ")":
                        self.next = Token("CP", 0)
                        Parser.stack -= 1
                    else:
                        raise Exception("Wrong symbol combination")
                    PARSING = 0

                self.position += 1 
        else:
            self.position += 1
        #print("Type: {} Value: {}".format(self.next.type, self.next.value))

class Parser():
    tokenizer = None
    stack = 0
    
    def parseFactor():
        if Parser.tokenizer.next.type != "CP":
            res = Parser.tokenizer.next.value
            if Parser.tokenizer.next.type == "POS":
                Parser.tokenizer.selectNext()
                res *= Parser.parseFactor()
            elif Parser.tokenizer.next.type == "NEG":
                Parser.tokenizer.selectNext()
                res *= Parser.parseFactor()
            elif Parser.tokenizer.next.type == "OP":
                res = Parser.parseExpression()
                if Parser.tokenizer.next.type != "CP":
                    raise Exception("Faltou fechar")
            return res
        else:
            raise Exception("CP No lugar errado")


    def parseTerm():
        res = Parser.parseFactor()
        Parser.tokenizer.selectNext()
        while Parser.tokenizer.next.type == "MULT" or Parser.tokenizer.next.type == "DIV":
            if Parser.tokenizer.next.type == "MULT":
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type == "EOF":
                    raise Exception("* no fim")
                res *= Parser.parseFactor()
                   
            elif Parser.tokenizer.next.type == "DIV":
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type == "EOF":
                    raise Exception("* no fim")
                res /= Parser.parseFactor()
                
            Parser.tokenizer.selectNext()
        return res
                    
    def parseExpression():
        Parser.tokenizer.selectNext()
        res = Parser.parseTerm()
        while Parser.tokenizer.next.type == "POS" or Parser.tokenizer.next.type == "NEG":
            if Parser.tokenizer.next.type == "POS":
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type == "EOF":
                    raise Exception("+ no fim")
                res += Parser.parseTerm()
                
                  
            elif Parser.tokenizer.next.type == "NEG":
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type == "EOF":
                    raise Exception("- no fim")
                res -= Parser.parseTerm()
        
        if Parser.stack != 0:
            raise Exception("Faltou parenteses")
        
        return int(res)

    def run(code):
        line = comments(code).strip()
        lexicon(line)
        Parser.tokenizer = Tokenizer(line,0,Token("INT", 0))
        return Parser.parseExpression()


def lexicon(arg):
    alfabeto = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "+", "*", "/", " ", "(", ")"]
    if len(arg) == 0:
        raise Exception("No Argument")
    for i in arg:
        if i not in alfabeto:
            raise Exception("Invalid Argument")
        
def comments(arg):
    if "#" in arg:
        return arg[0:arg.index("#")]
    else:
        return arg

if __name__ == "__main__":
    res = Parser.run(sys.argv[1])
    #res = Parser.run("100 + 100")
    print(res)