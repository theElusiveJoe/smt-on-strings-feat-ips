from copy import deepcopy


class My_String():
    """
    stype - один из:
    'const' , 'variable', 'str.++' , 'str.replace', 'str.replace_all'
    """

    def __init__(self, stype, cont=None, var_name=None, concats_strs=None, replace_strs=None):
        if stype not in ['const' , 'variable', 'str.++' , 'str.replace', 'str.replace_all']:
            raise Exception(f'Указан неверный stype при создании My_String: {stype}')
        self.stype = stype
        self.cont = cont
        self.var_name = var_name
        self.concats_strs = concats_strs
        self.replace_strs = replace_strs

    def __str__(self):
        if self.cont:
            # s = f'"{self.cont}"'
            return f'"{self.cont}"'
        elif self.var_name:
            # s = f'<{self.var_name}>'
            return self.var_name
        elif self.concats_strs:
            s = 'str.++'
            for cs in self.concats_strs:
                s += ' ' + str(cs)
        else:
            s = self.stype
            for cs in self.replace_strs:
                s += ' ' + str(cs)
        return f'[{s}]'

    def __eq__(self, o):
        if self.stype != o.stype:
            return False

        if self.cont:
            return self.cont == o.cont

        if self.var_name:
            return self.var_name == o.var_name

        if self.stype == 'str.++':
            return self.concats_strs == o.concats_strs

        return self.replace_strs == o.replace_strs

    def __hash__(self):
        return len(self.__str__())


class Atom():
    """
    ltype - один из:
    '=', 'str.contains'
    """
    def __init__(self, ltype, my_string1, my_string2):
        if ltype not in ['=', 'str.contains']:
            raise Exception(f'Указан неверный ltype при создании Atom: {ltype}')
        self.ltype = ltype
        self.my_string1 = my_string1
        self.my_string2 = my_string2

    def __str__(self):
        return f'({self.ltype} {str(self.my_string1)} {str(self.my_string2)})'

    def __eq__(self, o):
        return self.ltype == o.ltype and self.my_string1 == o.my_string1 and self.my_string2 == o.my_string2

    def __hash__(self):
        return len(self.__str__())

class Literal():
    def __init__(self, atom, negation, decisive=False):
        self.atom = atom
        self.negation = negation
        self.decisive = decisive

    def __str__(self):
        return f'{"(not " if self.negation else ""}{str(self.atom)}{")" if self.negation else ""}'

    def __eq__(self, o):
        return self.negation == o.negation and self.atom == o.atom

    def get_conjugate(self, decisive=False):
        """Возвращает объект сопряженного литерала"""
        return Literal(self.atom, not self.negation, decisive=decisive)

    def get_copy(self, decisive=False):
        """Возвращает объект-копию литерала"""
        return Literal(self.atom, self.negation, decisive=decisive)


class Clause():
    def __init__(self, literals):
        self.literals = literals

    def __str__(self):
        s = '(or\n'
        for lw in self.literals:
            s += f'    {str(lw)}\n'
        s += '  )\n'
        return s

    def __eq__(self, o):
        for x in self.literals:
            if x not in o.literals:
                return False
        for x in o.literals:
            if x not in self.literals:
                return False
        return True


class Formula():
    def __init__(self, **kwargs):
        """
        либо без аргументов,
        либо {
            strings: [],
            atoms: [],
            literals: [],
            clauses: []
        }
        """
        if not kwargs:
            return
        self.strings = kwargs['strings']
        self.atoms = kwargs['atoms']
        self.literals = kwargs['literals']
        self.clauses = kwargs['clauses']

    def __str__(self):
        try:
            s = '\n###FORMULA:###\n'
            s += 'STRINGS:\n'
            for x in self.strings:
                s += '  ' + str(x)+'\n'
            s += 'ATOMS:\n'
            for x in self.atoms:
                s += '  ' + str(x)+'\n'
            s += 'LITERALS:\n'
            for x in self.literals:
                s += '  ' + str(x)+'\n'
            s += 'CLAUSES:\n'
            for x in self.clauses:
                s += '  ' + str(x)+'\n'
            return s
        except:
            return "ПУСТАЯ ФОРМУЛА"

    def copy(self):
        return deepcopy(self)

    def extend_clauses(self, m):
        cop = self.copy()
        for lm in m:
            literal = deepcopy(lm)
            ext_clause = Clause([literal.get_conjugate()])
            cop.clauses.append(ext_clause)

        return cop