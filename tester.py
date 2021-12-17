def syntax_val(expr_string, oprtor_dict):
    """
    :param expr_string: The main expression that the user had inserted
    that sent from main to calculate.
    :param oprtor_dict: A dictionary from the calculator module that contains
    the operators as a key. each key has a list as a value that contains the
    significance of its key, the function that calculates according to it and
    the sides the operator gets operands from.
    :return: True or False if the expression is valid by syntax. Checks for
    letters, misplaced dots and brackets.
    """
    invalid_chars = ""
    for char in expr_string:
        if char not in oprtor_dict.keys() and not char.isdigit() and not char == '.' \
                and not char == '(' and not char == ')':
            invalid_chars += "\'" + str(char) + "\', "
    if invalid_chars == "":
        bracks_val, msg = brackets_val(expr_string)
        if bracks_val:
            dot_val, msg = dots_val(expr_string)
            if dot_val:
                oprs_val, msg = operators_val(expr_string, oprtor_dict)
                if oprs_val:
                    return True, msg
                else:
                    return False, msg
            else:
                return False, msg
        else:
            return False, msg
    return False, "Error - " + invalid_chars + "are not valid chars..."


def brackets_val(expr_string):
    """
    :param expr_string: The main expression that the user had inserted
    that sent from main to calculate.
    :return: False if there are parentheses that were written
    in a wrong way: with nothing between them, with one remains open
    and so... returns True for the opposite case.
    """
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
                return False, "Error - No expressions between the brackets."
            close_p += 1
            is_between = False
        if is_between:
            between += 1
    if is_between:
        return False, "Error - No closure bracket in this expression. One bracket remained opened."
    if close_p != open_p:
        return False, "Error - The amount of openers brackets is different than the amount of closure brackets."
    return True, "all valid"


def dots_val(expr_string):
    """
    :param expr_string: The main expression that the user had inserted
    that sent from main to calculate.
    :return: False if there are dots that were written in a wrong way:
    with no digit before or with no digit after. If all of the dots in
    the expression are a part of a valid number - x.x - it'll return True.
    """
    try:
        for index in range(len(expr_string)):
            if expr_string[index] == '.':
                if index == 0:
                    raise IndexError
                if not (expr_string[index - 1].isdigit() and expr_string[index + 1].isdigit()):
                    return False, "Error - Dot (\'.\') have to be between two digits in order to be a part of number: "
        return True, "all valid"
    except IndexError as ie:
        return False, "Error - Dot (\'.\') have to be between two digits in order to be a part of number."


def operators_val(expr_string, oprtors_dict):
    """
    :param expr_string: The main expression that the user had inserted
    that sent from main to calculate.
    :param oprtors_dict: A dictionary from the calculator module that contains
    the operators as a key. each key has a list as a value that contains the
    significance of its key, the function that calculates according to it and
    the sides the operator gets operands from.
    :return: True if all of the operators that are at the end or start of the
    expression are placed in a valid way, otherwise it'll return False.
    """
    index = 0
    expr_len = len(expr_string)
    while index < expr_len:
        if index == 0:
            if expr_string[index] in oprtors_dict.keys() and (not oprtors_dict[expr_string[index]][2] == 'nr'):
                if expr_string[index] == '-':
                    return True, 'all valid'
                return False, "Error - operator \'" + expr_string[index] + "\' cannot be at start."
        if index == expr_len - 1:
            if expr_string[index] in oprtors_dict.keys() and (not oprtors_dict[expr_string[index]][2] == 'ln'):
                return False, "Error - operator \'" + expr_string[index] + "\' cannot be at end."
        index += 1
    return True, "all valid"


def to_stack(expr_string, oprtors_dict):
    """
    :param expr_string: The main expression that the user had inserted
    that sent from main to calculate.
    :param oprtors_dict: A dictionary from the calculator module that contains
    the operators as a key. each key has a list as a value that contains the
    significance of its key, the function that calculates according to it and
    the sides the operator gets operands from.
    :return: A stack that contains all of the string expression components:
    numbers, operators, parenthesis.
    """
    expr_stack = []
    index = 0
    expr_len = len(expr_string)
    while index < expr_len:
        curr_i = index
        tempstr, index, expr_string = treat_minuses(expr_string, index, expr_stack, oprtors_dict)
        expr_len = len(expr_string)
        if index < len(expr_string) and expr_string[index].isdigit():
            while index < len(expr_string) and (expr_string[index].isdigit() or expr_string[index] == '.'):
                tempstr += expr_string[index]
                index += 1
            expr_stack.append(convert_to_number(tempstr))
            continue
            # now tempstr is a number -> i had changed, or '-' -> i had changed, or '' -> i had changed if appended (-1*
        if curr_i == index and curr_i < len(expr_string):
            expr_stack.append(expr_string[curr_i])
        index += 1
    return expr_stack


