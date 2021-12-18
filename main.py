from solver import evaluate_expression


def main():
    expression_input = get_expr()
    while expression_input is not None and expression_input != "e":
        if expression_input is not None:
            expr_result = evaluate_expression(expression_input)
            if expr_result is not None:
                print("ANSWER: " + str(expr_result))
        expression_input = get_expr()

def get_expr():
    try:
        print("--------------------------")
        expression_input = str(input("Please enter an expression\n<for exit - type e>\nENTER HERE: "))
        return expression_input
    except EOFError as eofe:
        print("Error - Closed \'stdin\' file from keyboard without data in it, run the code again.")


if __name__ == '__main__':
    main()