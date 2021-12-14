from solver import *


def syntax_val(expr_string, oprtor_dict):
    invalid_chars = ""
    for char in expr_string:
        if char not in oprtor_dict.keys() and not char.isdigit() and not char == '.' \
                and not char == '(' and not char == ')':
            invalid_chars += "\'" + str(char) + "\', "
    if invalid_chars == "":
        pars_val, msg = check_parentheses(expr_string)
        if pars_val:
            oprtors_val, msg = operators_validation(expr_string, oprtor_dict)
            if oprtors_val:
                return True, msg
            else:
                return False, msg
        else:
            return False, msg
    return False, invalid_chars + "are not valid chars..."


def check_parentheses(expr_string):
    close_p = 0
    open_p = 0
    between = -1
    is_between = False
    for char in expr_string:
        if char == '(':
            open_p += 1
            is_between = True
        if char == ')':
            if between == 0:
                return False, "ERROR - No expressions between the brackets."
            close_p += 1
            is_between = False
        if is_between:
            between += 1
    if is_between:
        return False, "ERROR - No closure bracket in this expression. One bracket remained opened."
    if close_p != open_p:
        return False, "ERROR - The amount of openers brackets is different than the amount of closure brackets."
    return True, "all valid"


def operators_validation(expr_string, oprtors_dict):
    for index in range(len(expr_string)):
        