def convert_to_number(str_number):
    """
    :param str_number: A part from the original expression string that might
    contain a number (might has minus, dot, and must have digits).
    :return: A conversion of the string expression to a float-type number, None
    if the conversion cannot be done.
    """
    try:
        if str_number[0] == '.' or str_number[-1] == '.':
            raise ValueError("Not full number defining.")
        return float(str_number)
    except ValueError:
        print("Error: " + str(str_number) + " conversion to number cannot be done.")
        return None


def treat_minuses(expr_string, index, expr_stack, oprtors_dict):
    """
    :param expr_string: The main expression that the user had inserted
    that sent from main to calculate.
    :param index: the current index of the string that the main loop in the to_stack
    method sent to this method in order to extract and treat all minus cases.
    :param expr_stack: the stack that contains the expression while calculating
    it, divided by two types - string and float (operators or brackets and operands).
    :param oprtors_dict: A dictionary from the calculator module that contains
    the operators as a key. each key has a list as a value that contains the
    significance of its key, the function that calculates according to it and
    the sides the operator gets operands from.
    :return: it returns back the smallest amount of minuses the given expression
    represents, or add to the main stack (-1* in order to take care of special cases.
    It also returns the index's change while activating this function and a fixed
    expression string.
    """
    minustr = ""
    # sign minuses:
    if index == 0 or not (expr_string[index - 1].isdigit() or expr_string[index - 1] == ')' or (
                    expr_string[index - 1] in oprtors_dict.keys() and oprtors_dict[expr_string[index - 1]][2] == 'ln')):
        while expr_string[index] == '-':
            minustr += expr_string[index]
            index += 1
    # sign minuses before brackets or tilda and so...
    if len(minustr) != 0:
        if (expr_string[index] in oprtors_dict.keys() and oprtors_dict[expr_string[index]][2] == 'nr') or expr_string[
            index] == '(':
            if len(minustr) % 2 != 0:
                expr_stack.append('(')
                expr_stack.append(float(-1.0))
                expr_stack.append('*')
                if expr_string[index] == '(':
                    expr_string = add_closure(expr_string, index + 1, True)
                elif expr_string[index] in oprtors_dict.keys() and oprtors_dict[expr_string[index]][2] == 'nr':
                    if expr_string[index + 1] == '(':
                        expr_string = add_closure(expr_string, index + 1, True)
                    else:
                        expr_string = add_closure(expr_string, index + 1, False)
                        # minus_brack = True
            expr_stack.append(expr_string[index])
            return "", index, expr_string
        if len(minustr) % 2 != 0:
            return '-', index, expr_string
    return '', index, expr_string


def add_closure(expr_string, index, is_opener):
    """
    :param expr_string: The main expression that the user had inserted
    that sent from main to calculate.
    :param index: the current index of the string that the function treat_minuses
    gave in order to treat this specific case when a minus comes before brackets or
    before an operator that receives operands only from its right side.
    :param is_opener: A flag that if its value is True - the given case is an opener
    parenthesis after a minus, and if it is False - it is the other case - an operator
    that takes operands only from its right side.
    :return: The function returns a re-written main expression string with a closure
    bracket, right after the treat_minuses function added to the expression '(-1*', in
    order to keep the expression valid.
    """
    i = index
    if is_opener:
        opened = 1
        while opened and i < len(expr_string):
            if expr_string[i] == '(':
                opened += 1
            if expr_string[i] == ')':
                opened -= 1
            i += 1
        if i == len(expr_string):
            expr_string += ')'
        else:
            expr_string = expr_string[:i] + ')' + expr_string[i:]
    else:
        dig_cnt = 0
        while i < len(expr_string) and (
                    expr_string[i].isdigit() or expr_string[i] == '.' or expr_string[i] == '-' or expr_string[
            i] == '('):
            if expr_string[i] == '(':
                expr_string = add_closure(expr_string, index + 1, True)
                return expr_string
            if dig_cnt != 0 and expr_string[i] == '-':
                break
            if expr_string[i].isdigit():
                dig_cnt += 1
            i += 1
        if dig_cnt == 0:
            print("Error - No operand after given operator: \'" + str(expr_string[index - 1]) + "\'")
        else:
            expr_string = expr_string[:i] + ')' + expr_string[i:]
    return expr_string


