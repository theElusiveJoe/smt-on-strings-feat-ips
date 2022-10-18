from .structures import *


def translate_literal(atom):
    return_array_l = []
    return_array_r = []
    if atom.my_string1.concats_strs:
        for mystr in atom.my_string1.concats_strs:
            if mystr.stype == 'const':
                for char in mystr.cont:
                    return_array_l.append(String_Theory_Representation('char', char))
            elif mystr.stype == 'variable':
                return_array_l.append(String_Theory_Representation('variable', mystr.var_name))
    else:
        if atom.my_string1.stype == 'const':
            for char in atom.my_string1.cont:
                return_array_l.append(String_Theory_Representation('char', char))
        elif atom.my_string1.stype == 'variable':
            return_array_l.append(String_Theory_Representation('variable', atom.my_string1.var_name))

    if atom.my_string2.concats_strs:
        for mystr in atom.my_string2.concats_strs:
            if mystr.stype == 'const':
                for char in mystr.cont:
                    return_array_r.append(String_Theory_Representation('char', char))
            elif mystr.stype == 'variable':
                return_array_r.append(String_Theory_Representation('variable', mystr.var_name))
    else:
        if atom.my_string2.stype == 'const':
            for char in atom.my_string2.cont:
                return_array_r.append(String_Theory_Representation('char', char))
        elif atom.my_string2.stype == 'variable':
            return_array_r.append(String_Theory_Representation('variable', atom.my_string2.var_name))
    return return_array_l, return_array_r


def translate_representation(repr_array):
    temp = []
    if len(repr_array) > 1:
        for repr in repr_array:
            if repr.type == 'char':
                temp_mystring = My_String('const', cont=repr.content)
                temp.append(temp_mystring)
            elif repr.type == 'variable':
                temp.append(My_String(stype='variable', var_name=repr.content))
        ret = My_String('str.++', concats_strs=temp)
    elif len(repr_array) == 1:
        if repr_array[0].type == 'char':
            ret = My_String('const', cont=repr_array[0].content)
        elif repr_array[0].type == 'variable':
            ret = My_String('variable', var_name=repr_array[0].content)
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
multiset_l_helper_2 = []
multiset_r_helper_2 = []


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
    length = 0
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
    if multiset_l_helper or multiset_r_helper:
        for arr in returnset_l:
            length += len(arr)
        returnset_l.append(representation_l[length:])
        returnset_r.append(representation_r[length:])
    elif len(representation_l) != len(representation_r):
        len_l = 0
        len_r = 0
        for arr in returnset_l:
            len_l += len(arr)
        for arr in returnset_r:
            len_r += len(arr)
        if len(representation_l) > len(representation_r):
            returnset_l.append(representation_l[len_l:])
            returnset_r.append([String_Theory_Representation('char', "")])
        else:
            returnset_r.append(representation_r[len_r:])
            returnset_l.append([String_Theory_Representation('char', "")])
    for arr_l, arr_r in zip(returnset_l[:], returnset_r[:]):
        if len(arr_l) == 1 and len(arr_r) == 1 and arr_l == arr_r:
            returnset_l.remove(arr_l)
            returnset_r.remove(arr_r)
    for i in range(len(returnset_l)):
        returnset_l[i] = translate_representation(returnset_l[i])
    for i in range(len(returnset_r)):
        returnset_r[i] = translate_representation(returnset_r[i])
    for mystr_l, mystr_r in zip(returnset_l, returnset_r):
        final_returnset.append(Atom('=', mystr_l, mystr_r))
    multiset_l = {}
    multiset_r = {}
    multiset_l_helper = []
    multiset_r_helper = []
    return final_returnset


