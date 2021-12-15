from solver import evaluate_expression


def main():
    expression_input = get_expr()
    while expression_input != "e":
        if expression_input != "":
            print("ANSWER: " + str(evaluate_expression(expression_input)))
        expression_input = get_expr()

def get_expr():
    try:
        print("--------------------")
        expression_input = str(input("Please enter an expression\n<for exit - type e>\nENTER HERE: "))
        if expression_input == "":
            raise Exception("Error - No data has been recieved from user.")
    except EOFError as eofe:
        print("Error - Got file from keyboard without data in it.")
    except Exception as err:
        print(err)
    finally:
        return expression_input


if __name__ == '__main__':
    main()