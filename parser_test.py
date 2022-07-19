from parser import Parser
import os 
import re

os.chdir('./tests/parser/')
files = os.listdir()
for file in files:
    if re.match('test_.\.smt2', file):
        with open(file, 'r') as src:
            with open(f'result_{file}', 'w') as dst:
                dst.write(src.read())
                dst.write('\n\n---------------------\n\n')
                p = Parser(file)
                p.parse()
                dst.write(str(p))
