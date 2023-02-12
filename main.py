import sys
import re

class Compiler():
    def __init__(self) -> None:
        pass


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

    def calculadora(arg):
        Compiler.lexico(arg)
        Compiler.sintatico(arg)
        l = arg.replace(" ", "")
        num = re.split("[+-]", l)
        sin = re.split("[0123456789]", l)
        sin = [x for x in sin if x != '']

        i = 1
        res = int(num[0])
        while i < len(num):
            if sin[i-1] == "-":
                res -= int(num[i])
            else:
                res += int(num[i])
            i+=1

        return res

if __name__ == "__main__":
    res = Compiler.calculadora(sys.argv[1])
    print(res)