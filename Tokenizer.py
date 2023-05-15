import string

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
        sym = {"+":"POS", "-":"NEG", "/":"DIV", 
               "*":"MULT", "(":"OP", ")":"CP", ",":"COMA",
               "||":"OR", "&&":"AND", "=": "EQL", "==":"SEQL",
               ">":"GRT", "<":"LST", "!" : "FTR", ".":"CONCAT", "::":"TYPO", '"':"COT"}
        reserved = {"println":"PNT", "readline":"RD", "while":"WHL", "if":"IF", "else":"ELSE", "end":"END", "String":"STR",
                     "Int":"INT", "function":"FUNC", "return":"RET"}
        letters= list(string.ascii_letters)
        start_positon = self.position
        if start_positon == len(self.source):
            self.next = Token("EOF", 0)
            
        elif self.source[self.position] in nums:
            PARSING = 1
            while PARSING:
                if self.source[self.position] in list(sym.keys()) or self.source[self.position:self.position+1] == "\n":
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
           
        elif self.source[self.position:self.position+2] in list(sym.keys()):
            if not " " in self.source[start_positon:self.position+2]:
                self.next = Token(sym[self.source[self.position:self.position+2]], self.source[self.position:self.position+2])
                self.position += 2
                PARSING = 0
                         
        elif self.source[self.position] in list(sym.keys()):
            PARSING = 1
            while PARSING:        
                if self.source[self.position+1] in nums+letters+["\n", " ", ":"]:
                    sinal = self.source[start_positon:self.position+1].replace(" ", "")
                    self.next = Token(sym[sinal], sinal)
                    PARSING = 0
                
       
                elif self.source[self.position+1] in list(sym.keys())+letters:
                    sinal = self.source[start_positon:self.position+1]
                    sinal2 = self.source[start_positon:self.position+2]
                    if " " in sinal2 and (not "(" in sinal2) and (not ")" in sinal2) and start_positon != 0:
                        raise Exception("Space between symbols")
                    elif (sinal2[0] == "*" or sinal2[0] == "/") and (sinal2[-1] == "*" or sinal2[-1] == "/"):
                        raise Exception("Too Many symbols")

                    else:                   
                        sinal = sinal.replace(" ", "")
                        self.next = Token(sym[sinal], sinal)

                        PARSING = 0
                    


                self.position += 1 
        
        elif self.source[self.position] in letters:
            PARSING = 1
            while PARSING:
                self.position += 1
                if self.source[self.position] in list(sym.keys())+[" "] or self.source[self.position:self.position+1] == "\n" or self.source[self.position:self.position+2] in list(sym.keys()):
                    value = self.source[start_positon:self.position].strip()
                    if " " in value:
                        raise Exception("Variavel invalida")
                    self.next = Token("IDT", value)

                    if value in reserved.keys():
                        self.next = Token(reserved[value], value)

                    PARSING = 0 
           
                elif self.source[self.position:self.position+2] in list(sym.keys()):
                    if not " " in self.source[start_positon:self.position+2]:
                        self.next = Token(sym[self.source[self.position:self.position+2]], self.source[self.position:self.position+2])
                        self.position += 1
                        PARSING = 0 
             
        elif self.source[self.position:self.position+1] == "\n":
            PARSING = 1
            if self.position+1 >= len(self.source):
                value = self.source[self.position]
                self.next = Token("LB", value.strip())
                PARSING = 0 
                self.position += 1
                
            while PARSING:                    
                if self.source[self.position] in letters+["\n"]:
                    value = self.source[start_positon:self.position]
                    if " " in value.strip():
                        raise Exception("Variavel invalida")
                    self.next = Token("LB", value.strip())
                    PARSING = 0 
                self.position += 1

        else:
            self.position += 1
            self.selectNext()
            
        

