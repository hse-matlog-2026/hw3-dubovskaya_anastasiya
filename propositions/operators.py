# This file is part of the materials accompanying the book
# "Mathematical Logic through Python" by Gonczarowski and Nisan,
# Cambridge University Press. Book site: www.LogicThruPython.org
# (c) Yannai A. Gonczarowski and Noam Nisan, 2017-2022
# File name: propositions/operators.py

"""Syntactic conversion of propositional formulas to use only specific sets of
operators."""

from propositions.syntax import *
from propositions.semantics import *

def to_not_and_or(formula: Formula) -> Formula:
    """Syntactically converts the given formula to an equivalent formula that
    contains no constants or operators beyond ``'~'``, ``'&'``, and ``'|'``.

    Parameters:
        formula: formula to convert.

    Returns:
        A formula that has the same truth table as the given formula, but
        contains no constants or operators beyond ``'~'``, ``'&'``, and
        ``'|'``.
    """
    # Task 3.5
    if is_variable(formula.root):
        return Formula(formula.root)
    if is_constant(formula.root):
        p = Formula('p')
        if formula.root == 'T':
            return Formula('|', p, Formula('~', p))
        return Formula('&', p, Formula('~', p))
    if is_unary(formula.root):
        return Formula('~', to_not_and_or(formula.first))
    a = to_not_and_or(formula.first)
    b = to_not_and_or(formula.second)
    if formula.root == '&':
        return Formula('&', a, b)
    if formula.root == '|':
        return Formula('|', a, b)
    if formula.root == '->':
        return Formula('|', Formula('~', a), b)
    if formula.root == '+':
        return Formula('|', Formula('&', a, Formula('~', b)),
                       Formula('&', Formula('~', a), b))
    if formula.root == '<->':
        return Formula('|', Formula('&', a, b),
                       Formula('&', Formula('~', a), Formula('~', b)))
    if formula.root == '-&':
        return Formula('|', Formula('~', a), Formula('~', b))
    if formula.root == '-|':
        return Formula('&', Formula('~', a), Formula('~', b))
    raise ValueError('Unknown operator: ' + formula.root)

def to_not_and(formula: Formula) -> Formula:
    """Syntactically converts the given formula to an equivalent formula that
    contains no constants or operators beyond ``'~'`` and ``'&'``.

    Parameters:
        formula: formula to convert.

    Returns:
        A formula that has the same truth table as the given formula, but
        contains no constants or operators beyond ``'~'`` and ``'&'``.
    """
    # Task 3.6a
    return to_not_and_or(formula).substitute_operators(
        {'|': Formula.parse('~(~p&~q)')})

def to_nand(formula: Formula) -> Formula:
    """Syntactically converts the given formula to an equivalent formula that
    contains no constants or operators beyond ``'-&'``.

    Parameters:
        formula: formula to convert.

    Returns:
        A formula that has the same truth table as the given formula, but
        contains no constants or operators beyond ``'-&'``.
    """
    # Task 3.6b
    return to_not_and(formula).substitute_operators({
        '~': Formula.parse('(p-&p)'),
        '&': Formula.parse('((p-&q)-&(p-&q))')})

def to_implies_not(formula: Formula) -> Formula:
    """Syntactically converts the given formula to an equivalent formula that
    contains no constants or operators beyond ``'->'`` and ``'~'``.

    Parameters:
        formula: formula to convert.

    Returns:
        A formula that has the same truth table as the given formula, but
        contains no constants or operators beyond ``'->'`` and ``'~'``.
    """
    # Task 3.6c
    return to_not_and_or(formula).substitute_operators({
        '&': Formula.parse('~(p->~q)'),
        '|': Formula.parse('(~p->q)')})

def to_implies_false(formula: Formula) -> Formula:
    """Syntactically converts the given formula to an equivalent formula that
    contains no constants or operators beyond ``'->'`` and ``'F'``.

    Parameters:
        formula: formula to convert.

    Returns:
        A formula that has the same truth table as the given formula, but
        contains no constants or operators beyond ``'->'`` and ``'F'``.
    """
    # Task 3.6d
    return to_implies_not(formula).substitute_operators({
        '~': Formula.parse('(p->F)')})
