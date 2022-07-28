import context 
from solver.lia import Lia_Formula
from solver.parser import Parser

p = Parser('tests/lia_tests/test_5.smt2')
f = p.to_formula()
print(f)
lf = Lia_Formula(f)
print(lf)
print(lf.check_sat())