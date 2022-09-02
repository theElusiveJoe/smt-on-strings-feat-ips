from .structures import *


def translate_literal(atom):
    return_array_l = []
    return_array_r = []
    for mystr in atom.my_string1.concats_strs:
        if mystr.stype == 'const':
            for char in mystr.cont:
                return_array_l.append(String_Theory_Representation('char', char))
        elif mystr.stype == 'variable':
            return_array_l.append(String_Theory_Representation('variable', mystr.var_name))

    for mystr in atom.my_string2.concats_strs:
        if mystr.stype == 'const':
            for char in mystr.cont:
                return_array_r.append(String_Theory_Representation('char', char))
        elif mystr.stype == 'variable':
            return_array_r.append(String_Theory_Representation('variable', mystr.var_name))
    return return_array_l, return_array_r


def translate_representation(repr_array):
    temp = []
    for repr in repr_array:
        if repr.type == 'char':
            temp_mystring = My_String('const', cont=repr.content)
            temp.append(temp_mystring)
        elif repr.type == 'variable':
            temp.append(My_String(stype='variable', var_name=repr.content))
    ret = My_String('str.++', concats_strs=temp)
    return ret


def simplify(rep_l, rep_r):
    for char_l, char_r in zip(rep_l[:], rep_r[:]):
        if char_l == char_r:
            rep_l.remove(char_l)
            rep_r.remove(char_r)
        else:
            break


def reverse_arrays(arr1, arr2):
    arr1 = arr1[::-1]
    arr2 = arr2[::-1]


def left_right_simplify(rep_l, rep_r):
    simplify(rep_l, rep_r)
    reverse_arrays(rep_l, rep_r)
    simplify(rep_l, rep_r)
    reverse_arrays(rep_l, rep_r)


multiset_l = {}
multiset_r = {}
multiset_l_helper = []
multiset_r_helper = []


def find_splits(rep_char, multiset, multiset_helper):
    if rep_char.type == 'char':
        if 'const' not in multiset:
            multiset['const'] = 0
        multiset['const'] += 1
        multiset_helper.append(rep_char)
    elif rep_char.type == 'variable':
        if rep_char.content not in multiset:
            multiset[rep_char.content] = 0
        multiset[rep_char.content] += 1
        multiset_helper.append(rep_char)


def cutter_cycle(representation_l, representation_r):
    global multiset_l, multiset_r, multiset_l_helper, multiset_r_helper
    returnset_l = []
    returnset_r = []
    final_returnset = []
    left_right_simplify(representation_l, representation_r)

    for char_l, char_r in zip(representation_l[:], representation_r[:]):
        find_splits(char_l, multiset_l, multiset_l_helper)
        find_splits(char_r, multiset_r, multiset_r_helper)
        if multiset_l == multiset_r:
            returnset_l.append(multiset_l_helper)
            returnset_r.append(multiset_r_helper)
            multiset_l = {}
            multiset_r = {}
            multiset_l_helper = []
            multiset_r_helper = []

    if multiset_l_helper and multiset_r_helper:
        returnset_l.append(multiset_l_helper)
        returnset_r.append(multiset_r_helper)

    for i in range(len(returnset_l)):
        returnset_l[i] = translate_representation(returnset_l[i])
    for i in range(len(returnset_r)):
        returnset_r[i] = translate_representation(returnset_r[i])
    for mystr_l, mystr_r in zip(returnset_l, returnset_r):
        final_returnset.append(Atom('=', mystr_l, mystr_r))
    return final_returnset


def cut(formula):
    for literal in formula.literals[:]:
        if literal.atom.ltype == '=' and literal.atom.my_string1.stype == 'str.++' and literal.atom.my_string2.stype == 'str.++':
            if literal.negation is True:
                repres_l, repres_r = translate_literal(literal.atom)
                cut_atom = cutter_cycle(repres_l, repres_r)
                for i in range(len(cut_atom)):
                    formula.atoms.append(cut_atom[i])
                    cut_atom[i] = Literal(cut_atom[i], True)
                formula.literals.remove(literal)
                formula.atoms.remove(literal.atom)
                for clause in formula.clauses[:]:
                    if literal in clause.literals:
                        formula.clauses.remove(clause)
                for new_literal in cut_atom:
                    formula.literals.append(new_literal)
                formula.clauses.append(Clause(cut_atom))
            elif literal.negation is False:
                repres_l, repres_r = translate_literal(literal.atom)
                cut_atom = cutter_cycle(repres_l, repres_r)
                for i in range(len(cut_atom)):
                    formula.atoms.append(cut_atom[i])
                    temp_literal = Literal(cut_atom[i], False)
                    formula.literals.append(temp_literal)
                    cut_atom[i] = Clause(temp_literal)
                formula.literals.remove(literal)
                for clause in formula.clauses[:]:
                    if literal in clause.literals:
                        formula.clauses.remove(clause)
                for new_clause in cut_atom:
                    formula.clauses.append(new_clause)
