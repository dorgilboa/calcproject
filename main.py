from solver import evaluate_expression


def main():
    """
    Welcome to the main file of the Calculate project that was made by
    Dor Gilboa. You will be able to find this project on github:
    https://github.com/dorgilboa/calcproject
    In order to use the console app correctly - run this file. To see the
    usage of the pytest - go to 'test_calculator.py' file. All functions
    are documented.
    """
    expression_input = get_expr()
    while expression_input is not None and expression_input != "e":
        if expression_input is not None:
            expr_result = evaluate_expression(expression_input)
            if type(expr_result) == float:
                print("ANSWER: " + str(expr_result))
        expression_input = get_expr()

def get_expr():
    """
    :return: input string expression. Function built to deal with
    EOF exceptions.
    """
    try:
        print("--------------------------")
        expression_input = str(input("Please enter an expression\n<for exit - type e>\nENTER HERE: "))
        return expression_input
    except EOFError as eofe:
        print("Error - Closed \'stdin\' file from keyboard without data in it, run the code again.")


if __name__ == '__main__':
    main()