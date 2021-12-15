from solver import evaluate_expression


def main():
    expression_input = get_expr()
    while expression_input and expression_input != "e":
        if expression_input and expression_input != " ":
            expr_result = evaluate_expression(expression_input)
            if expr_result:
                print("ANSWER: " + str(expr_result))
        expression_input = get_expr()

def get_expr():
    try:
        print("--------------------")
        expression_input = str(input("Please enter an expression\n<for exit - type e>\nENTER HERE: "))
        expression_input = expression_input.replace(" ", "")
        expression_input = expression_input.replace("\t", "")
        if expression_input == "":
            raise Exception("Error - No data has been received from user.")
        detect_lang(expression_input)
        return expression_input
    except EOFError as eofe:
        print("Error - Closed \'stdin\' file from keyboard without data in it, run the code again.")
    except Exception as err:
        print(err)
        return " "


def detect_lang(expression):
    for char in expression:
        asc = ord(char)
        if asc < 0 or asc >= 256:
            raise Exception("Error - Unsupported language had been detected try to use a default ENG keyboard.")


if __name__ == '__main__':
    main()