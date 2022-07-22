from .structures import *

def call_lia(f):
    return True


def call_theory(f, m):
    """
    По идее, теория вызывается просто на набор Литералов, 
    мб для этого выделить отдельную структуру?
    """
    return True


def literal_in_m(literal, m):
    not_literal = literal.get_conjugate()
    for x in m:
        if x == literal:
            return 0
        if x == not_literal:
            return 1
    return 'u'


def check_if_zero_without(c, literal, m):
    i = c.literals.index(literal)
    for x in c.literals[:i] + c.literals[i+1:]:
        if literal_in_m(x, m) != 0:
            return False
    return True


def unit_propagate(m, f):
    for c in f.clauses:
        for literal in c.literals:
            if literal_in_m(literal, m) == 'u' and check_if_zero_without(c, literal, m):
                m.append(literal.get_conjugate(decisive=False))
                print('M <-', literal.get_conjugate(decisive=False))
                return unit_propagate(m, f)

    return m, f


def check_broken(m, f):
    for c in f.clauses:
        if any([literal_in_m(literal, m) for literal in c.literals]):
            continue
        print('BROKEN')
        return False
    return True


def decide(m, f):
    for c in f.clauses:
        for literal in c.literals:
            if literal_in_m(literal, m) == 'u':
                print('Decide: ', literal.get_copy(decisive=False), '= 0')
                return literal


def check_node(m, f):
    """
    не забыть, что нельзя гонять один и тот же объект списка по рекурсивным вызовам
    """
    # 1 распространяем переменные
    m, f = unit_propagate(m, f)

    # 2 проверяем, не сломало ли ничего распространение
    if not check_broken(m, f):
        return False
    """
    в данный момент lia вызывается на каждом ветвлении
    """
    # 3 теперь можно проверить полученную модель в lia
    if not call_lia(f):
        return False

    # 4 проверяем, осталось ли чего неопределенного в m
    if len(m) == len(f.atoms):
        return call_theory(f, m)

    # 4 если осталось, то порождаем 2 ветки
    new_literal = l
    return check_node(m + [new_literal], f) or check_node(m+[new_literal.get_conjugate()], f)


def check_sat(f):
    return check_node([], f)
   