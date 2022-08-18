def left_right_simplify(my_string1, my_string2):
    if len(my_string1.concats_strs) <= len(my_string2.concats_strs):
        length = len(my_string1.concats_strs)
    else:
        length = len(my_string2.concats_strs)
    for i in range(length):
        if my_string1.concats_strs[i] != my_string2.concats_strs[i]:
            break
        if my_string1.concats_strs[i] == my_string2.concats_strs[i]:
            my_string1.concats_strs.remove(my_string1.concats_strs[i])
            my_string2.concats_strs.remove(my_string2.concats_strs[i])
    my_string1.concats_strs = my_string1.concats_strs[::-1]
    my_string2.concats_strs = my_string2.concats_strs[::-1]
    if len(my_string1.concats_strs) <= len(my_string2.concats_strs):
        length = len(my_string1.concats_strs)
    else:
        length = len(my_string2.concats_strs)
    for i in range(length):
        if my_string1.concats_strs[i] != my_string2.concats_strs[i]:
            break
        if my_string1.concats_strs[i] == my_string2.concats_strs[i]:
            my_string1.concats_strs.remove(my_string1.concats_strs[i])
            my_string2.concats_strs.remove(my_string2.concats_strs[i])
    my_string1.concats_strs = my_string1.concats_strs[::-1]
    my_string2.concats_strs = my_string2.concats_strs[::-1]


def cutter_cycle(atom):
    multiset_l = {}
    multiset_r = {}
    returnset_l = []
    returnset_r = []
    returnset_counter = 0
    concat_arr_l = []
    concat_arr_r = []
    final_returnset = []
    left_right_simplify(atom.my_string1, atom.my_string2)
    if len(atom.my_string1.concats_strs) <= len(atom.my_string2.concats_strs):
        length = len(atom.my_string2.concats_strs)
    else:
        length = len(atom.my_string1.concats_strs)
    for i in range(length):
        for mystring_1, mystring_2 in zip(atom.my_string1.concats_strs, atom.my_string2.concats_strs):
            if mystring_1.stype == 'const':
                if 'const' not in multiset_l:
                    multiset_l['const'] = 0
                multiset_l['const'] += 1
            elif mystring_1.stype == 'variable':
                if mystring_1.var_name not in multiset_l:
                    multiset_l[mystring_1.var_name] = 0
                multiset_l[mystring_1.var_name] += 1

            if mystring_2.stype == 'const':
                if 'const' not in multiset_r:
                    multiset_r['const'] = 0
                multiset_r['const'] += 1
            elif mystring_2.stype == 'variable':
                if mystring_2.var_name not in multiset_r:
                    multiset_r[mystring_2.var_name] = 0
                multiset_r[mystring_2.var_name] += 1

            if multiset_l == multiset_r:
                cut_len = sum(multiset_l.values())
                for i in range(cut_len):
                    returnset_l[returnset_counter][i] = mystring_1[i]
                    returnset_l[returnset_counter][i] = mystring_2[i]
                returnset_counter += 1
                atom.my_string1.concats_strs = atom.my_string1.concats_strs[cut_len:]
                atom.my_string2.concats_strs = atom.my_string2.concats_strs[cut_len:]
                break

    if not atom.my_string1.concats_strs and atom.my_string2.concats_strs:
        returnset_r.append(atom.my_string2.concats_strs)
    elif not atom.my_string2.concats_strs and atom.my_string1.concats_strs:
        returnset_l.append(atom.my_string1.concats_strs)

    for mystr_array1, mystr_array2 in zip(returnset_l, returnset_r):
        concat_arr_l.append(My_String('str.++', concats_strs=mystr_array1))
        concat_arr_r.append(My_String('str.++', concats_strs=mystr_array2))
    for left, right in zip(concat_arr_l, concat_arr_r):
        final_returnset = Atom('=', left, right)
    return final_returnset


def cut(formula):
    for literal in formula.literals:
        if literal.atom.ltype == '=' and literal.atom.my_string1.stype == 'str.++' and literal.atom.my_string2.stype == 'str.++':
            if literal.negation is True:
                cut_atom = cutter_cycle(literal.atom)
                for new_atom in cut_atom:
                    new_atom = Literal(new_atom, True)
                formula.literals.remove(literal)
                for new_literal in cut_atom:
                    formula.literals.append(new_literal)
