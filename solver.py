from calculator import *
from checker import *


def evaluate_expression(expression_string):
    """
    :param input: The expression we would like to solve as a string.
    :return: The result of said evaluation.
    """
    var_to_get_operators_dict = Calculator('~', -1)
    operators_dict = var_to_get_operators_dict.oprtor_dict
    expression_string = expression_string.replace(" ", "")
    expression_string = expression_string.replace("\t", "")
    is_syntax_valid, syntax_msg = syntax_val(expression_string, operators_dict)
    if is_syntax_valid:
        expression_stack, seperate_msg = seperate_expression(expression_string, operators_dict)
        if expression_stack:
            parenthesis, p_index = extract_parenthesis(expression_stack)
            while parenthesis is not None:
                calculation = try_to_calc(parenthesis, operators_dict)
                while calculation[0]:
                    try:
                        parenthesis.insert(calculation[2], calculation[1])
                        calculation = try_to_calc(parenthesis, operators_dict)
                    except:
                        break
                if check_for_calc_error(calculation, expression_stack, p_index) == "no valid":
                    return ""
                parenthesis, p_index = extract_parenthesis(expression_stack)
            calculation = try_to_calc(expression_stack,operators_dict)
            while calculation[0]:
                try:
                    expression_stack.insert(calculation[2], calculation[1])
                    calculation = try_to_calc(expression_stack, operators_dict)
                except:
                    print("too high")
                    break
            if calculation[2] == "no operator to check on.":
                can_return_val = check_for_calc_error(calculation, expression_stack)
                if type(can_return_val) == str:
                    return can_return_val
                else:
                    return expression_stack[0]
            else:
                can_return_val = check_for_calc_error(calculation, expression_stack)
                if type(can_return_val) == str:
                    return can_return_val
                else:
                    return ""
        else:
            print(seperate_msg)
    else:
        print(syntax_msg)


def check_for_calc_error(calculation, expr_stack, index=0):
    if calculation[2] == "no operator to check on.":
        expr_stack.insert(index, calculation[1])
        if type(expr_stack[0]) != float:
            return "no valid"
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


def try_to_calc(str_stack, oprtor_dict):
    index_to_inset = 0
    curr_oprtor_index = strongest_operator_index(str_stack, oprtor_dict)
    # try:
    can_calc, sides = arithmetic_val(str_stack, curr_oprtor_index, oprtor_dict)
    if can_calc:
        if sides == "lr":
            calc = Calculator(str_stack[curr_oprtor_index], str_stack[curr_oprtor_index - 1],
                              str_stack[curr_oprtor_index + 1])
            str_stack.pop(curr_oprtor_index - 1)
            str_stack.pop(curr_oprtor_index - 1)
            str_stack.pop(curr_oprtor_index - 1)
            index_to_inset = curr_oprtor_index - 1
        if sides == "ln":
            calc = Calculator(str_stack[curr_oprtor_index], str_stack[curr_oprtor_index - 1])
            str_stack.pop(curr_oprtor_index - 1)
            str_stack.pop(curr_oprtor_index - 1)
            index_to_inset = curr_oprtor_index - 1
        if sides == "nr":
            calc = Calculator(str_stack[curr_oprtor_index], str_stack[curr_oprtor_index + 1])
            str_stack.pop(curr_oprtor_index)
            str_stack.pop(curr_oprtor_index)
            index_to_inset = curr_oprtor_index
        return True, calc.get_result(), index_to_inset
    if str_stack:
        return False, str_stack[0], sides
    else:
        return False, "ERROR - no operand was given", sides
    # except:
    #     return False, None, None


def main():
    print(evaluate_expression(input("Please Enter Your'e expression here: ")))


if __name__ == '__main__':
    main()
