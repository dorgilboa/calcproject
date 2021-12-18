from tester import *
from calculator import *


def evaluate_expression(expression_string):
    """
    :param input: The expression we would like to solve as a string.
    :return: The result of said evaluation, None if there is no result.
    The function runs first on brackets, then pushes the final result
    back to the original expression. Then it calculate the rest of the
    expression and checks for flags that say the calculation failed.
    """
    temp = Calculator('~', -1)
    operators_dict = temp.oprtor_dict
    expression_string = input_val(expression_string)
    if expression_string == ' ':
        return None
    is_syntax_valid, syntax_msg = syntax_val(expression_string, operators_dict)
    if is_syntax_valid:
        expr_stack = to_stack(expression_string, operators_dict)
        bracket, b_index = extract_parenthesis(expr_stack)
        while bracket is not None:
            calculation = calc(bracket, operators_dict)
            while calculation[0]:
                try:
                    bracket.insert(calculation[2], calculation[1])
                    calculation = calc(bracket, operators_dict)
                except Exception as err:
                    print(err)
                    break
            if is_calc_fail(calculation,expr_stack,b_index) == "no valid":
                return None
            bracket, b_index = extract_parenthesis(expr_stack)
        calculation = calc(expr_stack, operators_dict)
        while calculation[0]:
            try:
                expr_stack.insert(calculation[2], calculation[1])
                calculation = calc(expr_stack, operators_dict)
            except Exception as err:
                print(err)
                break
        if calculation[2] == "no operator to check on.":
            val_return = is_calc_fail(calculation, expr_stack)
            if type(val_return) is str:
                return val_return
            else:
                return expr_stack[0]
    else:
        print(syntax_msg)
        return None


def is_calc_fail(calculation, expr_stack, index=0):
    """
    :param calculation: A list of three flags -
    first (Boolean) - True if there is result to calculation, otherwise False.
    second (None or Float) - result if there is any.
    third (string) - flag message for result case of calculation process.
    :param expr_stack: the stack that contains the expression while calculating
    it, divided by two types - string and float (operators and operands).
    :param index: index to put result in if there is any.
    :return: only if there is an error - a message of a wrong expression the
    calculation process had bumped into. Otherwise, it'll push the result
    back in the stack.
    """
    if calculation[2] == "no operator to check on.":
        expr_stack.insert(index, calculation[1])
    else:
        return "ERROR: " + str(expr_stack) + ", This is not a valid expression."

def extract_parenthesis(expr_stack):
    """
    :param expr_stack: the stack that contains the expression while calculating
    it, divided by two types - string and float (operators or brackets and operands).
    :param new_expr_stack: the new stack contains only the most significant
    bracket (or parenthesis) there is in the expression. None if there is any.
    :return: new_expr_stack or None if there are no brackets.
    """
    new_expr_stack = []
    for i in range(len(expr_stack)):
        if expr_stack[i] == ')':
            expr_stack.pop(i)
            i -= 1
            while expr_stack[i] != '(':
                new_expr_stack.append(expr_stack.pop(i))
                i -= 1
            if expr_stack[i] == '(':
                expr_stack.pop(i)
                return new_expr_stack[::-1], i
    return None, None


def calc(stack, oprtor_dict):
    """
    :param stack: The main (or bracket) stack the program runs on, divided
    by two types - string and float (operators and operands).
    :param oprtor_dict: A dictionary from the calculator module that contains
    the operators as a key. each key has a list as a value that contains the
    significance of its key, the function that calculates according to it and
    the sides the operator gets operands from.
    :return: A flag if calculation succeeded, a result, or, if calculate
    failed, a flag message (sides), and sometimes an error message if needed.
    """
    index_to_inset = 0
    curr_oprtor_index = strongest_operator_index(stack, oprtor_dict)
    can_calc, sides = arithmetic_val(stack, curr_oprtor_index, oprtor_dict)
    if can_calc:
        if sides == "lr":
            calculation = Calculator(stack[curr_oprtor_index], stack[curr_oprtor_index - 1],
                                     stack[curr_oprtor_index + 1])
            stack.pop(curr_oprtor_index - 1)
            stack.pop(curr_oprtor_index - 1)
            stack.pop(curr_oprtor_index - 1)
            index_to_inset = curr_oprtor_index - 1
        if sides == "ln":
            calculation = Calculator(stack[curr_oprtor_index], stack[curr_oprtor_index - 1])
            stack.pop(curr_oprtor_index - 1)
            stack.pop(curr_oprtor_index - 1)
            index_to_inset = curr_oprtor_index - 1
        if sides == "nr":
            calculation = Calculator(stack[curr_oprtor_index], stack[curr_oprtor_index + 1])
            stack.pop(curr_oprtor_index)
            stack.pop(curr_oprtor_index)
            index_to_inset = curr_oprtor_index
        result = calculation.get_result()
        if result is not None:
            return True, result, index_to_inset
        else:
            return False, result, sides
    if stack:
        return False, stack[0], sides
    else:
        return False, "ERROR - no operand was given", sides