def strongest_operator_index(stack, oprtor_dict):
    """
    :param stack: The main (or bracket) stack the program runs on, divided
    by two types - string and float (operators and operands).
    :param oprtor_dict: A dictionary from the calculator module that contains
    the operators as a key. each key has a list as a value that contains the
    significance of its key, the function that calculates according to it and
    the sides the operator gets operands from.
    :return: The index of the first most significant operator there is from
    the given stack.
    """
    max_index = None
    max_power = 0
    for item in range(len(stack)):
        if stack[item] in oprtor_dict.keys():
            curr_power = oprtor_dict[stack[item]][0]
            if max_power < curr_power:
                max_index = item
                max_power = curr_power
    return max_index


def arithmetic_val(stack, oprtor_index, oprtor_dict):
    """
    :param stack: The main (or bracket) stack the program runs on, divided
    by two types - string and float (operators and operands).
    :param oprtor_index: The index of an operator (if there is any) in a given
    stack.
    :param oprtor_dict: A dictionary from the calculator module that contains
    the operators as a key. each key has a list as a value that contains the
    significance of its key, the function that calculates according to it and
    the sides the operator gets operands from.
    :return: True or False if the expression is mathematically right or not -
    if from both left and right of the operator's index its conditions are true
    ot false. It also returns a string flag that can be important for the rest
    of the script's run.
    """
    try:
        if oprtor_index is None and len(stack) == 1:
            raise Exception("no operator to check on")
        elif oprtor_index is None and len(stack) != 1:
            return False, "none"
        if oprtor_dict[stack[oprtor_index]][2] == "lr":
            return from_left(stack, oprtor_index, True) and from_right(stack, oprtor_index, True), "lr"
        if oprtor_dict[stack[oprtor_index]][2] == "ln":
            return from_left(stack, oprtor_index, True) and not from_right(stack, oprtor_index), "ln"
        if oprtor_dict[stack[oprtor_index]][2] == "nr":
            return not from_left(stack, oprtor_index) and from_right(stack, oprtor_index, True), "nr"
    except:
        return False, "no operator to check on."


def from_left(stack, oprtor_index, necessary=False):
    """
    :param stack:
    :param oprtor_index:
    :param necessary:
    :return:
    """
    if oprtor_index >= 1:
        if not necessary:
            if isinstance(stack[oprtor_index - 1], float):
                print("ERROR - " + "\'" + str(stack[oprtor_index - 1])
                      + "\'" + " cannot be before the the given operator: " + str(stack[oprtor_index]))
                return False
        if not isinstance(stack[oprtor_index - 1], float):
            if necessary:
                print("ERROR - " + "\'" + str(stack[oprtor_index - 1]) + "\'" +
                      " is not a valid operand for the given operator: " + str(stack[oprtor_index]))
            return False
        else:
            return True
    else:
        if necessary:
            print("ERROR - There is no operand before the given operator: " + str(stack[oprtor_index]))
        return False


def from_right(stack, oprtor_index, necessary=False):
    try:
        if not necessary:
            if isinstance(stack[oprtor_index + 1], float):
                print("ERROR - " + "\'" + str(stack[oprtor_index + 1])
                      + "\'" + " cannot be before the the given operator: " + str(stack[oprtor_index]))
                return False
        if not isinstance(stack[oprtor_index + 1], float) or isinstance(stack[oprtor_index + 1], int):
            if necessary:
                print("ERROR - " + "\'" + str(stack[oprtor_index + 1]) + "\'" +
                      " is not a valid operand for the given operator: " + str(stack[oprtor_index]))
            return False
        else:
            return True
    except IndexError:
        if necessary:
            print("ERROR - There is no operand after the given operator: " + str(stack[oprtor_index]))
        return False
