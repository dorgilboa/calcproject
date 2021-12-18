from solver import *
import pytest


def test_evaluate_expression():
    assert evaluate_expression("3*^2") is None
    assert evaluate_expression("1+") is None
    assert evaluate_expression("5!(2+3)") is None
    assert evaluate_expression("4-~~5") is None
    assert evaluate_expression("*5/4") is None

    assert evaluate_expression("ahuefla") is None

    assert evaluate_expression("  \t  \t") is None

    assert evaluate_expression("7+ 3+1+-3") == 8.0
    assert evaluate_expression("8-2---5-1") == 0.0
    assert evaluate_expression("5*4*-2") == -40.0
    assert evaluate_expression("7/(3/3)") == 7.0
    assert evaluate_expression("2^-2") == 0.25
    assert evaluate_expression("(12*2) @2") == 13.0
    assert evaluate_expression("8$-5") == 8.0
    assert evaluate_expression("8&-5") == -5.0
    assert evaluate_expression("8%5") == 5.0
    assert evaluate_expression("~ --15") == -15.0
    assert evaluate_expression("3!!") == 720.0
    assert evaluate_expression("~-(-5)") == -5.0
    assert evaluate_expression("4*-~-1") == -4.0
    assert evaluate_expression("-~12@13") == 12.5
    assert evaluate_expression("7/-7") == -1.0
    assert evaluate_expression("-1!") is None
    assert evaluate_expression("-8^0.5") is None
    assert evaluate_expression("6%0") is None

    assert evaluate_expression("1  ^2*(5 +2^ (3-1))*(2+ 3) +2^3  *2") == 61.0
    assert evaluate_expression("-(-(-(-~-(3*-4*(2--1)))))+1") == -35.0
    assert evaluate_expression("~(5+(-6*(7-(5*6)-5)))") == -173.0
    assert evaluate_expression("2*(5--((1+2)+(3*(2+1))))") == 34.0
    assert evaluate_expression("((-3*(---~---1))^(8-~-(12^0*8)))!!") == 1.0
    assert evaluate_expression("(7+5)!*(2-~5$3) +160  0") == -479000000.0
    assert evaluate_expression("(8^(1/3)*0.5)$-~-1+(2*2)") == 5.0
    assert evaluate_expression("~(5+ 2 *6    ^(3 +1))@( 3!-7)") == -1299.0
    assert evaluate_expression("12^2/12- 12 * (1  .2 / 10^2)") == 11.856
    assert evaluate_expression("((-~- -(6  -2)!)   - 25@ 7*-~5  +( 1 5/2)+1 1)") == -37.5
    assert evaluate_expression("28.5  /(4/8)-- -~-   4!+15&7 *(1+1-1)") == 40.0
    assert evaluate_expression("-2 +3+ 2* ( 3!-7)- 3  ^6+ (8& 7)") == -723.0
    assert evaluate_expression("8--(7- 9)*2^(  10-9*(8+(7^-  (-2)+5)))----- 6    +34") == 36.0
    assert evaluate_expression("6&2*(12^2)/   (3---~-1)*-2") == -288.0
    assert evaluate_expression("(3!!)/(-(92^4))*(-(4!!))/(150^(3!))") == 547443.4990956632
    assert evaluate_expression("(~---------51)!/(3^(152+4!))+(---------(81^2))") == -6561.0
    assert evaluate_expression("2^(2^(2^2))/(9!)*  3.14") == 0.5670828924162258
    assert evaluate_expression("((-150*(1/3!))^2)^2 +-300") == 390325.0
    assert evaluate_expression("~-(5--7*14. 2-(12^0.5))*(3^3)") == 2725.2692563912806
    assert evaluate_expression("123123 . 123 / 123.123 *(3-1+-2)") == 0.0
    assert evaluate_expression("(123123 . 123 / 123.123) ^(3-1+-2)") == 1.0
    assert evaluate_expression("(123123 . 123 / 123.123) /(3-1+-2)") is None
    assert evaluate_expression("5!(12---~-1*3.2/(1+3))+20") is None
    assert evaluate_expression("5!(12---~-1*3.2/(1+3))/0") is None