def cut(formula):
    for clause in formula.clauses[:]:
        for literal in clause.literals:
            if literal.atom.ltype == '=' and literal.atom.my_string1.stype == 'str.++' and literal.atom.my_string2.stype == 'str.++':
                if literal.negation is True:
                    repres_l, repres_r = translate_literal(literal.atom)
                    cut_atom = cutter_cycle(repres_l, repres_r)
                    if len(cut_atom) == 1:
                        repres_l, repres_r = translate_literal(cut_atom[0])
                        cut_atom_2 = cutter_cycle(repres_l[::-1], repres_r[::-1])
                        if len(cut_atom_2) == 1:
                            if not cut_atom[0].my_string1.concats_strs and not cut_atom[0].my_string2.concats_strs:
                                len_sum1 = 2
                            elif not cut_atom[0].my_string1.concats_strs and cut_atom[0].my_string2.concats_strs:
                                len_sum1 = 1 + len(cut_atom[0].my_string2.concats_strs)
                            elif cut_atom[0].my_string1.concats_strs and not cut_atom[0].my_string2.concats_strs:
                                len_sum1 = 1 + len(cut_atom[0].my_string1.concats_strs)
                            elif cut_atom[0].my_string1.concats_strs and cut_atom[0].my_string2.concats_strs:
                                len_sum1 = len(cut_atom[0].my_string1.concats_strs) + len(
                                    cut_atom[0].my_string2.concats_strs)

                            if not cut_atom_2[0].my_string1.concats_strs and not cut_atom_2[0].my_string2.concats_strs:
                                len_sum2 = 2
                            elif not cut_atom_2[0].my_string1.concats_strs and cut_atom_2[0].my_string2.concats_strs:
                                len_sum2 = 1 + len(cut_atom_2[0].my_string2.concats_strs)
                            elif cut_atom_2[0].my_string1.concats_strs and not cut_atom_2[0].my_string2.concats_strs:
                                len_sum2 = 1 + len(cut_atom_2[0].my_string1.concats_strs)
                            elif cut_atom_2[0].my_string1.concats_strs and cut_atom_2[0].my_string2.concats_strs:
                                len_sum2 = len(cut_atom_2[0].my_string1.concats_strs) + len(
                                    cut_atom_2[0].my_string2.concats_strs)

                            if len_sum1 > len_sum2:
                                if cut_atom_2[0].my_string1.concats_strs:
                                    cut_atom_2[0].my_string1.concats_strs = cut_atom_2[0].my_string1.concats_strs[::-1]
                                if cut_atom_2[0].my_string2.concats_strs:
                                    cut_atom_2[0].my_string2.concats_strs = cut_atom_2[0].my_string2.concats_strs[::-1]
                                cut_atom = cut_atom_2
                        elif len(cut_atom_2) > 1:
                            for atom in cut_atom_2:
                                if atom.my_string1.concats_strs:
                                    atom.my_string1.concats_strs = atom.my_string1.concats_strs[::-1]
                                if atom.my_string2.concats_strs:
                                    atom.my_string2.concats_strs = atom.my_string2.concats_strs[::-1]
                            cut_atom = cut_atom_2
                    elif len(cut_atom) > 1:
                        temp = cut_atom[-1]
                        if temp.my_string1.concats_strs:
                            temp.my_string1.concats_strs = temp.my_string1.concats_strs[::-1]
                        if temp.my_string2.concats_strs:
                            temp.my_string2.concats_strs = temp.my_string2.concats_strs[::-1]
                        repres_l, repres_r = translate_literal(temp)
                        cut_atom_2 = cutter_cycle(repres_l, repres_r)
                        for atom in cut_atom_2:
                            if atom.my_string1.concats_strs:
                                atom.my_string1.concats_strs = atom.my_string1.concats_strs[::-1]
                            if atom.my_string2.concats_strs:
                                atom.my_string2.concats_strs = atom.my_string2.concats_strs[::-1]
                        cut_atom.remove(temp)
                        cut_atom.extend(cut_atom_2)
                    if literal in clause.literals:
                        clause.literals.remove(literal)
                    if literal in formula.literals:
                        formula.literals.remove(literal)
                    if literal.atom in formula.atoms:
                        formula.atoms.remove(literal.atom)
                    if literal.atom.my_string1 in formula.strings:
                        formula.strings.remove(literal.atom.my_string1)
                    if literal.atom.my_string2 in formula.strings:
                        formula.strings.remove(literal.atom.my_string2)
                    for i in range(len(cut_atom)):
                        formula.strings.append(cut_atom[i].my_string1)
                        formula.strings.append(cut_atom[i].my_string2)
                        formula.atoms.append(cut_atom[i])
                        cut_atom[i] = Literal(cut_atom[i], True)
                        formula.literals.append(cut_atom[i])
                        clause.literals.append(cut_atom[i])
                    for new_literal in cut_atom:
                        formula.literals.append(new_literal)
                elif literal.negation is False:
                    repres_l, repres_r = translate_literal(literal.atom)
                    cut_atom = cutter_cycle(repres_l, repres_r)

                    if len(cut_atom) == 1:
                        repres_l, repres_r = translate_literal(cut_atom[0])
                        cut_atom_2 = cutter_cycle(repres_l[::-1], repres_r[::-1])
                        if len(cut_atom_2) == 1:

                            len_sum1 = 0
                            if cut_atom[0].my_string1.concats_strs:
                                len_sum1 += len(cut_atom[0].my_string1.concats_strs)
                            else:
                                len_sum1 += 1
                            if cut_atom[0].my_string2.concats_strs:
                                len_sum1 += len(cut_atom[0].my_string2.concats_strs)
                            else:
                                len_sum1 += 1

                            len_sum2 = 0
                            if cut_atom_2[0].my_string1.concats_strs:
                                len_sum2 += len(cut_atom_2[0].my_string1.concats_strs)
                            else:
                                len_sum2 += 1
                            if cut_atom_2[0].my_string2.concats_strs:
                                len_sum2 += len(cut_atom_2[0].my_string2.concats_strs)
                            else:
                                len_sum2 += 1

                            if len_sum1 > len_sum2:
                                if cut_atom_2[0].my_string1.concats_strs:
                                    cut_atom_2[0].my_string1.concats_strs = cut_atom_2[0].my_string1.concats_strs[::-1]
                                if cut_atom_2[0].my_string2.concats_strs:
                                    cut_atom_2[0].my_string2.concats_strs = cut_atom_2[0].my_string2.concats_strs[::-1]
                                cut_atom = cut_atom_2
                        elif len(cut_atom_2) > 1:
                            for atom in cut_atom_2:
                                if atom.my_string1.concats_strs:
                                    atom.my_string1.concats_strs = atom.my_string1.concats_strs[::-1]
                                if atom.my_string2.concats_strs:
                                    atom.my_string2.concats_strs = atom.my_string2.concats_strs[::-1]
                            cut_atom = cut_atom_2
                    elif len(cut_atom) > 1:
                        temp = cut_atom[-1]
                        if temp.my_string1.concats_strs:
                            temp.my_string1.concats_strs = temp.my_string1.concats_strs[::-1]
                        if temp.my_string2.concats_strs:
                            temp.my_string2.concats_strs = temp.my_string2.concats_strs[::-1]
                        repres_l, repres_r = translate_literal(temp)
                        cut_atom_2 = cutter_cycle(repres_l, repres_r)
                        for atom in cut_atom_2:
                            if atom.my_string1.concats_strs:
                                atom.my_string1.concats_strs = atom.my_string1.concats_strs[::-1]
                            if atom.my_string2.concats_strs:
                                atom.my_string2.concats_strs = atom.my_string2.concats_strs[::-1]
                        cut_atom.remove(temp)
                        cut_atom.extend(cut_atom_2)

                    if literal in formula.literals:
                        formula.literals.remove(literal)
                    if literal in clause.literals:
                        clause.literals.remove(literal)
                    if literal.atom in formula.atoms:
                        formula.atoms.remove(literal.atom)
                    if literal.atom.my_string1 in formula.strings:
                        formula.strings.remove(literal.atom.my_string1)
                    if literal.atom.my_string2 in formula.strings:
                        formula.strings.remove(literal.atom.my_string2)
                    temp = []
                    for i in range(len(cut_atom)):
                        formula.strings.append(cut_atom[i].my_string1)
                        formula.strings.append(cut_atom[i].my_string2)
                        formula.atoms.append(cut_atom[i])
                        formula.literals.append(Literal(cut_atom[i], False))
                        temp.append(Literal(cut_atom[i], False))
                        formula.clauses.append(Clause(temp))
                        temp = []
    for clause in formula.clauses[:]:
        if not clause.literals:
            formula.clauses.remove(clause)
