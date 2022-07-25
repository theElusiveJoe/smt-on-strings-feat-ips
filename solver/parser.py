import re
from .structures import *
from sys import argv


def split_to_pathernesses(whole_string):
    """Принимает строку. Возвращает список подстрок
    - содержимое скобочек нулевого уровня + сами скобочки"""
    counter = 0
    starts = []
    for i, ch in enumerate(whole_string):
        if ch == '(':
            counter += 1
            if counter == 1:
                starts.append(i)
        elif ch == ')':
            counter -= 1
    starts.append(len(whole_string))
    return [whole_string[starts[i]:starts[i+1]].strip() for i in range(len(starts)-1)]


def find_closing_parenthesis(long_str):
    counter = 0
    left_p = 0
    for i, x in enumerate(long_str):
        if x == '(':
            counter += 1
        elif x == ')':
            counter -= 1
            if counter == 0:
                return i+1


class Parser():
    def __init__(self, filepath):
        self.declared_variables = []

        self.clauses = []
        self.literals = []
        self.atoms = []
        self.strings = []

        self.filepath = filepath
        with open(self.filepath) as f:
            raw_strings = list(filter(lambda x: len(x.strip()) > 0 and x.strip()[
                               0] != ';', f.read().split('\n')))
            whole_string = re.sub('\s+', ' ', ''.join(raw_strings))
            self.raw_strings = split_to_pathernesses(whole_string)
        self.parse()

    def __str__(self):
        s = ''
        s += f'STRINGS({len(self.strings)}):\n'
        for x in self.strings:
            s += str(x)+'\n'
        s += f'ATOMS({len(self.atoms)}):\n'
        for x in self.atoms:
            s += str(x)+'\n'
        s += f'LITERALS({len(self.literals)}):\n'
        for x in self.literals:
            s += str(x)+'\n'
        s += f'CLAUSES({len(self.clauses)}):\n'
        for x in self.clauses:
            s += str(x)+'\n'
        return s

    def parse(self):
        for string in self.raw_strings:
            declare_match = re.match(
                r'\s*\(\s*declare-fun\s*(\S+)\s*\(\s*\) String\)\s*', string)
            if declare_match:
                name = declare_match.groups()[0]
                self.declared_variables.append(name)
                continue

            assert_match = re.match(r'\s*\(\s*assert\s*(.*)\s*\)\s*', string)
            if assert_match:
                print('parse assert:', string)
                clause = Clause(self.parse_literal(assert_match.groups()[0]))
                if clause not in self.clauses and clause and clause.literals and len(clause.literals) > 0:
                    self.clauses.append(clause)
                continue

            set_logic_match = re.match(r'\s*\(\s*set-logic (.*)\s*\)\s*', string)
            if set_logic_match:
                self.logic = set_logic_match.groups()[0]

        return self

    def parse_literal(self, term_expr):
        print('parse literal:', term_expr)
        or_match = re.match(r'\s*\(\s*or\s*(.*)\s*\)\s*', term_expr)
        if or_match:
            subterms = split_to_pathernesses(or_match.groups()[0])
            ret = []
            for subterm in subterms:
                new_literal = self.parse_literal(subterm)
                if new_literal:
                    ret.extend(new_literal)
            return ret

        not_match = re.match(r'\s*\(\s*not\s*(.*)\s*\)\s*', term_expr)
        if not_match:
            atom = self.parse_atom(not_match.groups()[0])
            if not atom:
                return
            literal = Literal(atom, True)
            if literal in self.literals:
                i = self.literals.index(literal)
                return[self.literals[i]]
            self.literals.append(literal)
            return [literal]

        atom = self.parse_atom(term_expr)
        if not atom:
            return
        literal = Literal(atom, False)
        if literal in self.literals:
            i = self.literals.index(literal)
            return[self.literals[i]]
        self.literals.append(literal)
        return [literal]

    def parse_atom(self, atom_expr):
        print('parse atom', atom_expr)

        eq_match = re.match(r'\s*\(\s*=\s*(.*)\s*\)\s*', atom_expr)
        if eq_match:
            string_of_strings = eq_match.groups()[0]
            my_strings = self.parse_many_strings(string_of_strings)
            atom = Atom('=', my_strings[0], my_strings[1])
            if atom in self.atoms:
                i = self.atoms.index(atom)
                return self.atoms[i]

            self.atoms.append(atom)
            return atom

        contains_match = re.match(
            r'\s*\(\s*str\.contains\s*(.*)\s*\)\s*', atom_expr)
        string_of_strings = contains_match.groups()[0]
        my_strings = self.parse_many_strings(string_of_strings)
        if my_strings[1].stype == 'const' and my_strings[1].cont == '':
            return
        atom = Atom('str.contains', my_strings[0], my_strings[1])
        if atom in self.atoms:
            i = self.atoms.index(atom)
            return self.atoms[i]

        self.atoms.append(atom)
        return atom

    def parse_many_strings(self, string_of_strings):
        string_of_strings = string_of_strings.strip()
        print('parse many strings:', string_of_strings)

        if string_of_strings.strip() == '':
            return []

        if string_of_strings.startswith('"'):
            second_quote = string_of_strings.index('"', 1)+1
            my_string = My_String(
                'const', cont=string_of_strings[1:second_quote-1])
            if my_string in self.strings:
                i = self.strings.index(my_string)
                ret = [self.strings[i]]
                ret.extend(self.parse_many_strings(
                    string_of_strings[second_quote:]))
                return ret

            self.strings.append(my_string)
            ret = [my_string]
            ret.extend(self.parse_many_strings(
                string_of_strings[second_quote:]))
            return ret

        if string_of_strings.startswith('('):
            closing_parenthesis_pos = find_closing_parenthesis(
                string_of_strings)
            ret = [self.parse_string(
                string_of_strings[:closing_parenthesis_pos])]
            ret.extend(self.parse_many_strings(
                string_of_strings[closing_parenthesis_pos:]))
            return ret

        if ' ' not in string_of_strings:
            my_string = My_String('variable', var_name=string_of_strings)
            if my_string in self.strings:
                i = self.strings.index(my_string)
                return [self.strings[i]]

            self.strings.append(my_string)
            return [my_string]
        first_space = string_of_strings.index(' ')
        my_string = My_String(
            'variable', var_name=string_of_strings[:first_space])
        if my_string in self.strings:
            i = self.strings.index(my_string)
            ret = [self.strings[i]]
            ret.extend(self.parse_many_strings(
                string_of_strings[first_space:]))
            return ret

        self.strings.append(my_string)
        ret = [my_string]
        ret.extend(self.parse_many_strings(string_of_strings[first_space:]))
        return ret

    def parse_string(self, string):
        print('PARSING STRING:', string)
        string = string.strip()

        concat_match = re.match(r'\(\s*str\.\+\+(.*)\)', string)
        if concat_match:
            strings_to_concat = self.parse_many_strings(
                concat_match.groups()[0])
            my_string = My_String(
                'str.++', concats_strs=strings_to_concat)
            print(my_string)
            if my_string in self.strings:
                i = self.strings.index(my_string)
                return self.strings[i]

            self.strings.append(my_string)
            return my_string

        replaceall_match = re.match(
            r'\(\s*str\.replace_all\s*(.*)\s*\)', string)
        if replaceall_match:
            many_strings = self.parse_many_strings(replaceall_match.groups()[0])
            for x in many_strings:
                print(x)
            my_string = My_String(
                'str.replace_all', replace_strs=self.parse_many_strings(replaceall_match.groups()[0]))
            if my_string in self.strings:
                i = self.strings.index(my_string)
                return self.strings[i]
            self.strings.append(my_string)
            return my_string

        replace_match = re.match(r'\(\s*str\.replace\s*(.*)\s*\)\s*', string)
        if replace_match:
            my_string = My_String(
                'str.replace', replace_strs=self.parse_many_strings(replace_match.groups()[0]))
            if my_string in self.strings:
                i = self.strings.index(my_string)
                return self.strings[i]
            self.strings.append(my_string)
            return my_string

    def to_formula(self):
        """
        Возвращает объект типа Formula,
        инициализированный рекурсивными копиями полей self 
        """
        return Formula(
            strings=deepcopy(self.strings),
            atoms=deepcopy(self.atoms),
            literals=deepcopy(self.literals),
            clauses=deepcopy(self.clauses),
            logic = self.logic if hasattr(self, 'logic') else None
        )
