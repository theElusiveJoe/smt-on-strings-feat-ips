import context 
from solver.dpllt import check_sat
from solver.parser import Parser
from subprocess import Popen, PIPE, STDOUT, run


p = Parser('tests/lia_tests/test_5.smt2')
f = p.to_formula()
f.print_dpll_view()
print('\n')
dot_strings = []
result = check_sat(f, dot_strings=dot_strings)
# for ds in dot_strings:
#     print(ds)
s = 'digraph G {\n    ' + '\n    '.join([ds for ds in dot_strings]) + '\n}}'
print(s)
print(result)
# with open('graph.svg', 'w+') as graph_file:
p = Popen(['dot', '-Tsvg', '-otests/dpllt_tests/graph.svg'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)    
p.communicate(input=bytes(s, encoding='utf8'))[0]
run(['display', 'tests/dpllt_tests/graph.svg'])
# print(r.stdout)
    # print(grep_stdout.decode())