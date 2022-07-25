import subprocess
from .structures import *

def generate_ints():
    for i in  ['Pineapple', 'Cherry', 'Avocado', 'Orange', 'Peach', 'Pineberry',
                       'Tamarind', 'Yuzu', 'Lemon', 'Jackfruit', 'Coconut', 'Kumquat', 'Apricot',
                       'Banana', 'Cucumber', 'Fig', 'Pear', 'Blackberry', 'Lime', 'Soursop',
                       'Watermelon', 'Raspberry', 'Barsik', 'Papaya', 'Guava', 'Mango', 'Kiwi',
                       'Passionfruit', 'Durian', 'Grape', 'Starfruit', 'Strawberry', 'Quince',
                       'Dragonfruit', 'Blueberry', 'Mulberry', 'Gooseberry', 'Plum', 'Apple', 'Persimmon']:
        yield i
    
    i = -1
    while True:
        i+=1
        yield f'var_name_{i}'

class Lia_Formula():
    """
    self.variables нужен для удобного состаления ассертов
    self.atom_to_lia и self.string_to_lia - для мемоизации
    и получения интерпретации в рамках теории lia
    """

    # почему мемоизация пишется без буквы "р"?...

    def __init__(self, formula: Formula):
        self.formula = formula

        self.varnames_generator = generate_ints()

        self.atom_to_lia = {}
        self.string_to_lia = {}
        self.variables = []

        for atom in self.formula.atoms:
            if atom not in self.atom_to_lia:
                self.atom_interpretation_in_lia(atom)

    def __str__(self):
        s = '###LIA_FORMULA###\n'
        s += 'FAKE STRINGS:\n    '
        s += ''.join([f'\n    {y} <- {x}' if 'str.re' in x.stype else '' for x,
                     y in self.string_to_lia.items()])
        s += '\nATOMS:\n    '
        s += '\n    '.join([f'{y} <- {x}' for x,
                           y in self.atom_to_lia.items()])
        s += '\n\n'
        return s

    def atom_interpretation_in_lia(self, atom: Atom):
        if atom in self.atom_to_lia:
            return

        sign = {'=': '=', 'str.contains': '>='}[atom.ltype]
        lia_string1 = self.string_interpretation_in_lia(atom.my_string1)
        lia_string2 = self.string_interpretation_in_lia(atom.my_string2)
        self.atom_to_lia[atom] = f'({sign} {lia_string1} {lia_string2})'

    def string_interpretation_in_lia(self, my_string: My_String):
        """
        возвращает строковую интерпретацию объекта типа My_String в рамках lia,
        а также рекурсивно строит эти интерпретации для вложенных My_String`ов
        """
        if my_string in self.string_to_lia:
            return self.string_to_lia[my_string]

        if my_string.stype == 'const':
            self.string_to_lia[my_string] = str(len(my_string.cont))
            return str(len(my_string.cont))

        if my_string.stype == 'str.++':
            s = f'(+ {" ".join([self.string_interpretation_in_lia(x) for x in my_string.concats_strs])})'
            self.string_to_lia[my_string] = s
            return s

        if my_string.stype == 'variable':
            self.variables.append(my_string.var_name)
            self.string_to_lia[my_string] = my_string.var_name
            return my_string.var_name

        name = next(self.varnames_generator)
        for mss in my_string.replace_strs:
            self.string_interpretation_in_lia(mss)
        self.string_to_lia[my_string] = name
        self.variables.append(name)
        return name

    def clause_interpretation_in_lia(self, clause: Clause):
        literals_interpretations = [self.literal_interpretation_in_lia(
            literal) for literal in clause.literals]
        literals_interpretations = list(filter(None, literals_interpretations))
        if not literals_interpretations:
            return
        t = f'(or {" ". join(literals_interpretations)})'
        return f'{t}'

    def literal_interpretation_in_lia(self, literal: Literal):
        if literal.negation:
            return 
            # return f'(not {self.atom_to_lia[literal.atom]})'
        return self.atom_to_lia[literal.atom]

    def check_sat(self):
        smt2_strings = ['(set-logic QF_LIA)']
        for var_name in self.variables:
            smt2_strings.append(f'(declare-fun {var_name} () Int)')
            smt2_strings.append(f'(assert (>= {var_name} 0))')
        # for x, y in self.string_to_lia.items():
            # if x.stype == 'str.replace' or x.stype == 'str.replace_all':
            # smt2_strings.append(f'(assert (= {y} {x}))')
        # smt2_strings.append(';------------------')

        for clause in self.formula.clauses:
            clause_interpret = self.clause_interpretation_in_lia(clause)
            if clause_interpret:
                smt2_strings.append(
                    f'(assert {clause_interpret})')
        # smt2_strings.append(';------------------')
        smt2_strings.append('(check-sat)')
        # smt2_strings.append('(get-model)')

        temp = 'temp.smt2'
        try:
            with open(temp, 'w+') as f:
                for s in smt2_strings:
                    f.write(s+'\n')
        except:
            raise Exception('Ошибка при создании/открытии временного файла')

        return not 'unsat' in str(subprocess.check_output(['z3', '-smt2', temp]), encoding='utf-8')
