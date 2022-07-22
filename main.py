from solver.dpllt import check_sat
from solver.formula_generator import Generator
# from solver.lia import Lia_Formula
from solver.parser import Parser
# from solver.structures import *

p = Parser('tests/dpllt_tests/test_1.smt2')
f = p.to_formula()
f.print_dpll_view()
print()
result = check_sat(f)
print(result)