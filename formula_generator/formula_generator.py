import sys
sys.path.insert(0, sys.path[0] + '/..')
from copy import deepcopy
import random
import configparser
from alphabet_strings import *
from structures import *


def randbool(prob=0.5):
    return random.random() < prob


class Generator():

    def __init__(self, config_file):
        co = configparser.ConfigParser()
        co.read(config_file)

        parse_keys = {
            'constants': ['constant_min_len', 'constant_max_len'],
            'variables': ['variables_number_low_limit', 'variables_number_high_limit'],
            'strings': ['max_string_depth', 'max_concat_number'],
            'atoms': ['atoms_number_low_limit', 'atoms_number_high_limit'],
            'asserts': ['asserts_number', 'literals_in_assert_low_limit', 'literals_in_assert_high_limit']
        }
        self.config = {}
        for group, group_params in parse_keys.items():
            for param in group_params:
                self.config[param] = co.getint(group, param)

        self.alphabeth = globals()[co.get('constants', 'alphabeth')]

    def __str__(self):
        s = '\n###FORMULA:###\n'
        s += 'STRINGS:\n'
        for x in self.variables + self.constants + self.strings:
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
        
    def generate(self):
        self.variables = []
        self.constants = []
        self.strings = []
        self.atoms = []
        self.literals = []
        self.clauses = []

        # 1 создаем объекты строк-переменных
        name = ord('z')
        for _ in range(random.randint(
                self.config['variables_number_low_limit'], self.config['variables_number_high_limit'])):
            self.variables.append(
                My_String('variable', var_name=chr(name)))
            name -= 1

        # 2 генерим определенное количество атомов
        atoms_num = random.randint(
            self.config['atoms_number_low_limit'], self.config['atoms_number_high_limit'])
        for _ in range(atoms_num):
            self.gen_atom()

        # 3 теперь можно собирать ассеры из атомов
        self.shaker_index = 0
        for _ in range(self.config['asserts_number']):
            self.gen_assert()

    def gen_assert(self):
        literals = []
        literals_num = random.randint(
            self.config['literals_in_assert_low_limit'], self.config['literals_in_assert_high_limit'])
        for _ in range(literals_num):
            literals.append(self.gen_literal())

        assrt = Clause(literals)
        self.clauses.append(assrt)

    def gen_literal(self):
        nt = random.choice([True, False])
        literal = Literal(self.get_atom_from_shaker(), nt)
        if literal not in self.literals:
            self.literals.append(literal)
        return literal

    def get_atom_from_shaker(self):
        if self.shaker_index == len(self.atoms):
            self.shaker_index = 0
            random.shuffle(self.atoms)

        self.shaker_index += 1
        return self.atoms[self.shaker_index-1]

    def gen_atom(self):
        ltype = random.choice(['=', 'str.contains'])

        my_string1 = self.gen_or_get_string(
            lvl=random.randint(1, self.config['max_string_depth']),
            stypes=['const', 'variable', 'str.++',
                    'str.replace', 'str.replace_all']
        )
        my_string2 = self.gen_or_get_string(
            lvl=random.randint(1, self.config['max_string_depth']),
            stypes=['variable', 'str.++', 'str.replace', 'str.replace_all']
        )

        while my_string1 == my_string2:
            my_string2 = self.gen_or_get_string(
                lvl=random.randint(1, self.config['max_string_depth']),
                stypes=['variable', 'str.++', 'str.replace', 'str.replace_all']
            )

        if randbool():
            my_string1, my_string2 = my_string2, my_string1

        new_atom = Atom(ltype, my_string1, my_string2)
        self.atoms.append(new_atom)

    def gen_or_get_string(self, lvl=1, stypes=['const', 'variable', 'str.++', 'str.replace', 'str.replace_all'], create_new_prob=0.5, not_void=False):
        # первый уровень -> константа или переменная
        if lvl == 1:
            const_prob = ('const' in stypes) * random.random()
            variable_prob = ('variable' in stypes) * random.random()
            if const_prob > variable_prob:
                # генерим константу
                return self.gen_constant(not_void)
            else:
                return random.choice(self.variables)
        # 2+ уровень -> str.replace(_all)? или str.++
        concat_prob = ('str.++' in stypes) * random.random()
        replace_prob = ('str.replace' in stypes) * random.random()
        replaceall_prob = ('str.replace_all' in stypes) * random.random()
        stype = random.choices(['str.++', 'str.replace', 'str.replace_all'],
                               weights=[concat_prob, replace_prob, replaceall_prob], k=1)[0]

        if stype == 'str.++':
            strings_to_concat = []
            for i in range(2, self.config['max_concat_number']+1):
                strings_to_concat.append(self.gen_or_get_string(lvl=random.randint(
                    1, lvl-1), stypes=['const', 'variable', 'str.replace', 'str.replace_all'], not_void=True))
            my_string = My_String(
                stype='str.++', concats_strs=strings_to_concat)
            self.strings.append(my_string)
            return my_string

        else:
            if randbool(1 - create_new_prob):
                if list(filter(lambda x: x.stype == stype, self.strings)):
                    old_replace = random.choice(
                        list(filter(lambda x: x.stype == stype, self.strings)))
                    return old_replace

            strings_to_replace = [
                self.gen_or_get_string(lvl=lvl-1),
                self.gen_or_get_string(
                    lvl=random.randint(1, lvl-1), not_void=True),
                self.gen_or_get_string(random.randint(1, lvl-1)),
            ]
            my_string = My_String(stype, replace_strs=strings_to_replace)
            self.strings.append(my_string)
            return my_string

    def gen_constant(self, not_void=False):
        start = random.randint(
            0, len(self.alphabeth) - self.config['constant_max_len'])
        length = random.randint(
            self.config['constant_min_len'], self.config['constant_max_len'])
        if not_void and length == 0:
            length = random.randint(1, self.config['constant_max_len'])
        my_string = My_String(
            'const', cont=self.alphabeth[start:start+length])
        self.constants.append(my_string)
        return my_string

    def to_formula(self):
        """
        Возвращает объект типа Formula,
        инициализированный рекурсивными копиями полей self 
        """
        f = Formula(
            strings=deepcopy(self.variables) +
            deepcopy(self.constants) + deepcopy(self.strings),
            atoms=deepcopy(self.atoms),
            literals=deepcopy(self.literals),
            clauses=deepcopy(self.clauses)
        )
        return f

    def to_smt2_file(self, filepath=None, include_config=False):
        """
        file_path is None => std.out 
        """
        s = ''.join([f'CONFIG:  {key} : {self.config[key]}\n' for key in self.config]) + '\n' if include_config else ''
        
        s += '\n'.join([f'(define {str(x)} () String)' for x in self.variables])
        s+='\n\n'
        s += '\n'.join([f'(assert {str(x)})' for x in self.clauses])
        
        if not filepath:
            print(s)
            return 

        try:
            with open(filepath, 'w+') as dst:
                dst.write(s)
        except:
            raise Exception(f'невозможно открытыть файл {filepath} для записи')


if __name__ == '__main__':
    co = configparser.ConfigParser()
    g = Generator('formula_generator/generator_config.ini')
    # print(g.config)
    g.generate()
    # print(g)
    g.to_smt2_file(include_config=True, filepath='tests/generated_0.smt2')