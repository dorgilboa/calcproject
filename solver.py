from tester import *
from calculator import *


def evaluate_expression(expression_string):
    """
    :param input: The expression we would like to solve as a string.
    :return: The result of said evaluation.
    """
    temp = Calculator('~', -1)
    operators_dict = temp.oprtor_dict
    expression_string = expression_string.replace(" ", "")
    expression_string = expression_string.replace("\t", "")
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
    if calculation[2] == "no operator to check on.":
        expr_stack.insert(index, calculation[1])
        # if type(expr_stack[0]) != float:
        #     return "no valid"
    else:
        return "ERROR: " + str(expr_stack) + ", This is not a valid expression."

def extract_parenthesis(str_stack):
    new_str_stack = []
    for i in range(len(str_stack)):
        if str_stack[i] == ')':
            str_stack.pop(i)
            i -= 1
            while str_stack[i] != '(':
                new_str_stack.append(str_stack.pop(i))
                i -= 1
            if str_stack[i] == '(':
                str_stack.pop(i)
                return new_str_stack[::-1], i
    return None, None


def calc(stack, oprtor_dict):
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
        if result:
            return True, result, index_to_inset
        else:
            return False, result, sides
    if stack:
        return False, stack[0], sides
    else:
        return False, "ERROR - no operand was given", sides



def main():
    string = []
    while True:
        char = 97
        string.append(chr(char))
        for j in range(len(string)-1,-1,-1):
            char = 97
            while char < 102:
                string[j] = chr(char)
                print(string)
                char += 1



if __name__ == '__main__':
    main()
