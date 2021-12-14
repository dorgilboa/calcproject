import math


def fact(oprnd1, oprnd2=None):
    try:
        if not oprnd1 < 0:
            res = 1
            for i in range(2, int(oprnd1) + 1):
                res *= i
            return float(res)
        print("factorial of " + str(oprnd1) + " is not possible")
    except OverflowError as err:
        print(err)


def switch_sign(oprnd1, oprnd2=None):
    try:
        return -oprnd1
    except OverflowError as err:
        print(err)


def add(oprnd1, oprnd2):
    try:
        return oprnd1 + oprnd2
    except OverflowError as err:
        print(err)


def sub(oprnd1, oprnd2):
    try:
        return oprnd1 - oprnd2
    except OverflowError as err:
        print(err)


def mult(oprnd1, oprnd2):
    try:
        return oprnd1 * oprnd2
    except OverflowError as err:
        print(err)


def divi(oprnd1, oprnd2):
    try:
        return oprnd1 / oprnd2
    except OverflowError as err1:
        print(err1)
    except ZeroDivisionError as err2:
        print(err2)


def powr(oprnd1, oprnd2):
    try:
        return math.pow(oprnd1, oprnd2)
    except OverflowError as err1:
        print(err1)
    except ValueError as err2:
        print("ERROR - Given operand " + str(oprnd1) + " is not valid for squared method.")


def avrg(oprnd1, oprnd2):
    try:
        return (oprnd1 + oprnd2) / 2
    except OverflowError as err:
        print(err)


def maxi(oprnd1, oprnd2):
    try:
        if (oprnd1 > oprnd2):
            return oprnd1
        return oprnd2
    except OverflowError as err:
        print(err)


def mini(oprnd1, oprnd2):
    try:
        if (oprnd1 < oprnd2):
            return oprnd1
        return oprnd2
    except OverflowError as err:
        print(err)


def modu(oprnd1, oprnd2):
    try:
        return oprnd1 % oprnd2
    except OverflowError as err:
        print(err)


class Calculator(object):
    oprtor_dict = {'!': [6, fact, "ln"], '~': [6, switch_sign, "nr"], '&': [5, mini, "lr"], '$': [5, maxi, "lr"],
                   '@': [5, avrg, "lr"],
                   '%': [4, modu, "lr"], '^': [3, powr, "lr"], '/': [2, divi, "lr"], '*': [2, mult, "lr"],
                   '+': [1, add, "lr"], '-': [1, sub, "lr"]}

    def __init__(self, operator, operand1, operand2=None):
        self.operator = operator
        self.operand1 = operand1
        self.operand2 = operand2

    def get_result(self):
        return self.oprtor_dict[self.operator][1](self.operand1, self.operand2)
