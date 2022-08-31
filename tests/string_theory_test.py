from solver.strings_theory import *
from solver.parser import Parser

p = Parser('tests/string_theory_tests/test_1.smt2')
f = p.to_formula()
cut(f)
print(f)
