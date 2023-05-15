from Tokenizer import *
from main import comments




with open("testes/exemplo.jl", "r") as f: 
    line = comments(f.read())
    t = Tokenizer(line,0,Token("INT", 0))

    while t.next.type != "EOF":
        t.selectNext()
        print("Type: {} Value: {}".format(t.next.type, t.next.value))