import math


def fact(oprnd1, oprnd2=None):
    """
    :param oprnd1: An operand to calc his factorial.
    :param oprnd2: None always. This function will never be sent with more
    than one valid operand.
    :return: The factorial of the oprnd1 varriable, if it is able to calc.
    """
    try:
        if not oprnd1 < 0:
            res = 1
            for i in range(2, int(oprnd1) + 1):
                res *= i
            return float(res)
        raise Exception("factorial of " + str(oprnd1) + " is not possible")
    except OverflowError as err1:
        print(err1)
    except Exception as err2:
        print(err2)


def switch_sign(oprnd1, oprnd2=None):
    """
    :param oprnd1: An operand to switch his sign.
    :param oprnd2: None always. This function will never be sent with more
    than one valid operand.
    :return: The inverse of the oprnd1 varriable.
    """
    try:
        return -oprnd1
    except OverflowError as err:
        print(err)


def add(oprnd1, oprnd2):
    """
    :param oprnd1: The 1st operand.
    :param oprnd2: The 2nd operand.
    :return: The addition of oprnd1 and oprnd2.
    """
    try:
        return oprnd1 + oprnd2
    except OverflowError as err:
        print(err)


def sub(oprnd1, oprnd2):
    """
    :param oprnd1: The 1st operand.
    :param oprnd2: The 2nd operand.
    :return: The subtraction of oprnd2 from oprnd1.
    """
    try:
        return oprnd1 - oprnd2
    except OverflowError as err:
        print(err)


def mult(oprnd1, oprnd2):
    """
    :param oprnd1: The 1st operand.
    :param oprnd2: The 2nd operand.
    :return: The multiplication of oprnd1 and oprnd2.
    """
    try:
        return oprnd1 * oprnd2
    except OverflowError as err:
        print(err)


def divi(oprnd1, oprnd2):
    """
    :param oprnd1: The 1st operand.
    :param oprnd2: The 2nd operand.
    :return: The division of oprnd2 from oprnd1, unless oprnd2 is 0,
    then it is mathematically illegal.
    """
    try:
        return oprnd1 / oprnd2
    except OverflowError as err1:
        print(err1)
    except ZeroDivisionError as err2:
        print(err2)


def powr(oprnd1, oprnd2):
    """
    :param oprnd1: The 1st operand.
    :param oprnd2: The 2nd operand.
    :return: The power of oprnd1 by oprnd2, unless oprnd2 is not an
    integer, then if oprnd1 is a negative number it is mathematically
    illegal.
    """
    try:
        return math.pow(oprnd1, oprnd2)
    except OverflowError as err1:
        print(err1)
    except ValueError as err2:
        print("ERROR - Given operand " + str(oprnd1) + " is not valid for squared method.")


def avrg(oprnd1, oprnd2):
    """
    :param oprnd1: The 1st operand.
    :param oprnd2: The 2nd operand.
    :return: The average between the two operands.
    """
    try:
        return (oprnd1 + oprnd2) / 2
    except OverflowError as err:
        print(err)


def maxi(oprnd1, oprnd2):
    """
    :param oprnd1: The 1st operand.
    :param oprnd2: The 2nd operand.
    :return: The bigger operand.
    """
    try:
        if (oprnd1 > oprnd2):
            return oprnd1
        return oprnd2
    except OverflowError as err:
        print(err)


def mini(oprnd1, oprnd2):
    """
    :param oprnd1: The 1st operand.
    :param oprnd2: The 2nd operand.
    :return: The smaller operand.
    """
    try:
        if (oprnd1 < oprnd2):
            return oprnd1
        return oprnd2
    except OverflowError as err:
        print(err)


def modu(oprnd1, oprnd2):
    """
    :param oprnd1: The 1st operand.
    :param oprnd2: The 2nd operand.
    :return: The remainder that we get from the division function.
    If oprnd2 is 0 - None - can't divide by 0.
    """
    try:
        if oprnd2 == 0:
            raise ZeroDivisionError("Error - Divide by 0 while calculating modulu (\'%\').")
        return oprnd1 % oprnd2
    except OverflowError as err1:
        print(err1)
    except ZeroDivisionError as err2:
        print(err2)


class Calculator(object):
    """
    :param oprtor_dict: A dictionary from the calculator module that contains
    the operators as a key. each key has a list as a value that contains the
    significance of its key, the function that calculates according to it and
    the sides the operator gets operands from. This dictionary is actually a
    router from operand to the result it should bring to the user, and is a
    main part of many functions in this project.
    """
    oprtor_dict = {'!': [6, fact, "ln"], '~': [6, switch_sign, "nr"], '&': [5, mini, "lr"], '$': [5, maxi, "lr"],
                   '@': [5, avrg, "lr"],
                   '%': [4, modu, "lr"], '^': [3, powr, "lr"], '/': [2, divi, "lr"], '*': [2, mult, "lr"],
                   '+': [1, add, "lr"], '-': [1, sub, "lr"]}

    def __init__(self, operator, operand1, operand2=None):
        self.operator = operator
        self.operand1 = operand1
        self.operand2 = operand2

    def get_result(self):
        """
        :return: This function calls for the function that suit to the operator
        key according to the dictionary, and returns the calculation of the given
        expression that we always contain at least one operand, and an operator.
        """
        return self.oprtor_dict[self.operator][1](self.operand1, self.operand2)
