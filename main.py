from solver.dpllt import check_sat
from solver.formula_generator import Generator
from solver.lia import Lia_Formula
from solver.parser import Parser
from solver.structures import *

g = Generator('generator_config.ini')
print(g)
check_sat(g.to_formula())