def syntax_val(expr_string, oprtor_dict):
    invalid_chars = ""
    for char in expr_string:
        if char not in oprtor_dict.keys() and not char.isdigit() and not char == '.' \
                and not char == '(' and not char == ')':
            invalid_chars += "\'" + str(char) + "\', "
    if invalid_chars == "":
        pars_val, msg = check_parentheses(expr_string)
        if pars_val:
            oprtors_val, msg = oprtors_at_start_or_end(expr_string, oprtor_dict)
            if oprtors_val:
                return True, msg
            else:
                return False, msg
        else:
            return False, msg
    return False, invalid_chars + "are not valid chars..."


def seperate_expression(expr_string, oprtor_dict):
    expr_stack = []
    i = 0
    waiting_for_num = False
    while i < len(expr_string):
        curr_i = i
        tempstr = ""
        waiting_for_num, tempstr, i = treat_minuses(i, expr_string, expr_stack, oprtor_dict, tempstr, waiting_for_num)
        if i < len(expr_string) and (expr_string[i].isdigit() and tempstr != '+'):
            while i < len(expr_string) and (expr_string[i].isdigit() or expr_string[i] == '.'):
                tempstr += expr_string[i]
                i += 1
            expr_stack.append(convert_to_number(tempstr))
            if waiting_for_num:
                expr_stack.append(')')
        if curr_i < len(expr_string) and curr_i == i and (
                            expr_string[curr_i] in oprtor_dict.keys() or expr_string[curr_i] == '(' or expr_string[
                    curr_i] == ')'):
            expr_stack.append(expr_string[curr_i])
            i += 1
        elif i < len(expr_string) and tempstr == '' and (
                not expr_string[i] in oprtor_dict.keys() or not expr_string[i] == '(' or not expr_string[
            i] == ')'):
            return [], "ERROR - Expression - \'" + expr_string + "\' is illegal."
    return expr_stack, "all fine"


def treat_minuses(i, expr_string, expr_stack, oprtor_dict, tempstr, waiting_for_num):
    start_i = i
    while i < len(expr_string) and (
                    expr_string[i] == '-' and (
                            i == 0 or not (expr_string[i - 1].isdigit() or expr_string[i - 1] == ')'))):
        tempstr += "-"
        i += 1
    if tempstr == "":
        if waiting_for_num and (
                    (expr_string[i] in oprtor_dict and oprtor_dict[expr_string[i]][2] == "nr") or ((expr_string[
                    i].isdigit()) or expr_string[i] == '(' or expr_string[i] == ')')):
            return True, tempstr, i
        return False, tempstr, i
    else:
        if i < len(expr_string) and (
                        expr_string[i] == '(' or (
                        expr_string[i] in oprtor_dict and oprtor_dict[expr_string[i]][2] == "nr")):
            if expr_string[start_i - 1] == '-':
                tempstr += expr_stack.pop()
                if len(tempstr) % 2 == 0:
                    tempstr = '+'
                else:
                    tempstr = '-'
                expr_stack.append(tempstr)
            elif not expr_stack or (
                expr_stack and (expr_stack[-1] in oprtor_dict.keys() and not oprtor_dict[expr_stack[-1]][2] == "ln")):
                expr_stack.append('(')
                if len(tempstr) % 2 == 0:
                    expr_stack.append(float(1.0))
                else:
                    expr_stack.append(float(-1.0))
                expr_stack.append('*')
                return True, tempstr, i
        if tempstr != '' and waiting_for_num and (expr_string[i].isdigit() or expr_string[i] == ')'):
            tempstr = reduce_minuses(tempstr)
            return True, tempstr, i
        tempstr = reduce_minuses(tempstr)
        return False, tempstr, i


def reduce_minuses(str_minuses):
    if len(str_minuses) % 2 == 0:
        return ''
    return '-'


def convert_to_number(str_number):
    try:
        if str_number[0] == '.' or str_number[-1] == '.':
            raise ValueError("Not full number defining.")
        return float(str_number)
    except ValueError:
        print(str(str_number) + " conversion to number cannot be done.")
        return None


def oprtors_at_start_or_end(string_expr, oprtor_dict):
    if string_expr[0] in oprtor_dict.keys() and not (string_expr[0] == '-' or oprtor_dict[string_expr[0]][2] == "nr"):
        return False, "Error - The operator " + string_expr[0] + " can't' be written at start."
    if string_expr[-1] in oprtor_dict.keys() and not oprtor_dict[string_expr[-1]][2] == "ln":
        return False, "Error - The operator " + string_expr[-1] + " can't' be written at end."
    return True, "all valid"


def strongest_operator_index(str_stack, oprtor_dict):
    max_index = None
    max_power = 0
    for item in range(len(str_stack)):
        if str_stack[item] in oprtor_dict.keys():
            curr_power = oprtor_dict[str_stack[item]][0]
            if curr_power == 6:
                return item
            if max_power < curr_power:
                max_index = item
                max_power = curr_power
    return max_index


def arithmetic_val(str_stack, oprtor_index, oprtor_dict):
    try:
        if oprtor_index is None and len(str_stack) == 1:
            raise Exception("no operator to check on")
        elif oprtor_index is None and len(str_stack) != 1:
            print("ERROR: " + str(str_stack[0]) + " " + str(str_stack[1]) + ", This is not a valid expression..")
            return False, "none"
        if oprtor_dict[str_stack[oprtor_index]][2] == "lr":
            return from_left(str_stack, oprtor_index, True) and from_right(str_stack, oprtor_index, True), "lr"
        if oprtor_dict[str_stack[oprtor_index]][2] == "ln":
            return from_left(str_stack, oprtor_index, True) and not from_right(str_stack, oprtor_index), "ln"
        if oprtor_dict[str_stack[oprtor_index]][2] == "nr":
            return not from_left(str_stack, oprtor_index) and from_right(str_stack, oprtor_index, True), "nr"
    except:
        return False, "no operator to check on."


def from_left(str_stack, oprtor_index, necessary=False):
    if oprtor_index >= 1:
        if not isinstance(str_stack[oprtor_index - 1], float) or isinstance(str_stack[oprtor_index - 1], int):
            if necessary:
                print(str("ERROR - " + "\'" +
                          str_stack[
                              oprtor_index - 1]) + "\'" + " is not a valid operand for the given operator: " + str(
                    str_stack[oprtor_index]))
            return False
        else:
            return True
    else:
        if necessary:
            print("ERROR - There is no operand before the given operator: " + str(str_stack[oprtor_index]))
        return False


def from_right(str_stack, oprtor_index, necessary=False):
    try:
        if not isinstance(str_stack[oprtor_index + 1], float) or isinstance(str_stack[oprtor_index + 1], int):
            if necessary:
                print(str("ERROR - " + "\'" +
                          str_stack[
                              oprtor_index + 1]) + "\'" + " is not a valid operand for the given operator: " + str(
                    str_stack[oprtor_index]))
            return False
        else:
            return True
    except IndexError:
        if necessary:
            print("ERROR - There is no operand after the given operator: " + str(str_stack[oprtor_index]))
        return False


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
