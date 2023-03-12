from main import Parser
import unittest

def test_1():
    res = Parser.run(" (3 + 2) /5")
    assert res == 1 

def test_2():
    res = Parser.run("+--++3")
    assert res == 3

def test_3():
    res = Parser.run("4/(1+1)*2")
    assert res == 4
    
def test_4():
    res = Parser.run("1+2")
    assert res == 3

def test_5():
    res = Parser.run("3-2")
    assert res == 1

def test_6():
    res = Parser.run("1+2-3")
    assert res == 0

def test_7():
    res = Parser.run("11+22-33")
    assert res == 0

def test_8():
    res = Parser.run("789      +345    -     123")
    assert res == 1011

def test_9():
    res = Parser.run("4/2+3")
    assert res == 5







