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
    ret = My_String('str.++', concats_strs=repr_array)
    return ret

def simplify(rep_l, rep_r):
    for char_l, char_r in zip(rep_l, rep_r):
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


def find_splits(rep_char):
    if rep_char.type == 'char':
        if 'const' not in multiset_l:
            multiset_l['const'] = 0
        multiset_l['const'] += 1
    elif rep_char.type == 'variable':
        if rep_char.content not in multiset_l:
            multiset_l[rep_char.content] = 0
        multiset_l[rep_char.content] += 1


def cutter_cycle(representation_l, representation_r):
    returnset_l = []
    returnset_r = []
    final_returnset = []
    left_right_simplify(representation_l, representation_r)
    if len(representation_l) <= len(representation_r):
        length = len(representation_l)
    else:
        length = len(representation_r)
    for i in range(length):
        for char_l, char_r in zip(representation_l, representation_r):
            find_splits(char_l)
            find_splits(char_r)
            if multiset_l == multiset_r:
                print("!!!!!!!!!!!!!!!!!!!!!!")
                cut_len = sum(multiset_l.values())
                returnset_l.append(representation_l[0:cut_len-1])
                returnset_r.append(representation_r[0:cut_len-1])
                representation_l = representation_l[cut_len:]
                representation_r = representation_r[cut_len:]
                left_right_simplify(representation_l, representation_r)
                break

    if not representation_l and representation_r:
        returnset_r.append(representation_r)
    elif not representation_r and representation_l:
        returnset_l.append(representation_l)
    for arr in returnset_l:
        arr = translate_representation(arr)
    for arr in returnset_r:
        arr = translate_representation(arr)
    for mystr_l, mystr_r in zip(returnset_l, returnset_r):
        final_returnset.append(Atom('=', mystr_l, mystr_r))
    return final_returnset



def cut(formula):
    for literal in formula.literals:
        if literal.atom.ltype == '=' and literal.atom.my_string1.stype == 'str.++' and literal.atom.my_string2.stype == 'str.++':
            if literal.negation is True:
                repres_l, repres_r = translate_literal(literal.atom)
                print("!!!!!!!!!!!!!!!!!!!!!!")
                cut_atom = cutter_cycle(repres_l, repres_r)
                for new_atom in cut_atom:
                    new_atom = Literal(new_atom, True)
                formula.literals.remove(literal)
                for new_literal in cut_atom:
                    formula.literals.append(new_literal)
