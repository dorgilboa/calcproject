def syntax_val(expr_string, oprtor_dict):
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
        index+=1
    return expr_stack


def convert_to_number(str_number):
    try:
        if str_number[0] == '.' or str_number[-1] == '.':
            raise ValueError("Not full number defining.")
        return float(str_number)
    except ValueError:
        print(str(str_number) + " conversion to number cannot be done.")
        return None


def treat_minuses(expr_string, index, expr_stack, oprtors_dict):
    minustr = ""
    # sign minuses:
    if index == 0 or not (expr_string[index - 1].isdigit() or expr_string[index - 1] == ')' or (
        expr_string[index - 1] in oprtors_dict.keys() and oprtors_dict[expr_string[index - 1]][2] == 'ln')):
        while expr_string[index] == '-':
            minustr += expr_string[index]
            index+=1
    # sign minuses before brackets or tilda and so...
    if len(minustr) != 0:
        if (expr_string[index] in oprtors_dict.keys() and oprtors_dict[expr_string[index]][2] == 'nr') or expr_string[index] == '(':
            if len(minustr) % 2 != 0:
                expr_stack.append('(')
                expr_stack.append(float(-1.0))
                expr_stack.append('*')
                if expr_string[index] == '(':
                    expr_string = add_closure(expr_string,index+1, True)
                elif expr_string[index] in oprtors_dict.keys() and oprtors_dict[expr_string[index]][2] == 'nr':
                    if expr_string[index+1] == '(':
                        expr_string = add_closure(expr_string, index+1, True)
                    else:
                        expr_string =  add_closure(expr_string, index+1, False)
                    # minus_brack = True
            expr_stack.append(expr_string[index])
            return "", index, expr_string
        if len(minustr) % 2 != 0:
            return '-', index, expr_string
    return '', index, expr_string


def add_closure(expr_string, index, is_opener):
    i = index
    if is_opener:
        opened = 1
        while opened and i < len(expr_string):
            if expr_string[i] == '(':
                opened+=1
            if expr_string[i] == ')':
                opened -=1
            i+=1
        if i == len(expr_string):
            expr_string+= ')'
        else:
            expr_string = expr_string[:i] + ')' + expr_string[i:]
    else:
        dig_cnt = 0
        found_opener = False
        while i < len(expr_string) and (expr_string[i].isdigit() or expr_string[i] == '.' or expr_string[i] == '-' or expr_string[i] == '('):
            if expr_string[i] == '(':
                found_opener = True
                expr_string = add_closure(expr_string, index+1, True)
                return expr_string
            if dig_cnt != 0 and expr_string[i] == '-':
                break
            if expr_string[i].isdigit():
                dig_cnt+=1
            i+=1
        if dig_cnt == 0:
            print("Error - No operand after given operator: \'" + str(expr_string[index-1]) + "\'")
        else:
            expr_string = expr_string[:i] + ')' + expr_string[i:]
    return expr_string


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
        if not isinstance(str_stack[oprtor_index - 1], float):
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