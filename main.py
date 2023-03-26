import sys
from AST import *
from Tokenizer import *
import string

class Parser():
    tokenizer = None
    stack = 0
    
    def parseBlock():
        Parser.tokenizer.selectNext()
        statements = []
        while Parser.tokenizer.next.type() in ["IDT", "LB", "PNT"]:
            statements.append(Parser.parseStatement)
            Parser.tokenizer.selectNext()
        return Block(children=statements)
    
    def parseStatement():
        if Parser.tokenizer.next.type == "LB":
            return NoOp()
        if Parser.tokenizer.next.type == "IDT":
            res = Identifier(Parser.tokenizer.next.value)
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "EQL":
                res = Assigment(res, Parser.parseExpression())
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type == "LB":
                    return res
        if Parser.tokenizer.next.type == "PNT":
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "OP":
                res = Print(children = Parser.parseExpression())    
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type == "CP":
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type == "LB":
                        return res
    def parseFactor():
        if Parser.tokenizer.next.type != "CP":
            if Parser.tokenizer.next.type == "INT":
                res = IntVal(Parser.tokenizer.next.value, [])
            elif Parser.tokenizer.next.type == "POS":
                Parser.tokenizer.selectNext()
                res = UnOp("+", Parser.parseFactor())
            elif Parser.tokenizer.next.type == "NEG":
                Parser.tokenizer.selectNext()
                res = UnOp("-", Parser.parseFactor())
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
                res = BinOp("*", [Parser.parseFactor(), res])
                   
            elif Parser.tokenizer.next.type == "DIV":
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type == "EOF":
                    raise Exception("* no fim")
                res = BinOp("/", [Parser.parseFactor(), res])

            Parser.tokenizer.selectNext()
        return res
                    
    def parseExpression():
        res = Parser.parseTerm()
        while Parser.tokenizer.next.type == "POS" or Parser.tokenizer.next.type == "NEG":
            if Parser.tokenizer.next.type == "POS":
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type == "EOF":
                    raise Exception("+ no fim")
                res = BinOp("+", [Parser.parseTerm(), res])
                
                  
            elif Parser.tokenizer.next.type == "NEG":
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type == "EOF":
                    raise Exception("- no fim")
                res = BinOp("-", [Parser.parseTerm(), res])
        
        return res

    def run(code):
        line = comments(code).strip()
        lexicon(line)
        Parser.tokenizer = Tokenizer(line,0,Token("INT", 0))
        res = Parser.parseBlock()
        # if Parser.stack != 0:
        #     raise Exception("Faltou parenteses")
        return res

def lexicon(arg):
    alfabeto = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "+", "*", "/", " ", "(", ")", "="] + string.ascii_letters
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
    with open(sys.argv[1], "r") as f: 
        res = Parser.run(f.read())
        res = res.Evaluate()