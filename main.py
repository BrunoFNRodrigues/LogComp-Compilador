import sys
from AST import *
from Tokenizer import *
import string
from SymbolTable import *

class Parser():
    tokenizer = None
    stack = 0
    
    def parseMainBlock():
        Parser.tokenizer.selectNext()
        statements = []
        while Parser.tokenizer.next.type != "EOF":
            statements.append(Parser.parseStatement())
            Parser.tokenizer.selectNext()
        return Block(children=statements)
    
    def parseBlock():
        Parser.tokenizer.selectNext()
        statements = []
        while Parser.tokenizer.next.type in ["IDT", "LB", "PNT", "WHL", "IF", "RET", "FUNC"]:
            statements.append(Parser.parseStatement())
            Parser.tokenizer.selectNext()
        return Block(children=statements)
    
    def parseStatement():
        if Parser.tokenizer.next.type == "LB":
            return NoOp()
        elif Parser.tokenizer.next.type == "IDT":
            res = Identifier(Parser.tokenizer.next.value)
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "EQL":
                Parser.tokenizer.selectNext()
                res = Assignment(children=[res, Parser.parseRelExpression()])
                if Parser.tokenizer.next.type == "LB":
                    return res
            elif Parser.tokenizer.next.type == "TYPO":
                Parser.tokenizer.selectNext()
                t =  Parser.tokenizer.next.value
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type == "EQL":
                    Parser.tokenizer.selectNext()
                    res = VarDec(t, [res, Parser.parseRelExpression()])
                    if  Parser.tokenizer.next.type == "LB":
                        return res                    
                elif Parser.tokenizer.next.type == "LB":
                    res = VarDec(t, [res])
                    return res
            elif Parser.tokenizer.next.type == "OP":
                Parser.tokenizer.selectNext()
                args = [res]
                if Parser.tokenizer.next.type != "CP":
                    args.append(Parser.parseRelExpression())
                    while Parser.tokenizer.next.type == "COMA":
                        Parser.tokenizer.selectNext()
                        args.append(Parser.parseRelExpression())
                res = FuncCall(args[0], args[1:])
                if  Parser.tokenizer.next.type == "CP":
                    Parser.tokenizer.selectNext()
                    if  Parser.tokenizer.next.type == "LB":
                        return res 
                         
        elif Parser.tokenizer.next.type == "PNT":
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "OP":
                Parser.tokenizer.selectNext()
                res = Print(children = Parser.parseRelExpression())    
                if Parser.tokenizer.next.type == "CP":
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type == "LB":
                        return res
                    
        elif Parser.tokenizer.next.type == "WHL":
            Parser.tokenizer.selectNext()
            res = Parser.parseRelExpression()
            if Parser.tokenizer.next.type == "LB":
                res = While("while", [Parser.parseBlock(), res])
                if Parser.tokenizer.next.type == "END":
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type == "LB":
                        return res
                    
        elif Parser.tokenizer.next.type == "IF":
            Parser.tokenizer.selectNext()
            res = Parser.parseRelExpression()
            if Parser.tokenizer.next.type == "LB":
                block1 = Parser.parseBlock()
                if Parser.tokenizer.next.type == "END":
                    Parser.tokenizer.selectNext()
                    res = If("If", [block1, res])
                if Parser.tokenizer.next.type == "ELSE":
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type == "LB":
                        block2 = Parser.parseBlock()
                        res = If("If", [block2, block1, res])
                        if Parser.tokenizer.next.type == "END":
                            Parser.tokenizer.selectNext()
                        else:
                            raise Exception("Else problem")
                        
                if Parser.tokenizer.next.type == "LB":
                    return res    
        
        elif Parser.tokenizer.next.type == "RET":
            Parser.tokenizer.selectNext()
            res = Return(children=Parser.parseRelExpression())
            if Parser.tokenizer.next.type == "LB":
                return res
            
        elif Parser.tokenizer.next.type == "FUNC":
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "IDT":
                iden  = Identifier(Parser.tokenizer.next.value)
                args = []
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type == "OP":
                    while Parser.tokenizer.next.type != "CP":
                        Parser.tokenizer.selectNext()
                        if Parser.tokenizer.next.type == "IDT":
                            res = Identifier(Parser.tokenizer.next.value)
                            Parser.tokenizer.selectNext()
                            if Parser.tokenizer.next.type == "TYPO":
                                Parser.tokenizer.selectNext()
                                t =  Parser.tokenizer.next.value
                                args.append(VarDec(t, [res]))
                                Parser.tokenizer.selectNext()
                                if not Parser.tokenizer.next.type in ["COMA", "CP"]:
                                    raise Exception("Declarou errado a func")
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type == "TYPO":
                        Parser.tokenizer.selectNext()
                        t =  Parser.tokenizer.next.value
                        Parser.tokenizer.selectNext()
                        if Parser.tokenizer.next.type == "LB":
                            res = FuncDec(t, [iden, args, Parser.parseBlock()])
                            if Parser.tokenizer.next.type == "END":
                                Parser.tokenizer.selectNext()
                                if Parser.tokenizer.next.type == "LB":
                                    return res   
        
        else:
            raise Exception("Bad Statement: "+ Parser.tokenizer.next.type + " " + str(Parser.tokenizer.next.value))
                        
    def parseFactor():
        if Parser.tokenizer.next.type != "CP":
            res = 0
            if Parser.tokenizer.next.type == "INT":
                res = IntVal(Parser.tokenizer.next.value, [])
                Parser.tokenizer.selectNext()
            elif Parser.tokenizer.next.type == "IDT":
                res = Identifier(Parser.tokenizer.next.value)
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type == "OP":
                    Parser.tokenizer.selectNext()
                    args = [res]
                    if Parser.tokenizer.next.type != "CP":
                        args.append(Parser.parseRelExpression())
                        while Parser.tokenizer.next.type == "COMA":
                            Parser.tokenizer.selectNext()
                            args.append(Parser.parseRelExpression())
                    if  Parser.tokenizer.next.type == "CP":
                        Parser.tokenizer.selectNext()
                        res = FuncCall(args[0], args[1:])                
            elif Parser.tokenizer.next.type == "POS":
                Parser.tokenizer.selectNext()
                res = UnOp("+", Parser.parseFactor())
            elif Parser.tokenizer.next.type == "NEG":
                Parser.tokenizer.selectNext()
                res = UnOp("-", Parser.parseFactor())
            elif Parser.tokenizer.next.type == "FTR":
                Parser.tokenizer.selectNext()
                res = UnOp("!", Parser.parseFactor())  
            elif Parser.tokenizer.next.type == "OP":
                Parser.tokenizer.selectNext()
                res = Parser.parseRelExpression()
                if Parser.tokenizer.next.type != "CP":
                    raise Exception("Faltou fechar")
                Parser.tokenizer.selectNext()
            elif Parser.tokenizer.next.type == "RD":
                res = Read()
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type == "OP":
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type != "CP":
                        raise Exception("Faltou fechar parenteses")
                    Parser.tokenizer.selectNext()
            elif Parser.tokenizer.next.type == "COT":
                Parser.tokenizer.selectNext()
                res = StringVal(Parser.tokenizer.next.value, [])
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type != "COT":
                    raise Exception("Faltou fechar aspas")
                Parser.tokenizer.selectNext()

            return res
        else:
            raise Exception("CP No lugar errado")

    def parseTerm():
        res = Parser.parseFactor()
        while Parser.tokenizer.next.type == "MULT" or Parser.tokenizer.next.type == "DIV" or Parser.tokenizer.next.type == "AND":
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

            elif Parser.tokenizer.next.type == "AND":
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type == "EOF":
                    raise Exception("&& no fim")
                res = BinOp("&&", [Parser.parseFactor(), res])
                
        return res
                    
    def parseExpression():
        res = Parser.parseTerm()
        while Parser.tokenizer.next.type == "POS" or Parser.tokenizer.next.type == "NEG" or Parser.tokenizer.next.type == "OR":
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
                
            elif Parser.tokenizer.next.type == "OR":
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type == "EOF":
                    raise Exception("|| no fim")
                res = BinOp("||", [Parser.parseTerm(), res])            
        
        return res

    def parseRelExpression():
        res = Parser.parseExpression()
        while Parser.tokenizer.next.type == "SEQL" or Parser.tokenizer.next.type == "GRT" or Parser.tokenizer.next.type == "LST" or Parser.tokenizer.next.type == "CONCAT":
            if Parser.tokenizer.next.type == "SEQL":
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type == "EOF":
                    raise Exception("== no fim")
                res = BinOp("==", [Parser.parseExpression(), res])
                
                  
            elif Parser.tokenizer.next.type == "GRT":
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type == "EOF":
                    raise Exception("> no fim")
                res = BinOp(">", [Parser.parseExpression(), res])
                
            elif Parser.tokenizer.next.type == "LST":
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type == "EOF":
                    raise Exception("< no fim")
                res = BinOp("<", [Parser.parseExpression(), res])
                
            elif Parser.tokenizer.next.type == "CONCAT":
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type == "EOF":
                    raise Exception(". no fim")
                res = ConcatOp(".", [Parser.parseExpression(), res])
        return res


    def run(code):
        line = comments(code).lstrip()
        lexicon(line)
        Parser.tokenizer = Tokenizer(line,0,Token("INT", 0))
        res = Parser.parseMainBlock()
        return res

def lexicon(arg):
    alfabeto = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "+", "*", "/", " ", "(", ")", "=", "\n", "_", "|", "&", "<", ">", "!", ".", ":", '"', ","] + list(string.ascii_letters)
    if len(arg) == 0:
        raise Exception("No Argument")
    for i in arg:
        if i not in alfabeto:
            raise Exception(i,"Invalid Argument")
        
def comments(arg):
    pos = 0
    s_pos = 0
    CMT = 0
    while "#" in arg:
        if arg[pos] == "#":
            s_pos = pos
            CMT = 1
            
        if arg[pos:pos+1] == "\n" and CMT:
            a = arg[s_pos:pos]
            arg = arg.replace(a, "")
            CMT = 0
        pos += 1
        
    return arg

if __name__ == "__main__":
    with open(sys.argv[1], "r") as f: 
        res = Parser.run(f.read())
        res = res.Evaluate(SymbolTable())
