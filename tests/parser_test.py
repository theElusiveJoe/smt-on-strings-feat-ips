import context
from solver.parser import Parser
import sys
import os 
import re

os.chdir('tests/parser_tests')
files = os.listdir()
for file in files:
    if re.match('test_(.)*\.smt2', file):
        with open(file, 'r') as src:
            with open(f'result_{file}', 'w') as dst:
                dst.write(src.read())
                dst.write('\n\n---------------------\n\n')
                try:
                    p = Parser(file)
                except:
                    dst.write('Найдена ошибка в исходном файле')    
                else:
                    dst.write(str(p))
